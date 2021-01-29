#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : firstpage.py
# @time : 2020/11/18 10:38
# @Software :PyCharm

from Common.BasePage import *
from Common.log import Log
from Common import dir_config
from Common.read_config import Read_Config as R
from selenium.webdriver.common.by import By
import time
from TestDatas.北京邮电大学导师门户.首页 import zonglan_sql as sql
import pymysql

#从配置文件中获取测试数据，和mysql配置数据
D = R(dir_config.config_dir,'mysql.yaml').read_yaml()



class First_Page(BasePage):
    #总览
    导师年限='//h4[text()="导师年限（年）"]/following-sibling::p'
    在读研究生='//h4[text()="在读研究生（人）"]/following-sibling::p'
    往届毕业生 = '//h4[text()="往届毕业生（人）"]/following-sibling::p'
    项目经费 = '//h4[text()="项目经费（万元）"]/following-sibling::p'
    论文总数='//h4[text()="论文总数（篇）"]/following-sibling::p'
    发明专利 = '//h4[text()="发明专利（个）"]/following-sibling::p'

    def sql_zonglan(self):#查询数据库，获取总览中每个字段的值

        conn=pymysql.connect(host=D['server'],user=D['user'],passwd=D['password'],db=D['database'],
                             port=3306,cursorclass=pymysql.cursors.DictCursor)# 打开数据库连接
        cur = conn.cursor()  # 使用cursor()方法获取操作游标

        """获取sql语句"""
        sql0 = sql['在读研究生']
        sql1 = sql['发明专利']
        sql2 = sql['论文总数']

        rows={}  #定义一个空字典

        cur.execute(sql0)  # 执行SQL语句，获取在读研究生数量
        rows0 = cur.fetchone()
        rows['在读研究生人数']=rows0['人数']

        cur.execute(sql1) #执行SQL语句，获取发明专利数量
        rows1 = cur.fetchone()
        rows['发明专利数'] = rows1['专利数']

        cur.execute(sql2) #执行SQL语句，获取论文总数（篇）
        rows2 = cur.fetchone()
        rows['论文总数'] = rows2['论文总数']

        print(type(rows))
        conn.close()  # 关闭数据库
        return rows



    # 总览
    def get_zonglan(self):
        list =[]
        dsnx=self.get_text(self.导师年限)
        list.append(dsnx)
        zdyjs=self.get_text(self.在读研究生)
        list.append(zdyjs)
        wjbys=self.get_text(self.往届毕业生)
        list.append(wjbys)
        xmjf=self.get_text(self.项目经费)
        list.append(xmjf)
        lwzs=self.get_text(self.论文总数)
        list.append(lwzs)
        fmzl=self.get_text(self.发明专利)
        list.append(fmzl)
        return list






