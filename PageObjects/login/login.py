#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : login.py
# @time : 2020/11/18 10:37
# @Software :PyCharm

from Common.BasePage import *


class login(BasePage):
    account='//input[@placeholder="用户名"]'
    pwd='//input[@placeholder="密码"]'
    login_button='//span[text()="登录"]/..'



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
