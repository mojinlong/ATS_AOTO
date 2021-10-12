#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/9 17:07
# @File     : test_finance.py
# @Project  : integration-tests-insight

import allure
import pytest

from test_case.common.do_excel import DoExcel
from common import request

case_data = DoExcel(csv_dir='test_case.csv').get_cases_do_csv()


class Test_invoice_01:

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['invoice_sync'])
    def test_invoice_sync(self, feature, story, method, url, title, data, invoice_01):
        # 发票管理货票同行蓝票
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)
        if '导出' in story and '发票失败' in title:
            body['invoiceTypeList'] = eval(data)['invoiceTypeList']

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['invoice_finStates'])
    def test_invoice_finStates(self, feature, story, method, url, title, data, invoice_02):
        # 销后结算
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['invoice_Manual'])
    def test_invoice_Manual(self, feature, story, method, url, title, data, invoiceManual):
        # 红冲发票
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        if story == '根据发票查询发票明细':
            body['invoiceId'] = invoiceManual

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_statement:
    # 结算单

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['statement'])
    def test_statement(self, feature, story, method, url, title, data, statement):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)
        if title == '导出结算单失败':
            body['fewfea'] = eval(data)['fewfea']

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_cost_invoicing:
    # 成本中心——进销存

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['cost_invoicing'])
    def test_statement(self, feature, story, method, url, title, data, cost_invoicing):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']
