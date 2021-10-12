# -*- coding: utf-8 -*-
# @Time : 2021/1/22 2:55 下午
# @Author : spw
# @File : test_careat.py

import request
import time
from test_config.yamlconfig import timeid


def createWarehouse(name, departmentId, level=1):
    """
    # 新增仓库
    @param name: 仓库名
    @param departmentId: 科室id
    @param level: 科室等级   0：一级科室 ， 1：二级科室
    @return: 新增仓库的id
    """
    body = {
        "name": name,
        "level": level,
        "departmentId": departmentId,
        "isVirtual": False
    }
    response = request.post_body('/api/admin/warehouses/1.0', body)
    print('仓库{}'.format(response))

    return getWarehouse(name)


def getWarehouse(name):
    """
    根据仓库名查询该仓库id
    @param name: 仓库名
    @return: 该科室的id
    """
    params = {
        "pageNum": 0,
        "pageSize": 5,
        "name": name
    }
    warehouse_id = None
    response = request.get_params('/api/admin/warehouses/1.0/pageList', params)
    for i in response['data']['rows']:
        if i['name'] == name:
            warehouse_id = i['id']
            break
    return warehouse_id


def get_id_warehouses(id):
    """
    根据id获取仓库详情
    :return:
    """
    response = request.get('/api/admin/warehouses/1.0/{id}'.format(id=id))

    return response['data']


def editWarehouses(id):
    """
    更新仓库信息
    :return:
    """
    data = get_id_warehouses(id)

    body = {
        "name": data['name'],
        "level": data['level'],
        "departmentId": data['departmentId'],
        "isVirtual": data['isVirtual'],
        "deliveryGroupId": data['deliveryGroupId'],
        "priority": data['priority'],
        "id": id
    }
    request.put_body('/api/admin/warehouses/1.0/{id}'.format(id=id), body=body)


def getListByDepartment(departmentId):
    """
    查询部门的仓库信息
    :return:
    """
    params = {
        "departmentId": departmentId
    }
    request.get_params('/api/admin/warehouses/1.0/getListByDepartment', params=params)


def getListByDepartmentIds(departmentIds):
    """
    查询部门的仓库信息
    :return:
    """
    params = {
        "departmentIds": departmentIds
    }
    request.get_params('/api/admin/warehouses/1.0/getListByDepartmentIds', params=params)


def getByUser():
    """
    根据当前用户查询用户部门下所有的仓库
    :return:
    """
    request.get('/api/admin/warehouses/1.0/getByUser')


def getCentralWarehouse():
    """
    查询中心仓库
    :return:
    """
    request.get('/api/admin/warehouses/1.0/getCentralWarehouse')


def groupList():
    """
    推送组列表
    :return:
    """
    request.get('/api/admin/warehouses/1.0/groupList')


def getSummaryInfo():
    """
    仓库货位汇总查询
    :return:
    """
    params = {
        "pageNum": 0,
        "pageSize": 50
    }
    request.get_params('/api/admin/warehouses/1.0/getSummaryInfo', params=params)


def exportWarehouses():
    """
    仓库货位汇总导出
    :return:
    """
    request.get('/api/admin/warehouses/1.0/getSummaryInfo/export')


def createCargo(name, warehouseId_id):
    """
    # 新增货区
    @param name: 货区名
    @param warehouseId_id: 仓库id
    @return: 新增货区的id
    """
    body = {
        "name": name,
        "warehouseId": warehouseId_id,
        "storageAreaType": "174",
        "code": int(time.time() * 1000),
        "contact": "1111",
        "phone": "17899999999",
        "mergerName": "北京,东城,东华门",
        "address": "666",
        "hasSmartCabinet": True,
        "highValueSupported": True,
        "lowValueSupported": True
    }
    response = request.post_body('/api/admin/storageAreas/1.0/create', body)
    print('货区{}'.format(response))
    return getCargo(name)


def getCargo(name):
    """
    根据货区名查询货架id
    @param name: 货区名
    @return: 该货区的id
    """
    params = {
        "pageNum": 0,
        "pageSize": 5,
        "name": name
    }
    storageArea_id = None
    response = request.get_params('/api/admin/storageAreas/1.0/pageList', params)
    for i in response['data']['rows']:
        if i['name'] == name:
            storageArea_id = i['id']
            break
    return storageArea_id


def get_id_storageAreas(id):
    """
    根据库房id获取详情
    :return:
    """
    response = request.get('/api/admin/storageAreas/1.0/{id}'.format(id=id))

    return response['data']


