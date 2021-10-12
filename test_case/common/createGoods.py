# -*- coding: utf-8 -*-
# @Time : 2021/1/22 7:14 下午
# @Author : lsj
# @File : createGoods.py
import time, request

import request

time_now = int(time.time() * 1000)
timeArray = time.localtime(time.time())
otherStyleTime = time.strftime("%m-%d-%H%M", timeArray)


# print(otherStyleTime)

class createGoods:
    # 创建商品
    def addGoods(self, goodsname, type=[1, 2, 3, 4], manufacturerId=341):
        name = None
        isHighValue = None
        isBarcodeControlled = None
        procurementPrice = None
        goodsList = []
        for i in type:
            if i == 1:
                # 低值非条码管控 价格1元
                name, isHighValue, isBarcodeControlled, procurementPrice = goodsname['low'], False, False, 100005000
            elif i == 2:
                # 低值条码管控 价格10元
                name, isHighValue, isBarcodeControlled, procurementPrice = goodsname['low1'], False, True, 1000005000
            elif i == 3:
                # 高值 价格100元
                name, isHighValue, isBarcodeControlled, procurementPrice = goodsname['high'], True, True, 10000005000

            elif i == 4:
                # 低值 工具包组包用
                name, isHighValue, isBarcodeControlled, procurementPrice = goodsname['lowbag'], False, False, 100005000
            body = {"name": name,
                    "manufacturerId": manufacturerId,  # 生产商
                    "specification": "1",
                    "procurementPrice": procurementPrice,  # 价格
                    "limitType": "",
                    "limitPerMonth": None,
                    "minGoodsUnitId": "5",  # 计价单位
                    "purchaseGoodsUnitId": "5",  # 包装规格
                    "minGoodsNum": 1,
                    "isBarcodeControllable": True,  # 条码可控
                    "isHighValue": isHighValue,  # 是否高值
                    "isImplantation": False,  # 是否植入物
                    "isBarcodeControlled": isBarcodeControlled,  # 是否条码管控
                    "isConsumableMaterial": False,  # 是否医疗器械
                    "category": [14553, 14548, 14525, 12715, 10917],
                    # "category": ["Ⅱ", "6803-Ⅱ", "19"],  # 商品分类12
                    # "category": ["Ⅲ", "03-Ⅲ", "207"],   # 商品分类18
                    "categoryType": None,  # 商品分类18搬，12版
                    "registrationList": [{
                        "registrationBeginDate": time_now,
                        "registrationEndDate": time_now,
                        "registrationImg": "/file/2021/05/11/RtyLvDBF2LDyKcni7XhzAabTA90EKKKQ/src=http___cdn.duitang.com_uploads_item_201410_20_20141020162058_UrMNe.jpeg&refer=http___cdn.duitang.jfif",
                        "registrationNum": "111",  # 注册证号
                        "registrationDate": False
                    }],
                    "std95GoodsCategoryId": 10917
                    # "std2012GoodsCategoryId": '19',
                    # "std2018GoodsCategoryId": '207'
                    }

            # body = {
            #     "name": '测试商品',
            #     # "manufacturerId": createManufacturer,  # 供应商ID
            #     "specification": "111",  # 规格
            #     "procurementPrice": 100000,  # 价格
            #     "limitType": "",  # 物资类别
            #     "minGoodsUnitId": "58",  # 计价单位
            #     "purchaseGoodsUnitId": "58",  # 包装规格
            #     "minGoodsNum": "1",  # 换算率
            #     "isBarcodeControllable": True,  # 是否条码可控
            #     "isHighValue": True,  # 是否高值
            #     "isImplantation": False,  # 是否植入物
            #     "isBarcodeControlled": True,  # 是否条码管控
            #     "isConsumableMaterial": False,  # 是否医疗器械
            #     "category": [14551, 14546, 14541, 14485, 12162],
            #     "registrationList": [{
            #         "registrationBeginDate": self.time_now,
            #         "registrationEndDate": self.time_now,
            #         "registrationImg": "/file/2021/05/11/RtyLvDBF2LDyKcni7XhzAabTA90EKKKQ/src=http___cdn.duitang.com_uploads_item_201410_20_20141020162058_UrMNe.jpeg&refer=http___cdn.duitang.jfif",
            #         "registrationNum": "111",  # 注册证号
            #         "registrationDate": False
            #     }],
            #     "std95GoodsCategoryId": 12162
            # }

            response = request.post_body('/api/admin/goodsTypes/1.0/add', body=body)
            goodsId = response['data']
            # 商品ID 列表
            goodsList.append(goodsId)
        # print(goodsList)
        return goodsList

    def get_goodsTypes(self, goodsId):
        """
        查询商品详情
        :param goodsId:
        :return:
        """

        response = request.get('/api/admin/goodsTypes/1.0/{}'.format(goodsId))

        return response['data']

    def editGoods(self, goodsId):
        """
        编辑商品
        :param goodsId:
        :return:
        """
        body = self.get_goodsTypes(goodsId)
        body['registrationList'] = []
        response = request.post_body('/api/admin/goodsTypes/1.0/edit', body=body)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    # 创建定数包
    def createBag(self, goodsId, bagName):
        body = {
            "goodsId": goodsId,  # 定数包内 商品ID
            "name": bagName,  # 定数包名字
            "quantity": 2  # 定数包里面商品的数量
        }
        response = request.post_body('/api/admin/packageBulks/1.0/add', body=body)
        bagId = response['data']
        return bagId

    # 修改定数包
    def editBag(self, bagId, goodsId, bagName):
        body = {
            "goodsId": goodsId,
            "name": bagName,
            "quantity": 2,
            "id": bagId,
        }
        response = request.post_body('/api/admin/packageBulks/1.0/edit', body=body)
        bagId = response['data']
        return bagId

    def get_id_Bag(self, id):
        """
        根据id获取普通套包详情
        :return:
        """
        request.get('/api/admin/packageBulks/1.0/{id}'.format(id=id))

    def pageList_packageBulks(self):
        """
        分页获取普通套包列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
        }
        request.get_params('/api/admin/packageBulks/1.0/pageList', params=params)

    def export_packageBulks(self):
        """
        导出定数包
        :return:
        """
        request.get('/api/admin/packageBulks/1.0/export')

    def printBarcode_packageBulks(self, id):
        """
        普通套包条码打印
        :return:
        """
        params = {
            "id": id
        }
        request.post_params('/api/admin/packageBulks/1.0/printBarcode', params=params)

    def getDepartmentPackageBulk(self, departmentId):
        """
        查询部门绑定的定数包
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "departmentId": departmentId
        }
        request.get_params('/api/admin/packageBulks/1.0/getDepartmentPackageBulk', params=params)

    def getUnbindPackageBulk(self, departmentId):
        """
        查询部门未绑定的定数包
        :return:
        """
        params = {
            "departmentId": departmentId
        }
        request.get_params('/api/admin/packageBulks/1.0/getUnbindPackageBulk', params=params)

    def findPackageWarehouseLimits(self):
        """
        查询部门所有仓库设置的定数包上下限
        :return:
        """
        params = {
            "departmentId": 1,
            "packageBulkId": 1
        }
        request.get_params('/api/admin/packageBulks/1.0/findPackageWarehouseLimits', params=params)

    def get_pageList(self, pkgName):
        """
        手术套包页面查询
        :param pkgName: 手术套包名
        :return: 手术套包id
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "name": pkgName
        }
        response = request.get_params('/api/admin/packageSurgical/1.0/pageList', params=params)

        return response['data']['rows'][0]['id'], response['data']['rows'][0]['combinedGoodsId']

    # 创建手术套包
    def createPkg(self, goodsId, pkgName):
        body = {
            "name": pkgName,
            "stockingUp": True,
            "packageSurgicalGoodsList": []
        }
        for i in goodsId:
            body['packageSurgicalGoodsList'].append({
                "quantity": 1,
                "goodsId": i
            })
        response = request.post_body('/api/admin/packageSurgical/1.0', body=body)

        return self.get_pageList(pkgName)

    # 修改手术套包
    def editPkg(self, pkgId, name):
        body = {
            "name": name,
            "description": None,
            "stockingUp": True,
            "id": pkgId
        }
        response = request.put_body('/api/admin/packageSurgical/1.0/{}'.format(pkgId), body=body)

    def get_id_Pkg(self, id):
        """
        根据id获取手术套包详情
        :return:
        """
        request.get('/api/admin/packageSurgical/1.0/{id}'.format(id=id))

    def get_Pkg_getAllDetails(self, id):
        """
        根据id获取手术套包详情
        :return:
        """
        request.get('/api/admin/packageSurgical/1.0/getAllDetails/{id}'.format(id=id))

    def export_Pkg(self):
        """
        导出手术套包
        :return:
        """
        request.get('/api/admin/packageSurgical/1.0/export')

    def getDepartmentPackageSurgical(self, departmentId):
        """
        分页获取部门绑定的手术套包列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "departmentId": departmentId
        }
        request.get_params('/api/admin/packageSurgical/1.0/getDepartmentPackageSurgical', params=params)

    def getUnbindSurgicalBulk(self):
        """
        查询未绑定手术套包
        :return:
        """
        params = {
            "departmentId": 1
        }
        request.get_params('/api/admin/packageSurgical/1.0/getUnbindSurgicalBulk', params=params)

    # 删除手术套包
    def delPkg(self, pkgId):

        response = request.delete('/api/admin/packageSurgical/1.0/{}'.format(pkgId))

    # 启用手术套包
    def usePkg(self, goodsId):

        response = request.put('/api/admin/packageSurgical/1.0/enable/{}'.format(goodsId))

    # 禁用手术套包
    def unUsePkg(self, goodsId):

        response = request.put('/api/admin/packageSurgical/1.0/disable/{}'.format(goodsId))

    def bindDepartment(self, departmentId, warehouseId, packageSurgicalId):
        """
        # 科室绑定手术套包
        :param departmentId: 科室id
        :param warehouseId: 仓库id
        :param packageSurgicalId: 手术套包id
        :return:
        """
        for x, y in zip(departmentId, warehouseId):
            body = {
                "departmentId": x,
                "settings": [{
                    "lowerLimit": 0,
                    "warehouseId": y,
                    "upperLimit": 0
                }],
                "packageSurgicalId": packageSurgicalId
            }
            response = request.post_body('/api/admin/packageSurgical/1.0/bindDepartment', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    def unbindDepartment(self, departmentId, packageSurgicalId):
        """
        # 科室解绑手术套包
        :param departmentId: 科室id
        :param warehouseId: 仓库id
        :param packageSurgicalId: 手术套包id
        :return:
        """
        for x in departmentId:
            body = {
                "departmentId": x,
                "packageSurgicalId": packageSurgicalId
            }
            response = request.post_body('/api/admin/packageSurgical/1.0/unbindDepartment', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    # 科室绑定商品
    def setDepartmentGoods(self, departmentId, warehouseId, goodsId):
        # departmentId = [0, 1, 2]
        # warehouseId = [3, 1, 5]
        # goodsId = [5, 7, 8]
        i = 0
        for x, y in zip(departmentId, warehouseId):
            for z in goodsId:
                body = {
                    "departmentId": x,  # 科室ID
                    "settings": [{
                        "lowerLimit": 0,  # 下限
                        "warehouseId": y,  # 仓库ID
                        "upperLimit": 0  # 上限
                    }],
                    "goodsId": z,  # 商品ID
                    "conversionUnitId": None  # 转换比
                }
                response = request.post_body('/api/admin/departments/1.0/setDepartmentGoods', body=body)
                try:
                    assert response['msg'] == '操作成功'
                except:
                    raise Exception(response)
            i += 1

    # 科室绑定定数包
    def bindBag(self, departmentId, warehouseId, packageBulkId):
        for x, y in zip(departmentId, warehouseId):
            body = {
                "departmentId": x,
                "settings": [{
                    "lowerLimit": 0,
                    "warehouseId": y,
                    "upperLimit": 0
                }],
                "packageBulkId": packageBulkId
            }
            response = request.post_body('/api/admin/packageBulks/1.0/bindWarehouse', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    # 科室解绑定数包
    def unbindBag(self, departmentId, packageBulkId):
        for x in departmentId:
            body = {
                "departmentId": x,
                "packageBulkId": packageBulkId
            }
            response = request.post_body('/api/admin/packageBulks/1.0/unbindWarehouse', body=body)
            # try:
            #     assert response['msg'] == '操作成功'
            # except:
            #     raise Exception(response)

    #  启用商品
    def useGoods(self, goodsList):
        for i in goodsList:
            body = {
                "isEnabled": True,
                "goodsId": i
            }
            response = request.post_body('/api/admin/goodsTypes/1.0/updateEnabled', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    # 启用定数包
    def useBag(self, bagId):
        body = {
            "id": bagId,
            "enable": True
        }
        response = request.post_body('/api/admin/packageBulks/1.0/enable', body=body)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    # 批量启用商品
    def batchUpdateStatus(self, goodsIds):
        body = {
            "enabled": True,
            "goodsIds": goodsIds
        }
        response = request.post_body('/api/admin/goodsTypes/1.0/batchUpdateStatus', body=body)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    # 商品绑定DI码
    def bindDI(self, goodsId, diCode='(01)10705032055116'):
        """
            # 商品绑定DI码
        :param goodsId:
        :param diCode:  DI码
        :return:
        """
        body = {
            "goodsId": goodsId,
            "diCode": diCode
        }
        response = request.post_body('/api/admin/goodsTypes/1.0/bindDI', body=body)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    def setDefaultSupplier(self, goodsId, supplierId):
        """
        # 商品设置默认供应商
        :param goodsId:
        :param supplierId: 供应商id
        :return:
        """
        body = {
            "goodsId": goodsId,
            "supplierId": supplierId
        }
        response = request.post_body('/api/admin/goodsTypes/1.0/setDefaultSupplier', body=body)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    def export_goodsType(self):
        """
        导出商品
        :return:
        """
        params = {
            "isCombined": False
        }
        response = request.get_params('/api/admin/goodsTypes/1.0/export', params=params)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    def get_pageList_goods(self):
        """
        # 根据id获取商品详情
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'isCombined': False
        }

        response = request.get_params('/api/admin/goodsTypes/1.0/pageList', params=params)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    def get_pageListWithoutPrice(self):
        """
        分页获取商品列表（去处价格）
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50,
        }
        response = request.get_params('/api/admin/goodsTypes/1.0/pageListWithoutPrice', params=params)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    def get_GoodsByDepartment(self):
        """
        根据部门获取商品列表，去除已生成定数包的
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'departmentId': 1
        }

        response = request.get_params('/api/admin/goodsTypes/1.0/getGoodsByDepartment', params=params)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    def get_SurgicalGoods(self):
        """
        获取组合商品
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50,
        }
        response = request.get_params('/api/admin/goodsTypes/1.0/getSurgicalGoods', params=params)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)

    def get_supplierGoods(self):
        """
        获取供应商关联的商品信息
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'supplierId': 1
        }
        response = request.get_params('/api/admin/goodsTypes/1.0/supplierGoods', params=params)
        try:
            assert response['msg'] == '操作成功'
        except:
            raise Exception(response)


if __name__ == '__main__':
    createGoods().addGoods('测试123')
