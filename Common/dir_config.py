#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : dir_config.py
# @time : 2020/10/10 17:35
# @Software :PyCharm

import os
import sys
"""
定义框架层级的相对目录位置
"""

base_dir=os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

config_dir=os.path.join(base_dir,'Config')

htmltestreport_dir=os.path.join(base_dir,'HtmlTestReport')

if sys.platform == "win32":
    processlog_dir = os.path.join(base_dir,'Logs\\processlog')
else:
    processlog_dir = os.path.join(base_dir,'Logs/processlog')

if sys.platform =='win32':
    resultlog_dir = os.path.join(base_dir,'Logs\\resultlog')
else:
    resultlog_dir = os.path.join(base_dir, 'Logs/resultlog')

pageobject_dir=os.path.join(base_dir,'PageObjects')

screenshots_dir=os.path.join(base_dir,'ScreenShots')

testcases_dir=os.path.join(base_dir,'TestCases')

testdatas_dir=os.path.join(base_dir,'TestCases')

if __name__=="__main__":
    print(base_dir,testcases_dir,testdatas_dir)