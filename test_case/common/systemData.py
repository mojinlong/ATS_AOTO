#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/1 10:31
# @File     : systemData.py
# @Project  : integration-tests-insight
import pprint

import request
import requests
from test_config import param_config


class Login:

    def verify_login(self):
        # 判断是否已登录
        body = {}
        request.post_body('/api/admin/login/web/1.0/verify_login', body=body)

    def login(self, loginPhone, loginPassword):
        api_url = param_config.api_url

        payload = {
            'loginPassword': loginPassword,
            'loginPhone': loginPhone
        }
        r = requests.post(api_url + '/api/admin/login/web/1.0/login', data=payload, verify=False)
        try:
            assert r.json()['code'] == 0
        except Exception:
            raise Exception(r.json())
        hospital_name = r.json()['data']['hospitals'][0]['name']
        hospital_id = r.json()['data']['hospitals'][0]['id']
        token = r.headers['X-AUTH-TOKEN']
        # headers
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-TOKEN': token
        }
        return headers


class dictionary:
    # 词典

    def list(self):
        # 查询所有字典数据
        request.get('/api/admin/dictionary/1.0/list')

    def getDictByCategory(self):
        # 查询某个字典类别
        params = {
            'category': 'user_role_type'
        }
        request.get_params('/api/admin/dictionary/1.0/getDictByCategory', params=params)

    def getByCategory(self):
        # 根据字典类型查询某个字典类别
        params = {
            'category': 'user_role_type'
        }
        request.get_params('/api/admin/dictionary/1.0/getByCategory', params=params)

    def listDictAllCategory(self):
        # 查询所有字典类别
        request.get('/api/admin/dictionary/1.0/listDictAllCategory')

    def getDictLabelAllCategory(self):
        # 查询所有字典类别(返回id和name)
        request.get('/api/admin/dictionary/1.0/getDictLabelAllCategory')

    def getDictAllCategory(self):
        # 查询所有字典类别(返回name和value)
        request.get('/api/admin/dictionary/1.0/getDictAllCategory')


class districts:
    # 地区

    def listProvinces(self):
        # 获取所有省份
        request.get('/api/admin/districts/1.0/listProvinces')

    def listChildren(self):
        # 根据areaCode获取下级区域
        params = {
            'areaCode': 110000000000
        }
        request.get_params('/api/admin/districts/1.0/listChildren', params=params)

    def listSiblings(self):
        # 根据areaCode获取同级区域
        params = {
            'areaCode': 110000000000
        }
        request.get_params('/api/admin/districts/1.0/listSiblings', params=params)

    def getParentPaths(self):
        # 按顺序返回areaCode父层区域路径
        params = {
            'areaCode': 110000000000
        }
        request.get_params('/api/admin/districts/1.0/getParentPaths', params=params)


class batchApproval:
    # 一键审批
    def oneClick(self):
        # 一键审批
        request.post('/api/admin/batchApproval/1.0/oneClick')


class captcha:
    # 验证码

    def get(self):
        # 获取验证码
        request.get('/api/admin/captcha/1.0/get')

    def check(self):
        # 验证验证码
        params = {
            'captchaCode': 'captchaCode'
        }
        request.get_params('/api/admin/captcha/1.0/check', params)


class category:
    # 物资类别管理

    def getAll12(self):
        # 查询所有2012类别
        request.get('/api/admin/category/1.0/getAll12')

    def getAll18(self):
        # 查询所有2018类别
        request.get('/api/admin/category/1.0/getAll18')


class config:
    # 配置

    def list(self):
        # 配置列表，可根据查询条件
        request.get('/api/admin/config/1.0/list')

    def fields(self):
        # config 可选择字段
        request.get('/api/admin/config/1.0/fields')


class common:
    # 公共接口

    def autoGenerateProcessingOrder(self):
        # 自动生成加工单
        request.get_notResp('/api/admin/common/1.0/autoGenerateProcessingOrder')

    def autoGeneratePurchasePlan(self):
        # 测试触发生成计划
        request.get_notResp('/api/admin/common/1.0/autoGeneratePurchasePlan')

    def autoGenerateStatement(self):
        # 自动生成结算单
        request.get_notResp('/api/admin/common/1.0/autoGenerateStatement')

    def autoGeneratePickPendingOrder(self):
        # 自动波次
        request.get_notResp('/api/admin/common/1.0/autoGeneratePickPendingOrder')

    def autoGenerateHistoryInventory(self):
        # 自动生成历史库存
        request.get_notResp('/api/admin/common/1.0/autoGenerateHistoryInventory')

    def autoCheckDepartmentReturnGoods(self):
        # 自动检查部门退货
        request.get_notResp('autoCheckDepartmentReturnGoods')

    def loadMessageRecord(self):
        # 加载处理失败的消息
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/common/1.0/loadMessageRecord', params=params)

    def redeliveryMessage(self):
        # 重新发送失败的消息
        body = {
            "messagingIdList": [
                "in",
                "sed"
            ]
        }
        request.post_body('/api/admin/common/1.0/redeliveryMessage', body=body)


