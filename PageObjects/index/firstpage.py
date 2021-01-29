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
import pymysql

#从配置文件中获取测试数据，和html配置数据
#datas = R(dir_config.config_dir,'mysql.yaml')



class First_Page(BasePage):
    #总览
    导师年限='//h4[text()="导师年限（年）"]/following-sibling::p'
    在读研究生='//h4[text()="在读研究生（人）"]/following-sibling::p'
    往届毕业生 = '//h4[text()="往届毕业生（人）"]/following-sibling::p'
    项目经费 = '//h4[text()="项目经费（万元）"]/following-sibling::p'
    论文总数='//h4[text()="论文总数（篇）"]/following-sibling::p'
    发明专利 = '//h4[text()="发明专利（个）"]/following-sibling::p'

    def sql_zonglan(self):#查询数据库，获取总览中每个字段的值
        server = '116.63.56.139'  # 服务器名称
        user = 'root'  # 登录名
        password = '18iBH9#8z@pure_pro;'  # 登录密码
        database = 'scibox_bupt'  # 数据库名

        conn = pymysql.connect(host=server,user=user,passwd=password,db=database,port=3306,cursorclass=pymysql.cursors.DictCursor) # 打开数据库连接
        cur = conn.cursor()  # 使用cursor()方法获取操作游标
        sql0="""select count(*) as '人数' from n109_t_js_jbxx_jbxx a inner join n109_t_js_jxqk_zdyjsqk b 
        INNER JOIN n109_t_xsjbxx c on a.uid=b.uid AND b.xh=c.xh WHERE a.gzzh='2010810769' and c.xjzt='在校'
        """#在读研究生
        sql1="""select count(*) as '专利数' from n109_t_js_jbxx_jbxx a INNER JOIN n109_t_js_kyqk_sqzlqk b on a.uid=b.uid 
        where a.gzzh='2010810769'"""#发明专利
        sql2="""SELECT sum(a.论文数+b.论文数) as '论文总数' from 
        (select count(*) as '论文数' from n109_t_js_jbxx_jbxx a 
        INNER JOIN n109_t_js_jxqk_fbjglwqk b on a.uid=b.uid where a.gzzh='2010810769') a,
        (select count(*) as '论文数' from n109_t_js_jbxx_jbxx a INNER JOIN n109_t_js_kyqk_fbkylwqk b 
        on a.uid=b.uid where a.gzzh='2010810769') b """#论文总数（篇）
        rows={}
        cur.execute(sql0)  # 使用execute方法执行SQL语句
        rows0 = cur.fetchone()  # 使用 fetchone() 方法获取一条数据
        rows['在读研究生人数']=rows0['人数']
        cur.execute(sql1)
        rows1 = cur.fetchone()  # 使用 fetchone() 方法获取一条数据
        rows['发明专利数'] = rows1['专利数']
        cur.execute(sql2)
        rows2 = cur.fetchone()  # 使用 fetchone() 方法获取一条数据
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






