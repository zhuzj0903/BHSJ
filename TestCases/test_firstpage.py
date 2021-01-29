#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : test_firstpage.py
# @time : 2021/1/16 16:15
# @Software :PyCharm

import pytest
from Common.log import Log
from Common import dir_config
from PageObjects.index.firstpage import First_Page
from Common.read_config import Read_Config as R

#从配置文件中获取测试数据，和html配置数据
datas = R(dir_config.config_dir,'mysql.yaml')

#定义resultlog和processlog
P_log = Log(dir_config.processlog_dir)
R_log = Log(dir_config.resultlog_dir)

@pytest.mark.usefixtures("login_web")
class Test_firstpage:
    def test_zonglan(self,login_web):
        P_log.info("*********开始执行总览数据校验********")
        r=First_Page(login_web).get_zonglan()
        s=First_Page(login_web).sql_zonglan()
        try:
            P_log.info('获取到的导师年限为：{0}'.format(r[0]))
            P_log.info('获取到的在读研究生为：{0}'.format(r[1]))
            P_log.info('获取到的往届毕业生为：{0}'.format(r[2]))
            P_log.info('获取到的项目经费为：{0}'.format(r[3]))
            P_log.info('获取到的论文总数为：{0}'.format(r[4]))
            P_log.info('获取到的发明专利为：{0}'.format(r[5]))
            P_log.info('数据库中在读研究生人数为：{0}'.format(s['在读研究生人数']))
            P_log.info('数据库中发明专利数为：{0}'.format(s['发明专利数']))
            P_log.info('数据库中论文总数为：{0}'.format(s['论文总数']))
            #研究生人数校验
            # P_log.info("*********开始进行在读研究生人数校验********")
            # assert r[1] == s['在读研究生人数']
            # P_log.info("*********在读研究生人数校验成功********")
            #论文总数校验
            # P_log.info("*********开始进行论文总数校验********")
            # assert r[4] == s['论文总数']
            # P_log.info("*********论文总数校验成功********")
            #发明专利数校验
            P_log.info("*********开始进行发明专利数校验********")
            assert r[5] == str(s['发明专利数'])
            P_log.info("*********发明专利数校验成功********")
            R_log.info("*********总览数据校验成功********")
        except Exception as e:
            P_log.info("总览数据校验失败，失败原因：{0}".format(e))
            R_log.info("总览数据校验失败")
            First_Page(login_web).save_picture('用例异常截图')
            raise e


if __name__=="__main__":
        pytest.main(["-q","test_firstpage.py"])