class print_api:
    # 打印服务

    def loadPrintingData(self):
        # 加载打印信息
        params = {
            'id': 123,
            'type': 'goods_code'
        }
        request.get_params('/api/admin/print/1.0/loadPrintingData', params=params)

    def batchLoadPrintingData(self):
        # 批量加载打印信息
        params = {
            'ids': 123,
            'type': 'goods_code'
        }
        request.get_params('/api/admin/print/1.0/batchLoadPrintingData', params=params)

    def printSuccess(self):
        # 标记打印成功
        params = {
            'id': 123,
            'type': 'goods_code'
        }
        request.get_params('/api/admin/print/1.0/printSuccess', params=params)


class globalSearch:
    # 全局搜索

    def searchTypeList(self):
        """
        获取查询类型列表
        :return:
        """
        response = request.get('/api/admin/globalSearch/1.0/searchTypeList')

        return response['data']

    def search(self, type='GOODS_BARCODE', keywords='0'):
        """
        获取查询类型列表
        :return:
        """
        params = {
            "keywords": keywords,
            "pageNum": 0,
            "pageSize": 50,
            "type": type
        }
        request.get_params('/api/admin/globalSearch/1.0/search', params=params)

    def goodsLife(self, barcode='ID_0001_0210_10352'):
        """
        根据条码查询商品生命周期
        :return:
        """
        params = {
            "barcode": barcode
        }
        request.get_params('/api/admin/globalSearch/1.0/goodsLife', params=params)

    def goodsItemLife(self, barcode='ID_0001_0210_10352'):
        """
        根据条码查询商品生命周期
        :return:
        """
        params = {
            "barcode": barcode
        }
        request.get_params('/api/admin/globalSearch/1.0/goodsItemLife', params=params)

    def gs1Decoding(self, gs1='0'):
        """
        根据条码查询商品生命周期
        :return:
        """
        params = {
            "gs1": gs1
        }
        request.get_params('/api/admin/globalSearch/1.0/gs1Decoding', params=params)


class gsp:
    # 首页GSP提醒接口

    def goodsRegisterRemindList(self):
        """
        产品注册证提醒
        :return:
        """
        request.get('/api/admin/gsp/1.0/goodsRegisterRemindList')

    def companyLicenseRemindList(self):
        """
        企业证照提醒
        :return:
        """
        request.get('/api/admin/gsp/1.0/companyLicenseRemindList')


class history:
    # 历史库存

    def list(self):
        # 获取商品历史库存列表
        params = {
            "pageNum": 0,
            "pageSize": 50,
        }
        request.get_params('/api/admin/history/1.0/list', params=params)

    def listByPackageBulk(self):
        # 获取定数包历史库存列表
        params = {
            "pageNum": 0,
            "pageSize": 50,
        }
        request.get_params('/api/admin/history/1.0/listByPackageBulk', params=params)

    def listByPackageSurgical(self):
        # 获取手术套包历史库存列表
        params = {
            "pageNum": 0,
            "pageSize": 50,
        }
        request.get_params('/api/admin/history/1.0/listByPackageSurgical', params=params)


class jpush:

    def save(self):
        """
        保存alias
        :return:
        """
        body = {
            "jpushAlias": "magna laboris"
        }
        request.post_body('/api/admin/jpush/1.0/save', body=body)