def update_storageAreas(id):
    """
    更新库房信息
    :return:
    """
    data = get_id_storageAreas(id)

    body = {
        "name": data['name'],
        "warehouseId": data['warehouseId'],
        "storageAreaType": data['storageAreaType'],
        "code": data['code'],
        "contact": data['contact'],
        "phone": data['phone'],
        "mergerName": data['mergerName'],
        "address": data['address'],
        "hasSmartCabinet": data['hasSmartCabinet'],
        "highValueSupported": data['highValueSupported'],
        "lowValueSupported": data['lowValueSupported'],
        "remark": data['remark'],
        "id": id
    }
    request.put_body('/api/admin/storageAreas/1.0/update', body=body)


def listByWarehouse(warehouseId):
    """
    根据仓库id获取库房列表
    :return:
    """
    params = {
        "warehouseId": warehouseId
    }
    request.get_params('/api/admin/storageAreas/1.0/listByWarehouse', params=params)


def listByCentralWarehouse():
    """
    查询中心库的库房列表
    :return:
    """
    request.get('/api/admin/storageAreas/1.0/listByCentralWarehouse')


def del_storageAreas(id):
    """
    删除库房信息
    :return:
    """
    request.delete('/api/admin/storageAreas/1.0/{id}'.format(id=id))


def storageCabinets(name, warehouseId, storageAreaId, barCode):
    """
    # 新增货架
    @param name: 货架名
    @param warehouseId: 仓库id
    @param storageAreaId: 货区id
    @param barCode: 货位名
    @return: 货位list
    """
    barCode_0 = 'ow' + barCode
    barCode_1 = 'Low' + barCode
    barCode_2 = 'High' + barCode
    barCode_3 = 'Lowbag' + barCode
    body = {
        "locations": [{
            "storageLocBarcode": barCode_0
        },
            {
                "storageLocBarcode": barCode_1
            },
            {
                "storageLocBarcode": barCode_2
            },
            {
                "storageLocBarcode": barCode_3
            }],
        "name": name,
        "warehouseId": warehouseId,
        "storageAreaId": storageAreaId,
        "highValueSupported": True,
        "lowValueSupported": True,
        "barCode_0": barCode_0,
        "barCode_1": barCode_1,
        "barCode_2": barCode_2,
        "barCode_3": barCode_3
    }
    response = request.post_body('/api/admin/storageCabinets/1.0', body)
    print('货架{}'.format(response))
    return barCode_0, barCode_1, barCode_2, barCode_3


def pageListStorageCabinets(name):
    """
    根据货架名，查出货架id
    :return:
    """
    params = {
        "pageNum": 0,
        "pageSize": 5,
        "name": name
    }
    storageCabinets_id = None
    response = request.get_params('/api/admin/storageCabinets/1.0/pageList', params=params)
    for i in response['data']['rows']:
        if i['name'] == name:
            storageCabinets_id = i['id']
            break
    return storageCabinets_id


def get_id_storageCabinets(id):
    """
    更新货架信息
    :return:
    """
    response = request.get('/api/admin/storageCabinets/1.0/{id}'.format(id=id))

    return response['data']


def edit_storageCabinets(id):
    """
    更新货架信息
    :return:
    """
    data = get_id_storageCabinets(id)

    body = {
        "locations": [],
        "name": data['name'],
        "length": data['length'],
        "width": data['width'],
        "height": data['height'],
        "highValueSupported": data['highValueSupported'],
        "lowValueSupported": data['lowValueSupported'],
        "remark": data['remark'],
        "id": id
    }

    num = 0
    for i in data['locations']:
        body['barCode_{}'.format(num)] = i['storageLocBarcode']
        locationsItem = {
            "id": i['id'],
            "isDeleted": i['isDeleted'],
            "timeCreated": i['timeCreated'],
            "timeModified": i['timeModified'],
            "createdBy": i['createdBy'],
            "modifiedBy": i['modifiedBy'],
            "cabinetId": i['cabinetId'],
            "storageLocBarcode": i['storageLocBarcode'],
            "storageAreaId": i['storageAreaId'],
            "goodsId": i['goodsId'],
            "warehouseId": i['warehouseId'],
            "goodsName": i['goodsName'],
            "materialCode": i['materialCode'],
            "warehouseName": i['warehouseName'],
            "storageAreaName": i['storageAreaName'],
            "warehouseLevel": i['warehouseLevel']
        }
        body['locations'].append(locationsItem)
        num += 1

    request.put_body('/api/admin/storageCabinets/1.0/{id}'.format(id=id), body=body)


