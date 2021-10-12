#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/6/7 13:17 
# @Author   : 蓦然
# @File     : role.py
# Project   : integration-tests-insight

import request
from faker import Faker
import json
from test_config.yamlconfig import timeid
import time

timeStamp = int(time.time() * 1000)
fake = Faker(locale='zh_CN')


class role:
    def __init__(self):
        pass

    def addRole(self, rolename, remark="备注信息"):
        num = [timeStamp, timeStamp + 1, timeStamp + 2, timeStamp + 3]
        typex = ['custodian', 'hospital', 'operator', 'supplier']
        # rolelist = []
        roleIdlist = {}
        for name, type, code in zip(rolename.values(), typex, num):
            body = {
                "name": name,  # 名称
                "code": code,  # 编码
                "type": type,  # 类型
                "permissionIds": [370, 2, 2, 25, 25, 7, 11, 10, 9, 8, 7, 11, 10, 9, 8, 6, 6, 18, 17, 16, 15, 14, 18,
                                  17,
                                  16, 15, 14, 13, 13, 20, 23, 22, 25, 7, 11, 10, 9, 8, 6, 18, 17, 16, 15, 14, 13,
                                  20,
                                  23, 22, 21, 7, 11, 10, 9, 8, 6, 18, 17, 16, 15, 14, 13, 20, 23, 22, 21, 20, 23,
                                  22,
                                  21, 21, 29, 32, 33, 31, 30, 29, 32, 33, 31, 30, 28, 28, 35, 36, 37, 38, 39, 57,
                                  58,
                                  59, 60, 61, 62, 35, 36, 37, 38, 39, 57, 58, 59, 60, 61, 62, 63, 63, 45, 44, 43,
                                  42,
                                  41, 45, 44, 43, 42, 41, 374, 374, 49, 47, 48, 51, 52, 50, 53, 54, 55, 56, 49, 47,
                                  48,
                                  51, 52, 50, 53, 54, 55, 56, 373, 373, 446, 93, 89, 90, 91, 92, 94, 95, 93, 89, 90,
                                  91,
                                  92, 94, 95, 96, 96, 98, 101, 100, 98, 101, 100, 99, 99, 103, 104, 105, 103, 104,
                                  105,
                                  106, 106, 109, 108, 110, 111, 109, 108, 110, 111, 112, 112, 72, 66, 67, 68, 69,
                                  70,
                                  71, 73, 432, 72, 66, 67, 68, 69, 70, 71, 73, 432, 356, 356, 75, 76, 77, 78, 79,
                                  75,
                                  76, 77, 78, 79, 80, 80, 82, 83, 87, 86, 84, 29, 32, 33, 31, 30, 28, 35, 36, 37,
                                  38,
                                  39, 57, 58, 59, 60, 61, 62, 63, 45, 44, 43, 42, 41, 374, 49, 47, 48, 51, 52, 50,
                                  53,
                                  54, 55, 56, 373, 93, 89, 90, 91, 92, 94, 95, 96, 98, 101, 100, 99, 103, 104, 105,
                                  106,
                                  109, 108, 110, 111, 112, 446, 72, 66, 67, 68, 69, 70, 71, 73, 432, 356, 75, 76,
                                  77,
                                  78, 79, 80, 82, 83, 87, 86, 84, 85, 446, 72, 66, 67, 68, 69, 70, 71, 73, 432, 356,
                                  75,
                                  76, 77, 78, 79, 80, 82, 83, 87, 86, 84, 85, 82, 83, 87, 86, 84, 85, 85, 451, 372,
                                  371,
                                  122, 121, 120, 119, 118, 116, 115, 372, 371, 122, 121, 120, 119, 118, 116, 115,
                                  117,
                                  117, 130, 129, 126, 128, 127, 124, 125, 130, 129, 126, 128, 127, 124, 125, 131,
                                  131,
                                  135, 133, 134, 136, 372, 371, 122, 121, 120, 119, 118, 116, 115, 117, 130, 129,
                                  126,
                                  128, 127, 124, 125, 131, 135, 133, 134, 136, 137, 135, 133, 134, 136, 137, 137,
                                  186,
                                  429, 140, 141, 142, 430, 144, 145, 429, 140, 141, 142, 430, 144, 145, 143, 143,
                                  149,
                                  147, 149, 147, 148, 148, 154, 155, 153, 152, 151, 154, 155, 153, 152, 151, 160,
                                  160,
                                  157, 158, 159, 161, 157, 158, 159, 161, 162, 162, 166, 165, 164, 167, 169, 166,
                                  165,
                                  164, 167, 169, 168, 168, 171, 171, 174, 173, 175, 176, 177, 178, 174, 173, 175,
                                  176,
                                  177, 178, 179, 179, 181, 185, 184, 183, 181, 185, 184, 183, 182, 182, 188, 188,
                                  189,
                                  189, 191, 186, 429, 140, 141, 142, 430, 144, 145, 143, 149, 147, 148, 154, 155,
                                  153,
                                  152, 151, 160, 157, 158, 159, 161, 162, 166, 165, 164, 167, 169, 168, 171, 174,
                                  173,
                                  175, 176, 177, 178, 179, 181, 185, 184, 183, 182, 188, 189, 191, 192, 389, 388,
                                  389,
                                  388, 387, 393, 392, 391, 390, 387, 385, 384, 383, 382, 381, 380, 379, 378, 377,
                                  399,
                                  398, 397, 396, 395, 394, 386, 433, 434, 437, 436, 389, 388, 387, 393, 392, 391,
                                  390,
                                  385, 384, 383, 382, 381, 380, 379, 378, 377, 399, 398, 397, 396, 395, 394, 386,
                                  433,
                                  434, 437, 436, 435, 287, 288, 278, 279, 280, 281, 282, 283, 284, 285, 286, 290,
                                  291,
                                  294, 293, 296, 297, 385, 384, 383, 382, 381, 380, 379, 378, 377, 399, 398, 397,
                                  396,
                                  395, 394, 386, 433, 434, 437, 436, 435, 435, 301, 300, 301, 300, 302, 302, 304,
                                  304,
                                  305, 305, 307, 307, 308, 308, 310, 310, 312, 312, 314, 314, 315, 315, 317, 317,
                                  318,
                                  318, 320, 320, 364, 365, 428, 431, 448, 323, 323, 324, 324, 326, 326, 329, 330,
                                  329,
                                  330, 328, 328, 457, 457, 456, 456, 460, 460, 459, 459, 361, 362, 361, 362, 363,
                                  363,
                                  367, 368, 301, 300, 302, 304, 305, 307, 308, 310, 312, 314, 315, 317, 318, 320,
                                  323,
                                  324, 326, 329, 330, 328, 457, 456, 460, 459, 364, 365, 428, 431, 448, 361, 362,
                                  363,
                                  367, 368, 369, 364, 365, 428, 431, 448, 361, 362, 363, 367, 368, 369, 367, 368,
                                  369,
                                  369, 337, 333, 334, 335, 337, 333, 334, 335, 336, 336, 339, 339, 341, 341, 337,
                                  333,
                                  334, 335, 336, 339, 341, 343, 343, 343, 344, 348, 349, 350, 348, 349, 350, 347,
                                  347,
                                  438, 353, 354, 438, 353, 354, 352, 352, 445, 444, 443, 442, 348, 349, 350, 347,
                                  438,
                                  353, 354, 352, 445, 444, 443, 442, 441, 445, 444, 443, 442, 441, 441, 355, 357,
                                  358,
                                  359, 191, 192, 192, 197, 195, 201, 202, 200, 199, 198, 197, 195, 201, 202, 200,
                                  199,
                                  198, 196, 196, 207, 205, 204, 208, 209, 207, 205, 204, 208, 209, 206, 206, 212,
                                  213,
                                  214, 212, 213, 214, 211, 211, 216, 217, 219, 216, 217, 219, 218, 218, 226, 221,
                                  222,
                                  223, 224, 226, 221, 222, 223, 224, 225, 225, 228, 228, 244, 237, 238, 239, 240,
                                  241,
                                  242, 244, 237, 238, 239, 240, 241, 242, 243, 243, 246, 246, 247, 247, 249, 250,
                                  251,
                                  252, 253, 254, 249, 250, 251, 252, 253, 254, 255, 255, 464, 462, 197, 195, 201,
                                  202,
                                  200, 199, 198, 196, 207, 205, 204, 208, 209, 206, 212, 213, 214, 211, 216, 217,
                                  219,
                                  218, 226, 221, 222, 223, 224, 225, 228, 244, 237, 238, 239, 240, 241, 242, 243,
                                  246,
                                  247, 249, 250, 251, 252, 253, 254, 255, 464, 462, 463, 464, 462, 463, 463, 275,
                                  274,
                                  273, 260, 258, 260, 258, 259, 259, 263, 263, 262, 262, 265, 265, 266, 266, 269,
                                  269,
                                  268, 268, 272, 272, 271, 271, 454, 275, 274, 273, 260, 258, 259, 263, 262, 265,
                                  266,
                                  269, 268, 272, 271, 454, 453, 454, 453, 453, 287, 288, 278, 279, 280, 281, 282,
                                  283,
                                  284, 285, 287, 288, 278, 279, 280, 281, 282, 283, 284, 285, 286, 286, 290, 290,
                                  291,
                                  291, 294, 294, 293, 293, 296, 296, 297, 297, 393, 392, 391, 390],  # 权限分配
                "remark": remark,  # 备注信息
                "isSystemDefined": 'false'  # 系统定义
            }
            request.post_body('/api/admin/role/1.0', body=body)
            params = {
                "name": name,
                "pageNum": 0,
                "pageSize": 50,
                "status": "true",
                "type": type,
            }
            response = request.get_params('/api/admin/role/1.0/pageList', params=params)
            # rolelist.append(response['data']['rows'][0]['id'])
            roleIdlist[name] = response['data']['rows'][0]['id']
        # print(name, response['data']['rows'][0]['id'])
        print(roleIdlist)
        return roleIdlist

    def roleOperate(self, id, type):
        """
        启用/禁用 角色
        params : type 1启用 2禁用
        """
        body = {
            "id": id,
            "type": type
        }
        response = request.post_body('/api/admin/role/1.0/operate', body=body)
        return response

    def listByType(self, type):
        """
        根据type获取角色列表
        params type
        """
        params = {
            type
        }
        response = request.get_params('/api/admin/role/1.0/listByTypeAndHospitalId', params=params)
        return response

    def getRoleDetails(self, id):
        """
        根据id获取角色详情
        """
        response = request.get('/api/admin/role/1.0/%s' % id)
        print(response)
        return response

    def updateRole(self, id, name, remark, permissionIds=None):
        """
        修改角色信息
        """
        response = request.get('/api/admin/role/1.0/%s' % id)
        print(response)
        print(response['data']["type"])
        body = {
            "name": name,  # 名称
            "code": None,  # 编码
            "type": response['data']["type"],  # 类型
            "permissionIds": permissionIds,  # 权限分配
            "remark": remark,  # 备注信息
            "isSystemDefined": 'false'  # 系统定义
        }
        request.put_body("/api/admin/role/1.0/%s" % id, body=body)