class message:
    # 获取消息

    def pull(self):
        """
        weChat拉取数据
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/message/1.0/pull', params=params)

    def pullMessage(self):
        """
        pullMessage拉取数据
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/message/1.0/pullMessage', params=params)

    def unRead(self):
        """
        获得未读消息
        :return:
        """
        params = {
            "count": 1,
            "page": 1
        }
        request.get_params('/api/admin/message/1.0/unRead', params=params)

    def doHander(self):
        """
        操作消息
        :return:
        """
        params = {
            "id": 1
        }
        request.post_params('/api/admin/message/1.0/doHander', params=params)

    def doRead(self):
        """
        消息改变未读为已读(批量)
        :return:
        """
        request.post('/api/admin/message/1.0/doRead')

    def list(self):
        """
        分页获取消息列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/message/1.0/list', params=params)

    def loadMessageTypeByUser(self):
        """
        获取用户消息类型
        :return:
        """
        request.get('/api/admin/message/1.0/loadMessageTypeByUser')

    def doBatchRead(self):
        """
        根据id设置消息已读
        :return:
        """
        body = {
            "ids": [
                1
            ]
        }
        request.post_body('/api/admin/message/1.0/doBatchRead', body=body)

    def doBatchDelete(self):
        """
        根据id批量删除消息
        :return:
        """
        body = {
            "ids": [
                1
            ]
        }
        request.post_body('/api/admin/message/1.0/doBatchDelete', body=body)

    def single(self):
        """
        获取最新一条未读消息
        :return:
        """
        request.get('/api/admin/message/1.0/single')

    def fetchLatestMessage(self):
        """
        获取前rank条消息
        :return:
        """
        params = {
            "rank": 10
        }
        request.get_params('/api/admin/message/1.0/fetchLatestMessage', params=params)

    def getMessageAndPermission(self):
        """
        获取消息和权限信息
        :return:
        """
        request.get('/api/admin/message/1.0/getMessageAndPermission')

    def addMessageAndPermission(self):
        """
        新增消息和权限的信息
        :return:
        """
        body = {
            "createdBy": -63928314,
            "hospitalId": 43578284,
            "id": -812834,
            "messageType": 46621003,
            "permissionIds": [
                28543062,
                64117237
            ]
        }
        request.post_body('/api/admin/message/1.0/addMessageAndPermission', body=body)

    def updateMessageAndPermission(self):
        """
        更新权限列表
        :return:
        """
        body = {
            "createdBy": -46634946,
            "hospitalId": -92344626,
            "id": -77218096,
            "messageType": 88712882,
            "permissionIds": [
                25588885,
                12518746
            ]
        }
        request.put_body('/api/admin/message/1.0/updateMessageAndPermission', body=body)

    def deleteMessageAndPermission(self):
        """
        根据id删除用户的权限信息
        :return:
        """
        body = {
            "ids": [
                -33840244,
                78078044
            ]
        }
        request.put_body('/api/admin/message/1.0/deleteMessageAndPermission', body=body)


class users:
    # 用户

    def add(self, code):
        """
        新增用户
        :return:
        """
        name = 'test' + code
        body = {
            "type": "operator",
            "roleIds": [167],
            "name": name,
            "loginPhone": name,
            "contactId": [None]
        }
        request.post_body('/api/admin/users/1.0', body=body)

        return name

    def get_id(self, id):
        """
        根据id获取用户详情
        :return:
        """
        response = request.get('/api/admin/users/1.0/{id}'.format(id=id))

        return response['data']

    def editUser(self, id):
        """
        更新用户信息
        :return:
        """
        data = self.get_id(id)

        body = {
            "type": data['roles'][0]['type'],
            "roleIds": [data['roles'][0]['id']],
            "name": data['roles'][0]['name'],
            "loginPhone": data['loginPhone'],
            "contactId": [data['contactIds']]
        }
        request.put_body('/api/admin/users/1.0/{id}'.format(id=id), body=body)

    def usersPageList(self, loginPhone=None):
        """
        获取用户列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "loginPhone": loginPhone
        }
        response = request.get_params('/api/admin/users/1.0', params=params)

        return response['data']['rows'][0]['id']

    def operate(self, id):
        """
        启用/禁用
        :return:
        """
        body = {
            "id": id,
            "enable": True
        }
        request.post_body('/api/admin/users/1.0/operate', body=body)

    def listByRoleId(self):
        """
        根据角色Id获取用户列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "roleId": 1
        }
        request.get_params('/api/admin/users/1.0/listByRoleId', params=params)

    def listByDepartmentId(self):
        """
        根据组织Id获取用户列表，如果为中心库绑定的科室，则查询中心库和该科室的所有人员
        :return:
        """
        params = {
            "departmentId": 1
        }
        request.get_params('/api/admin/users/1.0/listByDepartmentId', params=params)

    def updatePwd(self, oldPassword, newPassword):
        """
        修改密码
        :return:
        """
        body = {
            "newPassword": newPassword,
            "oldPassword": oldPassword
        }
        request.put_body('/api/admin/users/1.0/updatePwd', body=body)

    def adminUpdatePwd(self, userId):
        """
        重置密码
        :return:
        """
        body = {
            "userId": userId
        }
        request.put_body('/api/admin/users/1.0/adminUpdatePwd', body=body)

    def getPickerList(self):
        """
        查询拣货员列表
        :return:
        """
        request.get('/api/admin/users/1.0/getPickerList')

    def getPusherList(self):
        """
        查询推送员列表
        :return:
        """
        request.get('/api/admin/users/1.0/getPusherList')

    def getUserBaseInfo(self, userId):
        """
        查询用户基本信息
        :return:
        """
        params = {
            "userId": userId
        }
        request.get_params('/api/admin/users/1.0/getUserBaseInfo', params=params)


class role:
    # 角色

    def add(self, code):
        """
        新增角色
        :return:
        """
        name = 'test' + code
        body = {
            "name": name,
            "code": code,
            "type": "operator",
            "permissionIds": [370],
            "isSystemDefined": False
        }
        request.post_body('/api/admin/role/1.0', body=body)

        return name

    def get_id(self, id):
        """
        根据id获取角色详情
        :return:
        """
        response = request.get('/api/admin/role/1.0/{id}'.format(id=id))

        return response['data']

    def editRole(self, id):
        """
        更新角色信息
        :return:
        """
        data = self.get_id(id)

        body = {
            "name": data['name'],
            "code": data['code'],
            "type": data['type'],
            "permissionIds": [data['permissions'][0]['id']],
            "remark": data['permissions'][0]['remark'],
            "id": id,
            "isSystemDefined": data['isSystemDefined']
        }
        request.put_body('/api/admin/role/1.0/{id}'.format(id=id), body=body)

    def operate(self, id, type=1):
        """
        启用/禁用
        :return:
        """
        body = {
            "id": id,
            "type": type
        }
        request.post_body('/api/admin/role/1.0/operate', body=body)

    def pageList(self, name):
        """
        分页获取角色列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "name": name
        }
        response = request.get_params('/api/admin/role/1.0/pageList', params=params)

        return response['data']['rows'][0]['id']

    def listByTypeAndHospitalId(self):
        """
        根据type获取角色列表
        :return:
        """
        params = {
            "type": "hospital"
        }
        request.get_params('/api/admin/role/1.0/listByTypeAndHospitalId', params=params)


