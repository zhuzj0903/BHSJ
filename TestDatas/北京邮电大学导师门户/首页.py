#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : 首页.py
# @time : 2021/1/29 17:33
# @Software :PyCharm

zonglan_sql={'导师年限':'',

             '在读研究生':"select count(*) as '人数' from n109_t_js_jbxx_jbxx a inner join n109_t_js_jxqk_zdyjsqk b "
                r"INNER JOIN n109_t_xsjbxx c on a.uid=b.uid AND b.xh=c.xh WHERE a.gzzh='2010810769' and c.xjzt='在校'",

             "往届毕业生":"select count(*) as '人数' from n109_t_js_jbxx_jbxx a inner join n109_t_js_jxqk_zdyjsqk b "
                     r"INNER JOIN n109_t_xsjbxx c on a.uid=b.uid AND b.xh=c.xh WHERE a.gzzh='2010810769' and c.xjzt='存档'",

             "项目经费":"select sum(brkzpjf) from n109_t_js_jbxx_jbxx a inner join n109_t_js_kyqk_cdkyxmqk b "
                    "on a.uid=b.uid WHERE a.gzzh='138784'and b.xmwcqk='进行'",

             "论文总数":"SELECT sum(a.论文数+b.论文数) as '论文总数' from (select count(*) as '论文数' from n109_t_js_jbxx_jbxx a "
                    "INNER JOIN n109_t_js_jxqk_fbjglwqk b on a.uid=b.uid where a.gzzh='2010810769') a,"
                    "(select count(*) as '论文数' from n109_t_js_jbxx_jbxx a INNER JOIN n109_t_js_kyqk_fbkylwqk b "
                    "on a.uid=b.uid where a.gzzh='2010810769') b ",

             "发明专利":"select count(*) as '专利数' from n109_t_js_jbxx_jbxx a INNER JOIN n109_t_js_kyqk_sqzlqk b "
                    "on a.uid=b.uid where a.gzzh='2010810769'"}