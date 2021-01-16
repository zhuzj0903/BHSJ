#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author : Zhuzj
# @file : conftest.py
# @time : 2020/10/10 17:45
# @Software :PyCharm


import pytest
from selenium import webdriver
from PageObjects.login.login import login
from Common import dir_config
from Common.read_config import Read_Config as R
from py._xmlgen import html
import sys




#从配置文件中获取测试数据，和html配置数据
datas = R(dir_config.config_dir,'url.yaml').read_yaml()
htmls = R(dir_config.config_dir,'html.yaml').read_yaml()


#定义全局的driver

driver = None


#定义一个初始化web的fixture
@pytest.fixture()
def init_web():
    global driver
    if sys.platform =='win32':
        # driver = webdriver.Chrome()
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        driver = webdriver.Chrome()
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--isable-gpu')
        options.add_argument('--no-sandbox')
        #chromedriver放在了ubuntu中绝对路径下面
        driver = webdriver.Chrome('/home/ubuntu/Documents/chromedriver',options=options)
    driver.maximize_window()
    driver.get(datas['url'])
    yield driver
    driver.quit()



#定义一个登录好系统的fixture
@pytest.fixture()
def login_web():
    global driver
    if sys.platform =='win32':
        # driver = webdriver.Chrome()
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        driver = webdriver.Chrome()
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--isable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome('/home/ubuntu/Documents/chromedriver', options=options)
    driver.maximize_window()
    driver.get(datas['url'])
    login(driver).login_system(datas['account'],datas['pwd'])
    yield driver
    driver.quit()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """当测试失败的时候，自动截图，展示到html报告中"""
    outcome = yield
    pytest_html = item.config.pluginmanager.getplugin('html')

    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    # 如果你生成的是web ui自动化测试，请把下面的代码注释打开，否则无法生成错误截图
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):  # 失败截图
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
    extra.append(pytest_html.extras.text('some string', name='Different title'))
    report.description = str(item.function.__doc__)
    # report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")  # 解决乱码


def capture_screenshot():
    '''截图保存为base64'''
    return driver.get_screenshot_as_base64()


def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = htmls["项目名称"]
    # 删除Java_Home
    config._metadata.pop("JAVA_HOME")


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("测试任务: {0}".format(htmls["测试任务"]))])
    prefix.extend([html.p("测试人员: {0}".format(htmls["测试人员"]))])


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('描述'))
    cells.pop(-1)  # 删除link列


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.pop(-1)  # 删除link列


