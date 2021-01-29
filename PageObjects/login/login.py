#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : login.py
# @time : 2020/11/18 10:37
# @Software :PyCharm

from Common.BasePage import *


class login(BasePage):
    #北邮平台
    account='//input[@placeholder="请输入登录帐号"]'
    pwd='//input[@placeholder="请输入登录密码"]'
    login_button='//button[text()="登录"]'



    def login_system(self,user,password):
        '''
        登录系统
        :param user: 用户名
        :param password: 密码
        :return:
        '''
        self.input_text(self.account,user)
        self.input_text(self.pwd,password)
        self.click(self.login_button)