def listByStorageArea(storageAreaId):
    """
    根据库房id获取货柜列表
    :return:
    """
    params = {
        "storageAreaId": storageAreaId
    }
    request.get_params('/api/admin/storageCabinets/1.0/listByStorageArea', params=params)


def del_storageCabinets(id):
    """
    根据id删除货柜信息
    :return:
    """
    request.delete('/api/admin/storageCabinets/1.0/{id}'.format(id=id))


def warehouseData(department, goodsname):
    """
    新增科室仓库、货区、货架流程
    @param department: [[科室id],[科室name],[科室唯一数]]
    @return: [[货位list],[仓库list]]
    """
    barCode_list = []
    warehouse_list = []
    for x, y, z in zip(department[1], department[0], goodsname):
        warehouse_id = createWarehouse(x + '-仓库', y)
        storageArea_id = createCargo(x + '-货区', warehouse_id)
        barCodes = storageCabinets(x + '-货架', warehouse_id, storageArea_id, z)
        barCode_list.append(barCodes)
        warehouse_list.append(warehouse_id)
    return barCode_list, warehouse_list


def core_warehouseData(core_code):
    """
    新建中心库货区、货架流程
    :param core_code: 中心库唯一id
    :return: 中心库货位编号
    """
    storageAreaId = createCargo('中心库货区' + core_code, 1)
    core_barCodes = storageCabinets('中心库货架' + core_code, 1, storageAreaId, '-' + core_code)

    return core_barCodes


class distributionUnit:
    # 配送单位

    def __init__(self):
        pass

    def list(self, goodsId):
        """
        配送单列表查询
        :param goodsId:
        :return:
        """
        params = {
            'goodsId': goodsId
        }
        response = request.get_params('/api/admin/distributionUnit/1.0/list', params=params)

        return [i['id'] for i in response['data']]

    def add(self, goodsId):
        """
        新增配送单位
        :param goodsId:
        :return:
        """
        body = {
            "unitId": "5",
            "quantity": 1,
            "length": 1000,
            "width": 1000,
            "height": 1000,
            "volume": 1000,
            "goodsId": goodsId
        }
        request.post_body('/api/admin/distributionUnit/1.0/add', body=body)

    def update(self, id, goodsId):
        """
        更新配送单位
        :param id: 配送单id
        :param goodsId:
        :return:
        """
        body = {
            "unitId": "52",
            "quantity": 2,
            "length": 0,
            "width": 0,
            "height": 0,
            "volume": 0,
            "id": id,
            "goodsId": goodsId
        }
        request.post_body('/api/admin/distributionUnit/1.0/update', body=body)

    def delete(self, id):
        """
        配送单单位删除
        :param id: 配送单id
        :return:
        """
        a = request.delete('/api/admin/distributionUnit/1.0/delete/{}'.format(id))
        return a

    def setDefault(self, id, goodsId):
        """
        设置默认配送单位
        :param id:配送单id
        :param goodsId:
        :return:
        """
        body = {
            "id": id,
            "goodsId": goodsId
        }
        request.post_body('/api/admin/distributionUnit/1.0/setDefault', body=body)

    def unsetDefault(self, id, goodsId):
        """
        清空默认配送单位
        :param id:配送单id
        :param goodsId:
        :return:
        """
        body = {
            "id": id,
            "goodsId": goodsId
        }
        request.post_body('/api/admin/distributionUnit/1.0/unsetDefault', body=body)


