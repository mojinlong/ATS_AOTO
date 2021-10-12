#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/16 15:15
# @File     : test_his.py
# @Project  : integration-tests-insight


import allure
import pytest

from test_case.common.do_excel import DoExcel
from common import request

case_data = DoExcel(csv_dir='test_case.csv').get_cases_do_csv()


class Test_medicalAdvice:

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['medicalAdvice'])
    def test_medicalAdvice(self, feature, story, method, url, title, data, medicalAdvice, surgical):
        # 医嘱收费
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_doctor:

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['doctor'])
    def test_doctor(self, feature, story, method, url, title, data, doctor):
        # 医生
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title == '根据id查询医生信息':
            url = url.format(id=1)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_patient:
    # 病人信息

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['patient'])
    def test_patient(self, feature, story, method, url, title, data, patient, unprocessedCount):
        # 病人信息
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title == '根据id查询病人信息':
            url = url.format(id=1)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']

