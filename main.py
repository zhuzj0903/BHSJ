#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : main.py
# @time : 2021/1/30 14:59
# @Software :PyCharm

"""
入口函数，pytest执行的统一入口
"""

import pytest
from Common.dir_config import *
from Common.read_config import Read_Config as R
from Common.send_mail import sendmail as S
import datetime
import sys
import os

# 读取配置文件
htmls = R(config_dir, 'html.yaml').read_yaml()
mes = R(config_dir, 'email.yaml').read_yaml()
# 定义时间戳
time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M')
# 定义html报告格式及样式
if sys.platform == 'win32':
    htmlpath = htmltestreport_dir + '\\{0}-{1}.html'.format(time, htmls['项目名称'])
else:
    htmlpath = htmltestreport_dir + '/{0}-{1}.html'.format(time, htmls['项目名称'])

if __name__ == '__main__':
    '''全部运行'''
    # pytest.main(["-q","--html="+htmlpath])

    '''指定文件夹运行'''
    if sys.platform == 'win32':
    #     pytest.main(["-q", "TestCases\\test_firstpage.py", "--html=" + htmlpath])
        '''指定标记运行,如果执行具体的py文件需要写上绝对路径,可以配合上面的执行策略一起使用'''
        pytest.main(["-q","TestCases\\登录测试\\test_login.py","-m=smoke","--html="+htmlpath,"--self-contained-html"])
    # else:
    #     pytest.main(["-q", "TestCases/登录测试/test_login.py", "--html=" + htmlpath])
    #发送测试报告邮件
    S(mes['from'],mes['pwd'],mes['to'],htmlpath).send()
