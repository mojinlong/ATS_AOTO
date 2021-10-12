#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/6/4 15:10 
# @Author   : 蓦然
# @File     : user.py
# Project   : integration-tests-insight

import request
from faker import Faker
import json
fake = Faker(locale='zh_CN')
# print(fake.name())


class user():
    def __init__(self):
        # self.type = ['operator', 'supplier', 'hospital', 'custodian']
        pass

    def getUserList(self, custodianIds=None, departmentIds=None, isEnabled=None, loginPhone=None, name=None, roleId=None, supplierIds=None,
                    type=None, typeList=None):
        """
        @Author   : 蓦然
        获取用户列表信息
        param:
        """
        params = {
            "custodianIds": custodianIds,
            "departmentIds": departmentIds,
            "isEnabled": isEnabled,
            "loginPhone": loginPhone,
            "name": name,
            "pageNum": 0,
            "pageSize": 50,
            "roleId": roleId,
            "supplierIds": supplierIds,
            "type": type,
            "typeList": typeList,
        }
        response = request.get_params('/api/admin/users/1.0', params=params)
        # print(response)
        # for i in response['data']['rows']:
        #     if i['name'] == name:
        return response

    def addUser(self, type=None, roleIds=None, name=None, loginPhone=None, email=None, remark=None, contactId=None):
        """
        @Author   : 蓦然
        新增用户
        """
        body = {
            "type": type,
            "roleIds": roleIds,
            "name": name,
            "loginPhone": loginPhone,
            "email": email,
            "profileImg": None,
            "remark": remark,
            "contactId": [None],
            "profileImg": ""
        }
        response = request.post_body('/api/admin/users/1.0', body=body)
        print(response)
        return name

    def operateUser(self, userId, enable):
        """
        @Author   : 蓦然
        启用/禁用 用户
        body: {userId, enable}
        """
        body = {
            {
                "id": userId,
                "enable": enable
            }
        }
        response = request.post_body('/api/admin/users/1.0/operate', body=body)
        return response


if __name__ == '__main__':
    # fake = Faker(locale='zh_CN')
    # print(fake.phone_number())
    type = ['operator', 'supplier', 'hospital', 'custodian']
    useradd = user().addUser(type=type[0], roleIds=[3], name=fake.name(), loginPhone=fake.phone_number(), email=fake.email(),
                   remark='123')
    list = user().getUserList(name=useradd)
    print(list['data']['rows'][0]['id'])
