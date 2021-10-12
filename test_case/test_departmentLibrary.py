#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/5/31 17:50
# @File     : test_departmentLibrary.py
# @Project  : integration-tests-insight

import allure
import pytest

from test_case.common.do_excel import DoExcel
from common import request

case_data = DoExcel(csv_dir='test_case.csv').get_cases_do_csv()


@pytest.mark.usefixtures('b_data')
class Test_goodsRequest:
    # 科室库普通请领

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['goodsRequest_01'])
    def test_goodsRequest_01(self, feature, story, method, url, title, data, goodsR):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title == '请领单id为空':
            body = request.body_replace(url, data, id=1)
        elif title == '物资id为空':
            body = request.body_replace(url, data, id=2)
        else:
            body = request.body_replace(url, data)
        if story == '修改普通请领' and title == '商品id为空':
            body['id'] += 1
            body['warehouseId'] += 1
        elif story == '请领审核' and (title == '物资数量为0' or title == '审核不通过'):
            body['id'] -= 2
        elif story == '请领复核' and (title == '物资数量为0' or title == '审核不通过'):
            body['id'] += 1

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['goodsRequest_02'])
    def test_goodsRequest_02(self, feature, story, method, url, title, data, goodsR_remove):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_acceptance:
    # 科室库验收

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['acceptance_Check_01'])
    def test_acceptance(self, feature, story, method, url, title, data, acceptance_Check_01):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_logicStockTakingOrder:
    # 逻辑库盘库

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['logicStockTakingOrder'])
    def test_logicStockTakingOrder(self, feature, story, method, url, title, data, logicStockTakingOrder):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title in ['删除逻辑库盘库单', '逻辑库盘库单审核通过', '查询逻辑库盘库单', '打印逻辑库盘库单']:
            url = url.format(id=logicStockTakingOrder)

        body = request.body_replace(url, data)

        if title == '提交逻辑库盘库单':
            body['id'] = logicStockTakingOrder

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_logicStockOperation_logicStock:
    # 逻辑库库存日志 & 逻辑库库存日志

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['logicStockOperation_logicStock'])
    def test_logicStockOperation_logicStock(self, feature, story, method, url, title, data,
                                            logicStockOperation_logicStock):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_pickOrder:
    # 拣货单

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['pickOrder'])
    def test_pickOrder(self, feature, story, method, url, title, data, pickOrder_01):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title in ['重复取消拣货单', '提前完成拣货单']:
            url = url.format(pickOrderId=pickOrder_01)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']
