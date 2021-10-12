# -*- coding: utf-8 -*-
# @Time : 2021/1/22 2:55 下午
# @Author : lsj
# @File : test_careat.py
import jsonpath

import request, random

hospitalCampusId = 103  # 大华医院id
# hospitalCampusId = request.hospital_id  # 徐汇区中心医院
mergeName = '北京,东城,东华门'  # 所在区域
address = '测试地址'  # 地址


# 创建一级科室
def createDepMax(name='测试0003'):
    url = '/api/admin/departments/1.0'
    body = {
        "name": name,
        "hospitalCampusId": hospitalCampusId,
        "parentId": None,
        "mergeName": mergeName,
        "address": address,
        "contactName": "1111",
        "contactPhone": "14788888888",
        "remark": "1111"
    }

    response = request.post_body(url, body)

    # try:
    #     assert response['msg'] == '操作成功'
    # except:
    #     raise Exception(response)

    response1 = request.get('/api/admin/departments/1.0/treeList')

    detail = response1['data']

    i = len(detail) - 1
    parentId = detail[i]['id']
    return parentId


# 创建二级科室
def createDepMin(parentId=162, j=None):
    # i = 1
    Num = []
    departmentId = []
    departmentName = []
    for x in j:

        # 设置二级科室名字
        # Name = name + x
        url = '/api/admin/departments/1.0'
        body = {"name": x,
                "hospitalCampusId": hospitalCampusId,
                "parentId": parentId,
                "mergeName": mergeName,
                "address": address}
        response1 = request.post_body(url, body)
        # try:
        #     assert response1['msg'] == '操作成功'
        # except:
        #     raise Exception(response1)
        # i += 1
        Num.append(x)
        response2 = request.get('/api/admin/departments/1.0/treeList')
        for i in response2['data'][-1]['children']:
            if i['name'] == x:
                departmentId.append(i['id'])
                departmentName.append(i['name'])

    return departmentId, departmentName, Num


def getdepartmentsName(departmentsId):
    """
    根据id获取组织详情
    :param departmentsId:
    :return:
    """
    response = request.get('/api/admin/departments/1.0/{}'.format(departmentsId))
    return response['data']['name']


def pageList():
    """
    分页获取直接子节点组织列表
    :return:
    """
    params = {
        'pageNum': 0,
        'pageSize': 50
    }
    request.get_params('/api/admin/departments/1.0/pageList', params=params)


def treeList():
    """
    获取组织树列表
    :return:
    """
    request.get('/api/admin/departments/1.0/treeList')


def getParent(id):
    """
    根据id获取父级组织
    :return:
    """
    request.get('/api/admin/departments/1.0/getParent/{id}'.format(id=id))


def getDepartmentGoodsWithPage(departmentId):
    """
    分页查询科室商品
    :return:
    """
    params = {
        'pageNum': 0,
        'pageSize': 50,
        'departmentId': departmentId
    }
    request.get_params('/api/admin/departments/1.0/getDepartmentGoodsWithPage', params=params)


def exportDepartmentGoods(departmentId):
    """
    导出科室商品
    :return:
    """
    params = {
        'pageNum': 0,
        'pageSize': 50,
        'departmentId': departmentId
    }
    request.get_params('/api/admin/departments/1.0/exportDepartmentGoods', params=params)


def addWarehouseGoodsLimit(goodsId, warehouseId):
    """
    设置仓库商品上下限
    :return:
    """
    body = {
        "goodsId": goodsId,
        "lowerLimit": 1,
        "upperLimit": 10,
        "userId": 234,
        "warehouseId": warehouseId
    }
    request.post_body('/api/admin/departments/1.0/addWarehouseGoodsLimit', body=body)


def updateWarehouseGoodsLimit(goodsId, warehouseId):
    """
    修改仓库商品上下限
    :return:
    """
    body = {
        "goodsId": goodsId,
        "lowerLimit": 1,
        "upperLimit": 10,
        "userId": 234,
        "warehouseId": warehouseId
    }
    request.post_body('/api/admin/departments/1.0/updateWarehouseGoodsLimit', body=body)


def removeWarehouseGoodsLimit(warehouseGoodsLimitId):
    """
    删除仓库商品上下限
    :return:
    """
    body = {
        "warehouseGoodsLimitId": warehouseGoodsLimitId
    }
    request.delete_body('/api/admin/departments/1.0/removeWarehouseGoodsLimit', body=body)


