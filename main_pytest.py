#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/5/10 9:05
# @File     : main_pytest.py
# @Project  : integration-tests-insight
import shutil

import pytest

# Pytest调用语句
#
# pytest.main([‘--html =./ report.html’, ‘模块.py::类::test_a_001
# '])
# 运行指定模块指定类指定用例，冒号分割，并生成测试报告
# pytest.main(['-x', '--html=./report.html', 't12est000.py'])
# # -x出现一条测试用例失败就退出测试
# - v: 丰富信息模式, 输出更详细的用例执行信息
#              - s: 显示print内容
#                   - q: 简化结果信息，不会显示每个用例的文件名
#
# Pytest的运行方式
#     .点号，表示用例通过　　　　　　　　　　　　　
# F
# 表示失败
# Failure
# E
# 表示用例中存在异常
# Error

# Pytest和allure结合生成html格式的测试报告
# # 生成测试报告json
# pytest.main(['--alluredir', 'report/result',
#              'test001.py'])   ## 将测试报告转为html格式   --html=../report.htmlsplit = 'allure ' + 'generate ' + './report/result ' + '-o ' + './report/html ' + '--clean'os.system(split)#system函数可以将字符串转化成命令在服务器上运行


if __name__ == '__main__':
    # pytest.main(["-s","-v","--html=Outputs/reports/pytest.html"])

    pytest.main(['test_case', '--alluredir', 'outputs/allure_reports'])

    shutil.copyfile('outputs/environment.properties', 'outputs/allure_reports/environment.properties')

    #
#   allure serve outputs/allure_reports  # test_case/test_baseData.py


# pip install Pyinstaller -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
