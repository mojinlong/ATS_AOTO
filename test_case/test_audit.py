#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/6/2 17:09 
# @Author   : 蓦然
# @File     : test_audit.py
# Project   : integration-tests-insight
import allure
import pytest, time

from test_case.common.do_excel import DoExcel
from test_config.yamlconfig import body_data
from common import request

case_data = DoExcel(csv_dir='test_case_1.csv').get_cases_do_csv()


@pytest.mark.usefixtures('b_data')
class Test_Audit:
    time_now = int(time.time() * 1000)

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['GetAudit'])
    def test_Audit(self, feature, story, method, url, title, data, audit_History, audit_getPage, creatRole):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)
        # if story == '分页查询审计记录':
        print(data)
        body = request.body_replace(url, data)
        response = request.Resp(path=url, method=method, body=body)
        assert response['msg'] == eval(data)['msg']

    # @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['role'])
    # def test_Role(self, feature, story, method, url, title, data, creatRole):
    #     allure.dynamic.title(title)
    #     allure.dynamic.feature(feature)
    #     allure.dynamic.story(story)
    #     body = request.body_replace(url, data)
    #     response = request.Resp(path=url, method=method, body=body)
    #     assert response['msg'] == eval(data)['msg']
    #     print(data)