def setDepartmentGoods(goodsId, departmentId, warehouseId):
    """
    设置科室商品并设置上下限
    :return:
    """
    body = {
        "departmentId": departmentId,
        "settings": [{
            "lowerLimit": 100,
            "warehouseId": warehouseId,
            "upperLimit": 110
        }],
        "goodsId": goodsId,
        "conversionRate": None,
        "conversionUnitId": None
    }
    request.post_body('/api/admin/departments/1.0/setDepartmentGoods', body=body)


def getWarehouseGoodsList(departmentId, goodsId):
    """
    查询仓库商品列表
    :return:
    """
    params = {
        "departmentId": departmentId,
        "goodsId": goodsId
    }
    request.get_params('/api/admin/departments/1.0/getWarehouseGoodsList', params=params)


def getSelections():
    """
    获取可以访问的非一级科室的科室名称和id
    :return:
    """
    request.get('/api/admin/departments/1.0/getSelections')


def getAllSubDepartment():
    """
    获取所有非一级科室的科室名称和id
    :return:
    """
    request.get('/api/admin/departments/1.0/getAllSubDepartment')


def getAllDepartment():
    """
    获取所有科室(包含一级科室)的科室名称和id
    :return:
    """
    request.get('/api/admin/departments/1.0/getAllDepartment')


def unbindDepartmentGoods(goodsId, departmentId):
    """
    解绑商品和部门
    :return:
    """
    body = {
        "departmentId": departmentId,
        "goodsId": goodsId
    }
    request.post_body('/api/admin/departments/1.0/unbindDepartmentGoods', body=body)


def editDepartments(departmentsId):
    """
    编辑科室
    :param departmentsId: 科室id
    :param name: 科室名字
    :return:
    """
    body = {
        "name": getdepartmentsName(departmentsId),
        "hospitalCampusId": hospitalCampusId,
        "parentId": None,
        "mergeName": mergeName,
        "address": address,
        "contactName": "1111",
        "contactPhone": "14788888888",
        "remark": "1111",
        'id': departmentsId
    }
    response = request.put_body('/api/admin/departments/1.0/{}'.format(departmentsId), body)


def delDepartments(departmentsId):
    """
    删除科室
    :param departmentsId: 科室id
    """

    response = request.delete('/api/admin/departments/1.0/{}'.format(departmentsId))


def batchBindDepartmentGoods(departmentIds, goodsId):
    """
    批量绑定科室和商品
    :param departmentIds: 科室列表
    :param goodsId: 商品id
    :return:
    """
    body = {
        "departmentIds": departmentIds,
        "goodsId": goodsId
    }
    response = request.post_body('/api/admin/departments/1.0/batchBindDepartmentGoods', body)


def removeDepartmentGoods(departmentId):
    """
    移除科室商品
    :param departmentIds: 科室
    :return:
    """
    response = request.delete('/api/admin/departments/1.0/removeDepartmentGoods/{}'.format(departmentId))


def allCreate(name='ceshi011', name_id=None):
    return createDepMin(parentId=createDepMax(name), j=name_id)


def batchSetDepartmentGoods(departmentId, goodsIds=[]):
    """
    批量绑定科室物资
    :param departmentId: 科室
    :param goodsIds 商品
    """
    body = {
        "departmentId": departmentId,
        "goodsIds": goodsIds
    }
    response = request.post_body('/api/admin/departments/1.0/batchSetDepartmentGoods', body=body)


def delete(id):
    request.delete("/api/admin/departments/1.0/{id}".format(id=id))


def getDepartmentGoodsWithPage():
    params = {
        'isCombinedDevelopment': 'false',
        'IsCombined': 'false',
        'departmentId': '2292',
        'pageNum': 0,
        'pageSize': 50
    }


class hospital:
    # 医院

    def setCurrentHospital(self):
        """
        设置当前医院
        :return:
        """
        body = {
            "hospitalId": request.hospital_id
        }
        request.post_body('/api/admin/hospital/1.0/setCurrentHospital', body=body)

    def list(self):
        """
        医院列表
        :return:
        """
        request.get('/api/admin/hospital/1.0/list')

    def get_id(self):
        """
        根据id获取医院院区详情
        :return:
        """
        request.get('/api/admin/hospitalCampus/1.0/{id}'.format(id=request.hospital_id))

    def get_list(self):
        """
        获取医院院区列表
        :return:
        """
        request.get('/api/admin/hospitalCampus/1.0')

    def get_jobTitle(self):
        """
        获取医院职务列表
        :return:
        """
        request.get('/api/admin/jobTitle/1.0')


if __name__ == '__main__':
    batchSetDepartmentGoods(departmentId=2292, goodsIds=[13500, 13499, 13498, 13497])
