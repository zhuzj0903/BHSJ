#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : BasePage.py
# @time : 2020/10/10 17:36
# @Software :PyCharm

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from Common.log import Log
from Common.dir_config import *
import time
import os
import sys

# 定义resultlog和processlog
P_log = Log(processlog_dir)
R_log = Log(resultlog_dir)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()

    # 等待元素可见
    def wait_eleVisible(self, loctor, by=By.XPATH, wait_times=20):
        if by not in By.__dict__.values():
            P_log.error("定位类型[ {0} ]不在支持的定位类型范围内".format(by))
            raise InvalidSelectorException
        # 当前运行时间
        t1 = time.time()
        try:
            WebDriverWait(self.driver, wait_times, 1).until(EC.visibility_of_element_located((by, loctor)))
            t2 = time.time()
            # 结束时间 - 两者之差就是真正的等待时间
            P_log.info("等待时间长为:{0}".format(t2 - t1))
        except TimeoutException as e:
            P_log.error("等待元素超时.截取当前页面。")
            self.save_picture("等待元素失败")
            # 抛出异常
            raise e
        except InvalidSelectorException as e:
            P_log.error("元素定位表达式：{0}  不正确，请修正".format(loctor))
            raise e

    # 等待元素存在
    def wait_eleExists(self, locator, by=By.XPATH, wait_times=40):

        if by not in By.__dict__.values():
            P_log.error("定位类型[  {0}  ]不在支持类型内。请修改定位类型。".format(by))
            raise InvalidSelectorException
        # 开始时间
        t1 = time.time()
        try:
            WebDriverWait(self.driver, wait_times, 1).until(EC.presence_of_element_located((by, locator)))
            t2 = time.time()
            # 结束时间 - 两者之差就是真正的等待时间
            P_log.info("等待时间长为:{0}".format(t2 - t1))
        except TimeoutException as e:
            P_log.error("等待元素存在超时.截取当前页面。")
            self.save_picture('等待元素存在失败')
            # 抛出异常
            raise e
        except InvalidSelectorException as e:
            P_log.error("元素定位表达式：{0}  不正确，请修正".format(locator))

        # 模拟鼠标悬停操作
    def move_mouse(self, locator, by=By.CSS_SELECTOR, wait_times=40, type="visible"):
        if type == "visible":
            P_log.info("开始等待元素在当前页面可见。")
            self.wait_eleVisible(locator, by, wait_times)
        else:
            P_log.info("开始等待元素在当前页面存在。")
            self.wait_eleExists(locator, by, wait_times)

        try:
            P_log.info("=====鼠标悬停操作======")
            em = self.find_element(locator, by)
            ActionChains(self.driver).move_to_element(em).perform()

        except Exception as e:
            R_log.error("鼠标悬停操作失败,失败原因{0}".format(e))
            raise e
        # 查找元素 - 一个元素

    def find_element(self, locator, by=By.XPATH, wait_times=40, type="visible"):
        '''
        :param locator: 元素定位的表达式
        :param by: 元素的定位类型，如id，xpath，name等
        :param wait_times: 等待元素出现或者存在的时长。默认为40s
        :param type: 等待的条件类型。是可见还是元素存在。
                    默认值为visible.目前只考虑可见和存在两种情况 。
        :return: 返回WebElement元素对象。
        '''
        P_log.info("当前元素定位类型：{0}，当前查找的元素表达式为：{1}".format(by, locator))
        if type == "visible":
            P_log.info("开始等待元素在当前页面可见。")
            self.wait_eleVisible(locator, by, wait_times)
        else:
            P_log.info("开始等待元素在当前页面存在。")
            self.wait_eleExists(locator, by, wait_times)
        try:
            ele = self.driver.find_element(by, locator)
            return ele
        except NoSuchElementException as e:
            P_log.error("元素查找失败，找不到该元素。开始截取当前页面图像：")
            self.save_picture("查找元素失败")
            raise e

        # 查找多个元素

    def find_elements(self, locator, by=By.XPATH, wait_times=40, type="visible"):
        P_log.info("查找一组元素。元素定位类型：{0}，查找的元素表达式为：{1}".format(by, locator))
        if type == "visible":
            P_log.info("开始等待元素在当前页面可见。")
            self.wait_eleVisible(locator, by, wait_times)
        else:
            P_log.info("开始等待元素在当前页面存在。")
            self.wait_eleExists(locator, by, wait_times)
        try:
            eles = self.driver.find_elements(by, locator)
            return eles
        except Exception as e:
            P_log.error("元素查找失败。找不到与表达式 {0} 匹配的元素。")
            self.save_picture("查找元素集合失败")
            raise e

        # 获取当前页面的url

    def get_url(self):
        return self.driver.current_url

        # 滚动到可见区域

    def scroll_intoView(self, ele):
        P_log.info("将元素滚动到可见区域。")
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)

    # 元素的点击操作
    def click(self, locator, by=By.XPATH, wait_times=40, type="visible", scroll=False):
        P_log.info("=====执行点击事件======")
        ele = self.find_element(locator, by, wait_times, type)
        if scroll is True:
            self.scroll_intoView(ele)
        try:
            ele.click()
        except Exception as e:
            P_log.error("点击操作失败。")
            self.save_picture("点击失败")
            raise e

    # 元素的点击操作
    def double_click(self, locator, by=By.XPATH, wait_times=40, type="visible", scroll=False):
        P_log.info("=====执行双击事件======")
        ele = self.find_element(locator, by, wait_times, type)
        if scroll is True:
            self.scroll_intoView(ele)
        try:
            ele.double_click()
        except Exception as e:
            P_log.error("双击操作失败。")
            self.save_picture("双击失败")
            raise e

    # 元素组点击操作
    def clicks(self, locator, by=By.XPATH, wait_times=40, type="visible", index=0,scroll=False):
        P_log.info("=====执行点击事件======")
        eles = self.find_elements(locator, by,wait_times, type)[index]
        if scroll is True:
            self.scroll_intoView(eles)
        try:
            eles.click()
        except Exception as e:
            P_log.error("元素点击失败")
            self.save_picture("点击失败")
            raise e
    # 输入文字
    def input_text(self, locator, text, by=By.XPATH, wait_times=40, type="visible", scroll=False):
        '''
        :param locator:元素定位
        :param text:输入文本
        :param by:定位方法
        :param wait_times:等待时长
        :param type:等待元素类型
        :param scroll:是否滚动至元素可见
        :return:
        '''
        P_log.info("=====执行输入操作======\n输入的数据为：{0}".format(text))
        ele = self.find_element(locator, by, wait_times, type)
        if scroll is True:
            self.scroll_intoView(ele)
        try:
            ele.send_keys(text)
        except Exception as e:
            P_log.error("输入操作失败。")
            self.save_picture("输入文本失败")
            raise e

    #多元素选择输入
    def input_text_m(self,locator,text,by=By.XPATH,wait_times=40,type="visible",scroll=False,index=0):
        P_log.info("=====执行输入操作======\n输入的数据为：{0}".format(text))
        ele = self.find_elements(locator, by, wait_times, type)[index]
        if scroll is True:
            self.scroll_intoView(ele)
        try:
            ele.send_keys(text)
        except Exception as e:
            P_log.error("输入操作失败。")
            self.save_picture("输入文本失败")
            raise e


    # 获取对象的文字
    def get_text(self, locator, by=By.XPATH, wait_times=40, type="visible", scroll=False):
        P_log.info("=====获取元素的文本内容======")
        ele = self.find_element(locator, by, wait_times, type)
        if scroll is True:
            self.scroll_intoView(ele)
        try:
            return ele.text
        except Exception as e:
            P_log.error("获取元素的文本内容失败：")
            self.save_picture("获取元素文本信息失败")
            raise e

    #多元素获取对象的文字
    def get_text_m(self,locator,by=By.XPATH, wait_times=40, type="visible",scroll=False,index=0):
        P_log.info("=====获取元素的文本内容======")
        ele = self.find_elements(locator, by, wait_times, type)[index]
        if scroll is True:
            self.scroll_intoView(ele)
        try:
            return ele.text
        except Exception as e:
            P_log.error("获取元素的文本内容失败：")
            self.save_picture("获取元素文本信息失败")
            raise e

    # 获取元素的属性值
    def get_element_attribute(self, locator, atrribute_name, by=By.XPATH, wait_times=40, type="visible",
                              scroll=False):
        P_log.info("=====获取元素的属性值：{0}".format(atrribute_name))
        ele = self.find_element(locator, by, wait_times, type)
        if scroll is True:
            self.scroll_intoView(ele)
        try:
            return ele.get_attribute(atrribute_name)
        except Exception as e:
            P_log.error("获取属性值失败：")
            self.save_picture("取元素属性失败")
            raise e



    # 处理alert弹出框
    def alert_handler(self, action="accept"):
        # 等待alert出现 #
        WebDriverWait(self.driver, 10, 1).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        message = alert.text
        if action == "accept":
            alert.accept()
        else:
            alert.dismiss()
        return message

    # 截图函数
    def save_picture(self, doc, flag=True):
        '''
        :param doc: 截图的名称
        :return: pic_path
        '''
        if sys.platform == 'win32':
            file_dir = '\\{0}_screenshots_dir'.format(time.strftime('%Y-%m-%d'))
            filepath = screenshots_dir + file_dir
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            pic_path = filepath + "\\{0}-{1}.png".format(doc, time.strftime('%Y-%m-%d_%H_%M_%S'))
            self.driver.save_screenshot(pic_path)
            P_log.info("已截取当前页面，文件路径：{0}".format(pic_path))
        else:
            file_dir = '/{0}_screenshots_dir'.format(time.strftime('%Y-%m-%d'))
            filepath = screenshots_dir + file_dir
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            pic_path = filepath + "/{0}-{1}.png".format(doc, time.strftime('%Y-%m-%d_%H_%M_%S'))
            self.driver.save_screenshot(pic_path)
            P_log.info("已截取当前页面，文件路径：{0}".format(pic_path))

        return pic_path

    def switch_window(self):
        pass

    def switch_iframe(self):
        pass

    #页面刷新
    def refresh(self):
        return self.driver.refresh()


