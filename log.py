#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : log.py
# @time : 2020/10/10 17:37
# @Software :PyCharm

'''
日志模块,定义两个输出目录，分别记录两个log，processlog及resultlog
分别记录用例的执行过程，以及用例的执行结果
'''
import logging
import os
import time
from Common import dir_config


class Log:

    def __init__(self, log_path, name='processlog'):
        if 'processlog' in log_path:
            self.logname = os.path.join(log_path, '{0}-{1}.log'.format(name, time.strftime('%Y-%m-%d')))
        else:
            name = 'resultlog'
            self.logname = os.path.join(log_path, '{0}-{1}.log'.format(name, time.strftime('%Y-%m-%d')))

    def __printconsole(self, level, message):
        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.logname, 'a+', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        if self.logname.__contains__('processlog'):
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -[步骤信息]:%(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -[结果信息]:%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        # 记录一条日志
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__printconsole('debug', message)

    def info(self, message):
        self.__printconsole('info', message)

    def warning(self, message):
        self.__printconsole('warning', message)

    def error(self, message):
        self.__printconsole('error', message)


if __name__ == '__main__':
    logger = Log(dir_config.processlog_dir)
    logger.info('查找元素中===')
    logger_1 = Log(dir_config.resultlog_dir)
    logger_1.info('passed')
