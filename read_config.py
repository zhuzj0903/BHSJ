#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : read_config.py
# @time : 2020/11/18 10:41
# @Software :PyCharm

'''
读取配置文件，yaml,config

'''
import yaml
# import configparser
from Common import dir_config
import sys


class Read_Config:
    def __init__(self,path,file,section=None,option=None):
        self.path = path
        self.file = file
        self.section = section
        self.option = option

    #读取yaml文件
    def read_yaml(self):
        if sys.platform == 'win32':
            newpath = self.path+'\\'+self.file
            # print(newpath)
            fs = open(newpath,'rb')
            datas = yaml.full_load(fs)
            return datas[0]
        else:
            newpath = self.path + '/' + self.file
            # print(newpath)
            fs = open(newpath, 'rb')
            datas = yaml.full_load(fs)
            return datas[0]

    #读取普通配置文件
    def read_config(self,file_path,section,option):
        pass



if __name__ == '__main__':
    datas = Read_Config(dir_config.config_dir,'url.yaml').read_yaml()
    print(datas)
