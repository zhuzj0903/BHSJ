#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : firstpage.py
# @time : 2020/11/18 10:38
# @Software :PyCharm

from Common.BasePage import *
from Common.log import Log
from Common.dir_config import *
from selenium.webdriver.common.by import By
import time

# 定义resultlog和processlog
P_log = Log(processlog_dir)
R_log = Log(resultlog_dir)


class First_Page(BasePage):
    name='//i[@class="icon user-icon"]/following-sibling::span'#姓名
    account='(//div[@class="userInfo-line"])[1]/div[2]'#用户账号


    # 获取登录后的用户名
    def get_login_name(self):
        self.click(self.name)#点击用户姓名
        self.get_text(self.account)#获取账户名称
        return




    # # 点击进入系统管理下的子菜单
    # def manager(self, num, t):
    #     P_log.info('点击进入系统管理下的子菜单')
    #     self.move_mouse(self.mager)  # 鼠标悬停在管理上
    #     # self.find_elements(self.sysmager)[num].click()  # 点击管理下边的元素进入系统管理
    #     self.clicks(self.sysmager, By.CSS_SELECTOR, 40, 'visible', num)  # 点击管理下边的元素进入系统管理
    #     for handle in self.driver.window_handles:  # 获取当前浏览器所有窗口句柄
    #         self.driver.switch_to.window(handle)  # 得到该窗口的标题栏字符串
    #         if t in self.driver.title:  # 判断当前窗口是否包含该字符串，如果是，跳出循环
    #             break