class user():
    def addUser(self, type, roleIds, name, loginPhone, email, contactId):
        """
        添加用户
        """
        typelist = ['custodian', 'hospital', 'operator', 'supplier']
        try:
            for i in typelist:
                if i == type:
                    body = {
                        "type": type,
                        "roleIds": roleIds,
                        "name": name,
                        "loginPhone": loginPhone,
                        "email": email,
                        # "profileImg": None,
                        # "remark": remark
                        "contactId": contactId
                    }
        except:
            raise Exception("类型错误")

        request.post_body('/api/admin/users/1.0', body=body)

    def getUserList(self, typeList, isEnabled, loginPhone, name, custodianIds=None, departmentIds=None,
                    supplierIds=None, type=None):
        """
        获取用户列表
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "typeList": typeList,
            "isEnabled": isEnabled,
            "loginPhone": loginPhone,
            "name": name,
            "custodianIds": custodianIds,
            "departmentIds": departmentIds,
            "supplierIds": supplierIds,
            "type": type
        }
        response = request.get_params("/api/admin/users/1.0", params=params)
        print(response)
        return response

    def userDetail(self, id):
        """
        获取 用户详情
        params id
        """
        response = request.get("/api/admin/users/1.0/%s" % id)
        print(response)
        return response

    def updateUser(self, id, type, roleIds, name, loginPhone, email, contactId):
        """

        """
        body = {
            "type": type,
            "roleIds": roleIds,
            "name": name,
            "loginPhone": loginPhone,
            "email": email,
            # "profileImg": None,
            # "remark": remark
            "contactId": contactId
        }
        response = request.put_body("/api/admin/users/1.0/%s" % id)
        return response

    def adminUpdatepwd(self, userId):
        """
        重置密码
        put
        """
        body = {
            "userId": userId
        }
        request.put_body("/api/admin/users/1.0/adminUpdatePwd", body=body)

    def getPickerList(self):
        """
        查询拣货员列表接口
        """
        response = request.get("/api/admin/users/1.0/getPickerList")
        return response

    def getPusherList(self):
        """
        查询推送员列表接口
        """
        response = request.get("/api/admin/users/1.0/getPusherList")
        return response

    def getUserBaseInfo(self, userId):
        """
        查询用户基本信息
        """
        params = {
            "userId": userId
        }
        response = request.get_params("/api/admin/users/1.0/getUserBaseInfo", params=params)
        return response

    def listByDepartmentId(self, departmentId):
        """
        根据组织Id获取用户列表，如果为中心库绑定的科室，则查询中心库和该科室的所有人员
        params: departmentId 部门id
        """
        params = {
            "departmentId": departmentId
        }
        response = request.get_params("/api/admin/users/1.0/listByDepartmentId", params=params)
        print(response)
        return response

    def userOperte(self, enable, userId):
        """
        用户启用/禁用
        body : enable, userid
        """
        body = {
            "enable": enable,
            "id": userId
        }
        request.post_body("/api/admin/users/1.0/operate", body=body)

    def getListByRoleId(self, roleId, enabled, excludeExists, loginPhone, name, type, typeList=None):
        """
        根据角色Id获取用户列表
        """
        params = {
            "enabled": enabled,
            "excludeExists": excludeExists,
            "loginPhone": loginPhone,
            "name": name,
            "pageNum": 0,
            "pageSize": 50,
            "roleId": roleId,
            "type": type,
            "typeList": typeList
        }
        response = request.get_params("/api/admin/users/1.0/listByRoleId", params=params)

    def updatePwd(self, newPassword, oldPassword):
        """
        修改密碼
        """
        body = {
            "newPassword": newPassword,
            "oldPassword": oldPassword
        }
        response = request.put_body("/api/admin/users/1.0/updatePwd", body=body)
        return response

    def getRoleList(self, name=None, type=None):
        """
        获取用户列表
        """
        roleIdList = []
        params = {
            "name": name,
            "pageNum": 0,
            "pageSize": 50,
            "status": "true",
            "type": type,
        }
        response = request.get_params('/api/admin/role/1.0/pageList', params=params)
        for i in response['data']['rows']:
            roleIdList.append(i['id'])
        return roleIdList

    def wechatSave(self, formId):
        """
        小程序收集formid保存入库
        body: formid
        """
        params = {
            "formId": formId
        }
        response = request.post_params("/api/admin/formid/1.0/save", params=params)
        print(response)


if __name__ == '__main__':
    name = timeid().id()
    # print(name['rolename'])
    # for i in name['rolename'].values():
    #     print(i)
    # print(name)
    # role().addRole(name['rolename'])
    # role().roleOperate(69, 1)
    # role().getRoleDetails(67)
    # role().updateRole(67, "一级供应商角色test", "备注", [11, 7, 25, 2, 370, 5, 12, 19])
    # user().addUser("supplier", [70], "麻醉师1234", 15936930114, "m17600888366@163.com", [1])
    # user().getUserList(["operator", "hospital", "supplier", "custodian"], "false", "15936930113", "麻醉师1234")
    # user().userDetail(1)
    # user().adminUpdatepwd(13)
    # user().listByDepartmentId(1)
    # user().getListByRoleId(1, True, True, None, None, None)
    # user().getRoleList()
    user().wechatSave(1)