class permissions:
    # 权限

    def add(self, code):
        """
        新增权限数据
        :return:
        """
        name = 'test' + code
        body = {
            "name": name,
            "code": code,
            "sort": 1,
            "type": "menu",
            "parentId": 481
        }
        request.post_body('/api/admin/permissions/1.0', body=body)

    def get_id(self, id):
        """
        根据id获取权限详情
        :return:
        """
        response = request.get('/api/admin/permissions/1.0/{id}'.format(id=id))

        return response['data']

    def editPermissions(self, id):
        """
        更新权限信息
        :return:
        """
        data = self.get_id(id)

        body = {
            "name": data['name'],
            "code": data['code'],
            "sort": data['sort'],
            "type": data['type'],
            "parentId": data['parentId'],
            "icon": data['icon'],
            "remark": data['remark'],
            "route": data['route']
        }
        request.put_body('/api/admin/permissions/1.0/{id}'.format(id=id), body=body)

    def permissionsPageList(self):
        """
        获取权限列表
        :return:
        """
        response = request.get('/api/admin/permissions/1.0')

        for i in response['data']:
            if i['name'] == '权限测试':
                return i['children'][-1]['id']

    def findByHospital(self):
        """
        根据医院查询用户的权限
        :return:
        """
        request.get('/api/admin/permissions/1.0/findByHospital/{hospitalId}'.format(hospitalId=request.hospital_id))

    def getMenus(self):
        """
        根据医院查询菜单
        :return:
        """
        request.get('/api/admin/permissions/1.0/getMenus/{hospitalId}'.format(hospitalId=request.hospital_id))

    def getPermissionTree(self):
        """
        查询菜单权限树
        :return:
        """
        request.get('/api/admin/permissions/1.0/getPermissionTree')

    def reloadPermissionInterface(self):
        """
        重新加载接口权限
        :return:
        """
        params = {
            "hospitalId": request.hospital_id
        }
        request.get_params('/api/admin/permissions/1.0/reloadPermissionInterface', params=params)


class roleUser:
    # 角色绑定到用户

    def bind(self, roleId, userIds):
        """
        角色绑定到用户
        :param roleId: 角色id
        :param userIds: 用户id  列表
        :return:
        """
        body = {
            "roleId": roleId,
            "userIds": userIds
        }
        request.post_body('/api/admin/roleUser/1.0/bind', body=body)

    def unbind(self, roleId, userIds):
        """
        用户解绑角色
        :param roleId: 角色id
        :param userIds: 用户id  列表
        :return:
        """
        body = {
            "roleId": roleId,
            "userIds": userIds
        }
        request.delete_body('/api/admin/roleUser/1.0/unbind', body=body)


class printer:
    # 打印机相关接口

    def getListByUser(self):
        """
        查询科室打印机列表
        :return:
        """
        request.get('/api/admin/printer/1.0/getListByUser')


if __name__ == '__main__':
    # common().autoGenerateProcessingOrder()
    pprint.pprint(globalSearch().searchTypeList())
    # globalSearch().search()
    # globalSearch().goodsLife()
    # globalSearch().goodsItemLife()
    # globalSearch().gs1Decoding()
