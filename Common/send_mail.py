#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : send_mail.py
# @time : 2021/1/30 15:02
# @Software :PyCharm

import smtplib
import time
# 用于构建邮件内容
from email.mime.text import MIMEText
# 用于构建邮件头
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from Common import dir_config as D
from Common import read_config as R
import sys


class sendmail:
    def __init__(self, email_from, pwd, email_to, file, title='自动化测试报告', text='详情见附件，请查收！', type='163',
                 style_path='style.css'):
        """
        :param email_from: 发件人的地址
        :param pwd: 发件人邮箱密码
        :param email_to: 收件人地址，多个收件人可传入一个列表
        :param file: 附件的路径
        :param title: 邮件名称
        :param text: 邮件正文
        :param type: 使用哪个邮箱来发送邮件，默认163企业邮箱，填写其它信息默认QQ邮箱
        :param style_path: 定制化参数，针对发送html报告，同步发送css样式
        """
        self.email_from = email_from
        self.pwd = pwd
        self.email_to = email_to
        self.file = file
        self.title = title
        self.text = text
        self.type = type
        self.style_path = style_path

    def send(self):
        msg = MIMEMultipart()
        msg["Subject"] = time.strftime('%Y-%m-%d-%H-%M') + self.title
        msg["To"] = ','.join(self.email_to)
        msg["From"] = self.email_from

        # 邮件正文部分
        part = MIMEText(self.text)
        msg.attach(part)

        # 邮件附件_html报告
        part = MIMEApplication(open(self.file, 'rb').read())
        if sys.platform == 'win32':
            part.add_header('Content-Disposition', 'attachment', filename=self.file.split('\\')[-1])
        else:
            part.add_header('Content-Disposition', 'attachment', filename=self.file.split('/')[-1])
        msg.attach(part)

        # 邮件附件_html报告样式CSS
        if sys.platform == 'win32':
            old = self.file.split('\\')[-1]
        else:
            old = self.file.split('/')[-1]
        new_style_path = self.file.replace(old, self.style_path)
        part = MIMEApplication(open(new_style_path, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename='style.css')
        msg.attach(part)

        # 发送邮件
        host = 'smtp.163.com' if self.type == '163' else 'smtp.qq.com'
        if host.__contains__('163'):
            try:
                server = smtplib.SMTP_SSL(host, 994, timeout=10)
                server.login(self.email_from, self.pwd)
                server.sendmail(self.email_from, self.email_to, msg.as_bytes())
                server.close()
            except Exception as e:
                print('连接失败', e)
        else:
            try:
                server = smtplib.SMTP_SSL(host, 465, timeout=10)
                server.login(self.email_from, self.pwd)
                server.sendmail(self.email_from, self.email_to, msg.as_bytes())
                server.close()
            except Exception as e:
                print('连接失败', e)


if __name__ == '__main__':
    mes = R.Read_Config(D.config_dir, 'email.yaml').read_yaml()
    print(mes)
    file = 'C:\E\\autotest\\BHSJ\\HtmlTestReport\\2021-02-01 16-40-北京邮电大学导师门户.html'
    S = sendmail(mes['from'], mes['pwd'], mes['to'], file)
    S.send()