class orderUnit:
    # 订货单位

    def __init__(self):
        pass

    def list(self, goodsId):
        """
        订货单位列表查询
        :param goodsId:
        :return:
        """
        params = {
            'goodsId': goodsId
        }
        response = request.get_params('/api/admin/orderUnit/1.0/list', params=params)

        return [i['id'] for i in response['data']]

    def add(self, goodsId):
        """
        新增订货单位
        :param goodsId:
        :return:
        """
        body = {
            "unitId": "59",
            "quantity": 1,
            "goodsId": goodsId,
            "type": "round",
            "rate": 0
        }
        request.post_body('/api/admin/orderUnit/1.0/add', body=body)

    def update(self, id, goodsId):
        """
        更新订货单位
        :param id: 配送单id
        :param goodsId:
        :return:
        """
        body = {
            "unitId": "59",
            "quantity": 1,
            "goodsId": goodsId,
            "type": "round",
            "rate": 0,
            "id": id
        }
        request.post_body('/api/admin/orderUnit/1.0/update', body=body)

    def delete(self, id):
        """
        订货单位删除
        :param id: 配送单id
        :return:
        """
        a = request.delete('/api/admin/orderUnit/1.0/delete/{}'.format(id))
        return a

    def setDefault(self, id, goodsId):
        """
        设置默认订货单位
        :param id:配送单id
        :param goodsId:
        :return:
        """
        body = {
            "id": id,
            "goodsId": goodsId
        }
        request.post_body('/api/admin/orderUnit/1.0/setDefault', body=body)

    def unsetDefault(self, id, goodsId):
        """
        清空默认订货单位
        :param id:配送单id
        :param goodsId:
        :return:
        """
        body = {
            "id": id,
            "goodsId": goodsId
        }
        request.post_body('/api/admin/orderUnit/1.0/unsetDefault', body=body)


class std95GoodsCategory_goodsQuantityUnits:
    # 95分类 和 获取商品计量单位信息列表

    def treeList(self):
        # 获取所有分类
        request.get('/api/admin/std95GoodsCategory/1.0/treeList')

    def rootList(self):
        # 获取根节点列表
        request.get('/api/admin/std95GoodsCategory/1.0/rootList')

    def singleList(self):
        # 获取每个根节点下面的子列表
        request.get('/api/admin/std95GoodsCategory/1.0/singleList')

    def pageList(self):
        # 获取商品计量单位信息列表
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/goodsQuantityUnits/1.0/pageList', params=params)


class diagnosisProject:
    # 诊疗项目管理

    def add(self, num, goodsId):
        """
        新增诊疗项目
        :return:
        """
        name = 'iow诊疗项目' + num
        body = {
            "name": name,
            "detail": [{
                "quantity": 2,
                "goodsId": goodsId
            }]
        }
        response = request.post_body('/api/admin/diagnosisProject/1.0/add', body=body)

        return response['data']

    def edit(self, id):
        """
        修改诊疗项目
        :return:
        """
        data = self.get_id(id)
        body = {
            "name": data['name'],
            "remark": None,
            "detail": [{
                "quantity": data['detail'][0]['quantity'],
                "goodsId": data['detail'][0]['goodsId']
            }],
            "id": id
        }
        request.put_body('/api/admin/diagnosisProject/1.0/edit', body=body)

    def get_id(self, id):
        """
        根据id查询诊疗项目
        :return:
        """
        response = request.get('/api/admin/diagnosisProject/1.0/get/{id}'.format(id=id))

        return response['data']

    def enable(self, id):
        """
        启用诊疗项目
        :return:
        """
        request.put('/api/admin/diagnosisProject/1.0/enable/{id}'.format(id=id))

    def forbid(self, id):
        """
        禁用诊疗项目
        :return:
        """
        request.put('/api/admin/diagnosisProject/1.0/forbid/{id}'.format(id=id))

    def pageList(self):
        """
        列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/diagnosisProject/1.0/pageList', params=params)

    def export(self):
        """
        导出诊疗项目
        :return:
        """
        request.get('/api/admin/diagnosisProject/1.0/export')


class diagnosis_project_department:
    # 诊疗项目科室绑定

    def getDepartmentDiagnosisProjectWithPage(self, departmentId):
        """
        查询科室诊疗项目列表
        :return:
        """
        params = {
            "departmentId": departmentId,
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/diagnosis-project-department/1.0/getDepartmentDiagnosisProjectWithPage',
                           params=params)

    def bind(self, departmentId, warehouseId, projectId):
        """
        绑定
        :param departmentId: 科室id
        :param warehouseId: 仓库id
        :param projectId: 诊疗项目id
        :return:
        """
        body = {
            "departmentId": departmentId,
            "settings": [{
                "lowerLimit": 0,
                "warehouseId": warehouseId,
                "upperLimit": 0
            }],
            "projectId": projectId
        }
        request.post_body('/api/admin/diagnosis-project-department/1.0/bind', body=body)

    def unbin(self, departmentId, projectId):
        """
        解绑
        :param departmentId: 科室id
        :param projectId: 诊疗项目id
        :return:
        """
        body = {
            "departmentId": departmentId,
            "projectId": projectId
        }
        request.post_body('/api/admin/diagnosis-project-department/1.0/unbind', body=body)


if __name__ == '__main__':
    print(distributionUnit().delete(15))
