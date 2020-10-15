<div align="center">

<h1 align="center">
	cvxEDA for E4
</h1>

</div>
</div>

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytorch-lightning)]()
[![Conda](https://img.shields.io/conda/v/conda-forge/pytorch-lightning?label=conda&color=success)]()
[![Build Status](https://travis-ci.org/soimort/you-get.svg)]()

## Introduce
#### cvxEDA for E4,is a tool for EDA data analysis.It is developed based on `eda-explorer` and `cvxEDA`.Using this tool,you can easily analyze the EDA data measuring by the Empatica E4 wristband.
## Prerequisites
#### The tool is run with `Python 3.5+ `(recommended with Python 3.8).
####For convenience,you can install Anaconda.The software is free and you can download it through:`https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/`
#### Also,you need to install some required packages that can ensure you succeed to run the program.The list of required packages is in the requirement.txt.You can run the code to install rapidly.
    pip install requirement.txt -r
## Installation
#### There are three ways to install this tool,and you can choose anyone according to your preference.
#### 1.Download .zip instantly.
#### 2.Use git method to install
    git clone https://github.com/JiehangXie/E4_cvxEDA.git
#### 3.Download compiled version directly.
#### `Link：https://pan.baidu.com/s/1LZzyU_9kLMt6GTqw3u4b4A  Code：lxcf`
## Using Method
### 1.Download the data package from the Empatica website.
### 2.Extract the data package.
### 3.Press Win+R ,open CMD windows,input command:(Compiled version can skip this step!)
    python E4_cvxEDA.py
### 4.Enter the data file directory as prompted.
### 5.Check the artifact data
> Pay attendtion to the `artifact rate`.If it is over 15% or more,the data sample may be wrong.!!!
### 6.If the data is correct,close the window.And then the program will **automatically** create a file named	`MIT_Labels.csv` and `Tonic.csv`
## Quote & More Technical Detail
###eda-explorer - https://github.com/MITMediaLabAffectiveComputing/eda-explorer
###cvxEDA - https://github.com/lciti/cvxEDA
