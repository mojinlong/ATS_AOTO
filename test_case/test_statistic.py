#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/17 20:02
# @File     : test_statistic.py
# @Project  : integration-tests-insight


import allure
import pytest

from test_case.common.do_excel import DoExcel
from common import request

case_data = DoExcel(csv_dir='test_case.csv').get_cases_do_csv()


class Test_statistic:

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['Statistic'])
    def test_statistic(self, feature, story, method, url, title, data, Statistic):
        # 报表
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']
