#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/1 11:34
# @File     : test_system.py
# @Project  : integration-tests-insight

import allure
import pytest

from test_case.common.do_excel import DoExcel
from common import request

case_data = DoExcel(csv_dir='test_case.csv').get_cases_do_csv()


class Test_system:
    #

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['System'])
    def test_system(self, feature, story, method, url, title, data, SystemData):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        if feature == '公用接口' and story not in ['加载处理失败的消息', '重新发送失败的消息']:
            pass
        else:
            response = request.Resp(path=url, method=method, body=body)
            assert response['msg'] == eval(data)['msg']


class Test_globalSearch:
    # 全局搜索

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['globalSearch'])
    def test_globalSearch(self, feature, story, method, url, title, data, globalSearch):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)
        if title == '全局搜索':
            for i in globalSearch[0]:
                body['type'] = i['code']
                request.get_params(url, params=body, headers=globalSearch[1])

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_gsp_history:
    # gsp 历史库存

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['gsp_history'])
    def test_gsp_history(self, feature, story, method, url, title, data, gsp_history):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_hospital:
    # 医院

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['hospital'])
    def test_gsp_history(self, feature, story, method, url, title, data, hospital):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title == '根据id获取医院院区详情':
            url = url.format(id=request.hospital_id)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_upload:
    # 导入

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['upload'])
    def test_upload(self, feature, story, method, url, title, data):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        response = request.Resp(path=url, method=method, file_name=eval(data)['file'])

        assert response['msg'] == eval(data)['msg']


class Test_jpush:
    # 保存alias

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['jpush'])
    def test_upload(self, feature, story, method, url, title, data, jpush):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_message:
    # 获取消息

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['message'])
    def test_message(self, feature, story, method, url, title, data, message):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_usersPermissions:
    # 用户

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['usersPermissions'])
    def test_usersPermissions(self, feature, story, method, url, title, data, usersPermissions):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if story in ['更新用户信息', '根据id获取用户详情']:
            url = url.format(id=usersPermissions[0])
        elif story in ['更新角色信息', '根据id获取角色详情']:
            url = url.format(id=usersPermissions[1])
        elif story in ['更新权限信息', '根据id获取权限详情']:
            url = url.format(id=usersPermissions[2])
        elif story in ['根据医院查询用户的权限', '根据医院查询菜单']:
            url = url.format(hospitalId=request.hospital_id)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['usersPermissions_01'])
    def test_usersPermissions_01(self, feature, story, method, url, title, data, usersPermissions_01):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_printer:
    # 获取消息

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['printer'])
    def test_printer(self, feature, story, method, url, title, data, printer):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']
