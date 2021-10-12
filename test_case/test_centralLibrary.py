#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/16 14:04
# @File     : test_centralLibrary.py
# @Project  : integration-tests-insight

import allure
import pytest

from test_case.common.do_excel import DoExcel
from common import request

case_data = DoExcel(csv_dir='test_case.csv').get_cases_do_csv()


class Test_deliveryOrder:
    # 推送单

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['deliveryOrder'])
    def test_deliveryOrder(self, feature, story, method, url, title, data, Delivery_01):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_processingOrder:
    # 拣货单

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['processingOrder'])
    def test_processingOrder(self, feature, story, method, url, title, data, processingOrder_01):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if story == '删除加工单':
            url = url.format(processingOrderId=processingOrder_01)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        if story == '查询要加工的手术套包中的商品':
            assert eval(data)['msg'] in response['msg']
        else:
            assert response['msg'] == eval(data)['msg']
