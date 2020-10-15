import time
import numpy as np
import pandas as pd
import pylab as pl
import edas
import cvxEDA
import os
import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['text.usetex']=False #禁用LaTex


def correct_eda(file,mit_file):
    '''
    EDA数据修正
    :return:
    '''

    #源文件处理
    data = pd.read_csv(file,header=None)
    begin_time = int(data.iat[0,0].astype('int')) #开始时间 第1行，第1列
    hz = int(data.iat[1,0].astype('int')) #赫兹 第2行，第1列
    eda_data = data.iloc[2:] #EDA数据

    data_reshape = []
    for i in range(len(eda_data)):
        data_time = int(begin_time + i*1/hz) #计算时间戳
        data_reshape.append([data_time,eda_data.iat[i,0]])
    #print(data_reshape)

    #MIT检测文件处理
    mit_data = []
    data_mit = pd.read_csv(mit_file)
    for t in range(len(data_mit['StartTime'])):
        starttimeArray = time.strptime(data_mit['StartTime'][t], "%Y-%m-%d %H:%M:%S")
        starttimeStamp = int(time.mktime(starttimeArray)) + 28800 #时间加东八区
        Label_mit = data_mit['BinaryLabels'][t] #读取标签
        for s in range(0,5):
            for s1 in range(0,4):
                time_process = starttimeStamp + s
                mit_data.append([time_process,Label_mit])
    #print(mit_data)
    #print(len(data_reshape),len(mit_data))
    #文件比对合并
    data_combine = []
    #BUG-0904 EDA.csv不足4hz数据修复
    if len(mit_data)>len(data_reshape):
        loop_range = len(data_reshape)
    else:
        loop_range = len(mit_data)
    for c in range(loop_range): #以mit结果为准
        #print(c,data_reshape[c][0],mit_data[c][0])
        if data_reshape[c][0]==mit_data[c][0]:
            timestamp,EDA,Label = data_reshape[c][0],data_reshape[c][1],mit_data[c][1]
            data_combine.append([timestamp,EDA,Label]) #timestamp,EDA,Label

    #print(data_combine) #输出合并后的数据

    data_frame = pd.DataFrame(data_combine,columns=['TimeStamp','EDA','Label'])
    artifact_data = data_frame[data_frame['Label'] == -1]
    #clean_data = data_frame[data_frame['Label'] == 1]
    print("伪影率：{}%".format(round(len(artifact_data)/len(data_frame)*100,2)))
    df_clear = data_frame.drop(data_frame[data_frame['Label'] == -1].index)
    #print(df_clear)
    return df_clear

def mit_detection():
    '''
    eda-explorer
    :return:
    '''
    numClassifiers = 1

    if numClassifiers == 1:
        temp_clf = 1
        if temp_clf == 1:
            print('Binary Classifier selected')
            classifierList = ['Binary']
        elif temp_clf == 2:
            print('Multiclass Classifier selected')
            classifierList = ['Multiclass']
    else:
        classifierList = ['Binary', 'Multiclass']
    pd.set_option('mode.chained_assignment', None)  # Ignore the warning message
    #数据分类标签
    labels, data = edas.classify(classifierList)

    #保存数据为csv
    saveDataInput = 'y'

    if saveDataInput == 'y':
        outputPath = edas.get_user_input('\tEnter Path to E4 directory again: ')
        outputLabelFilename = "MIT_Labels"

        #保存标签
        fullOutputPath = os.path.join(outputPath, outputLabelFilename)
        if fullOutputPath[-4:] != '.csv':
            fullOutputPath = fullOutputPath + '.csv'

        featureLabels = pd.DataFrame(labels, index=pd.date_range(start=data.index[0], periods=len(labels), freq='5s'),
                                     columns=classifierList)

        featureLabels.reset_index(inplace=True)
        featureLabels.rename(columns={'index': 'StartTime'}, inplace=True)
        featureLabels['EndTime'] = featureLabels['StartTime'] + datetime.timedelta(seconds=5)
        featureLabels.index.name = 'EpochNum'

        cols = ['StartTime', 'EndTime']
        cols.extend(classifierList)

        featureLabels = featureLabels[cols]
        featureLabels.rename(columns={'Binary': 'BinaryLabels', 'Multiclass': 'MulticlassLabels'},
                             inplace=True)

        featureLabels.to_csv(fullOutputPath)

        print("Labels saved to " + fullOutputPath)
        #print("Remember! The first column is timestamps and the second column is the labels (-1 for artifact, 0 for questionable, 1 for clean)")
        MIT_Labels_Path = "{0}\{1}.csv".format(outputPath,outputLabelFilename)
        return MIT_Labels_Path,outputPath #返回MITlabels和数据文件夹路径

if __name__ == '__main__':
    MIT_Labels_Path,outputPath = mit_detection()
    #修正数据
    correct_data = correct_eda(r'{}\EDA.csv'.format(outputPath),MIT_Labels_Path)
    df = pd.DataFrame(correct_data,columns=['TimeStamp','EDA','Label'])
    #df.to_csv(r'{}\Tonic.csv'.format(outputPath),index=None)


    '''
    CVXEDA
    '''
    y = np.array(df['EDA'])

    # print(type(y))
    #print(y)
    Fs = 4  # 频率
    [r, p, t, l, d, e, obj] = cvxEDA.cvxEDA(y, 1. / Fs)
    tm = pl.arange(1., len(y) + 1.) / Fs

    #print(len(y), len(t))
    # Python3

    pl.figure(1)
    pl.title("Raw data,Phasic & Tonic")
    pl.plot(tm,y, label="Raw data")
    pl.plot(tm,r, label="Phasic")
    pl.plot(tm,t, label="Tonic")
    pl.legend()
    # pl.plot(tm,r)
    pl.show()

    new_list = zip(df['TimeStamp'],y,t)
    new_df = pd.DataFrame(new_list,columns=['TimeStamp','Raw_EDA','Tonic_EDA'])
    new_df.to_csv('{}\Tonic.csv'.format(outputPath),index=None)
    #程序运行结束
    print('Completed!')
    input('Press Enter to exit.')
