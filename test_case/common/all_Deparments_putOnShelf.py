# -*- coding: utf-8 -*-
# @Time : 2021/1/29 1:06 下午
# @Author : lsj
# @File : all_Deparments_putOnShelf.py

# 科室库上架
import jsonpath

import request


class Deparment:
    # 查询科室下所有 待上架的商品信息
    # 默认上架 商品
    def get_goods_detail(self, warehouseData):
        params = {
            'pageNum': 0,
            'pageSize': 20,
            'warehouseIds': warehouseData
        }
        response = request.get_params('/api/admin/stock/1.0/getRepositoryStockWithPage', params)
        detail = response['data']['rows']
        # 商品 列表
        goodsIdList = jsonpath.jsonpath(detail, '$.[*].goodsId')
        # lotNum
        lotNumList = jsonpath.jsonpath(detail, '$.[*].lotNum')
        # 仓库 列表
        warehouseIdList = jsonpath.jsonpath(detail, '$.[*].warehouseId')
        # 过期时间列表
        expirationDateList = jsonpath.jsonpath(detail, '$.[*].expirationDate')
        # 状态列表
        statusDateList = jsonpath.jsonpath(detail, '$.[*].status')
        # 总和
        detailList = [goodsIdList, lotNumList, warehouseIdList, expirationDateList, statusDateList]
        return detailList
        # print(detailList)

    # 获取 待上架商品详细信息  --code
    def get_goods_code(self, detailList, ):
        codeList = []
        for a, b, c, d, e in zip(detailList[0], detailList[1], detailList[2], detailList[3], detailList[4]):
            params = {
                'goodsId': a,
                'lotNum': b,
                'warehouseId': c,
                'expirationDate': d,
                'status': e
            }
            response = request.get_params('/api/admin/stock/1.0/getStockDetails', params)
            allDetail = response['data'][0]
            # goodsName = allDetail['goodsName']
            operatorBarcode = allDetail['operatorBarcode']
            # nameList.append(goodsName)
            codeList.append(operatorBarcode)
        return codeList

    def get_bag_detail(self, warehouseData):
        params = {
            'pageNum': 0,
            'pageSize': 20,
            'warehouseIds': warehouseData
        }
        response = request.get_params('/api/admin/stock/1.0/getPackageBulkStock', params)
        detail = response['data']['rows']
        # 商品 列表
        packageIdList = jsonpath.jsonpath(detail, '$.[*].packageId')
        # 仓库 列表
        warehouseIdList = jsonpath.jsonpath(detail, '$.[*].warehouseId')
        # 过期时间列表
        expirationDateList = jsonpath.jsonpath(detail, '$.[*].expirationDate')
        # 状态列表
        statusDateList = jsonpath.jsonpath(detail, '$.[*].status')
        # 总和
        detailList = [packageIdList, warehouseIdList, expirationDateList, statusDateList]
        return detailList
        # print(detailList)

    # 获取 待上架定数包详细信息  --code
    def get_bag_code(self, detailList, ):
        codeList = []
        for a, b, c, d in zip(detailList[0], detailList[1], detailList[2], detailList[3]):
            params = {
                'packageId': a,
                'warehouseId': b,
                'expirationDate': c,
                'status': d,
                'isExpired': False
            }
            response = request.get_params('/api/admin/stock/1.0/getPackageBulkStockDetails', params)
            allDetail = response['data'][0]
            # goodsName = allDetail['goodsName']
            operatorBarcode = allDetail['operatorBarcode']
            # nameList.append(goodsName)
            codeList.append(operatorBarcode)
        return codeList

    # 通过仓库ID 查询出货架ID 再查出 货位
    def get_storageLocation(self, warehouseData):
        idList = []
        storageLocationList = []
        for i in warehouseData:
            params = {
                'pageNum': 0,
                'pageSize': 20,
                'warehouseId': i
            }
            response = request.get_params('/api/admin/storageCabinets/1.0/pageList', params)
            id = response['data']['rows'][0]['id']
            idList.append(id)
        for j in idList:
            response = request.get('/api/admin/storageCabinets/1.0/%s' % j)
            locationsList = jsonpath.jsonpath(response, '$..locations[*]')
            for i in locationsList:
                # if 'Low0' in i['storageLocBarcode'] or 'High' in i['storageLocBarcode']:
                if 'Low0' in i['storageLocBarcode'] or 'High' in i['storageLocBarcode'] \
                        or 'Lowbag' in i['storageLocBarcode']:
                    code = i['storageLocBarcode']
                    storageLocationList.append(code)
        # print(storageLocationList)
        return storageLocationList

    # 上架商品
    def putOnshelf(self, codeList, storageLocationList):
        for x in codeList:
            body = {
                "code": x,
                "storageLocation": None,
                "putOnShelfLot": False
            }
            for y in storageLocationList:
                body['storageLocation'] = y
                response = request.post_body_01('/api/admin/stock/1.0/putOnShelf', body)
                try:
                    response['msg'] == '操作成功'
                except:
                    raise Exception(response)

    def all(self, warehouseData):
        # 这个地方 如果要做兼容的话 需要加type，目前是商品 和定数包同时拣货。
        # 单独捡商品、定数包、手术套包 后续有需求再加
        # 组合拣货 后续根据实际使用再做适配
        # 科室下所有待上架商品的信息
        detailList = self.get_goods_detail(warehouseData)
        # 每一条待上架商品的详细信息
        codeList = self.get_goods_code(detailList)

        # 低值 、高值 、定数包 的货位
        storageLocationList = self.get_storageLocation(warehouseData)

        # 通过商品code 和 货位 进行上架
        self.putOnshelf(codeList, storageLocationList)  # 捡商品

        return codeList

    def all1(self, warehouseData):
        # 低值 、高值 、定数包 的货位
        storageLocationList = self.get_storageLocation(warehouseData)
        bagDetailList = self.get_bag_detail(warehouseData)
        codeList1 = self.get_bag_code(bagDetailList)
        self.putOnshelf(codeList1, storageLocationList)  # 捡定数包

        return codeList1


if __name__ == '__main__':
    a = Deparment()
    # a.get_detail([116, 117, 118, 119])
    #
    # detailList = [[6343, 6343, 6344, 6343, 6344, 6343, 6344, 6344],
    #               ['1', '1', '1', '1', '1', '1', '1', '1'],
    #               [119, 116, 117, 117, 118, 118, 119, 116],
    #               [1619798400000, 1619798400000, 1619798400000, 1619798400000, 1619798400000, 1619798400000,
    #                1619798400000,
    #                1619798400000],
    #               ['put_on_shelf_pending', 'put_on_shelf_pending', 'put_on_shelf_pending', 'put_on_shelf_pending',
    #                'put_on_shelf_pending', 'put_on_shelf_pending', 'put_on_shelf_pending', 'put_on_shelf']]
    # a.get_stockDetail(detailList)
    #
    # stockDetails = ['ID_0103_6343_222785', 'ID_0103_6343_222782', 'ID_0103_6343_222783', 'ID_0103_6343_222784'], \
    #                ['ID_0103_6344_222788', 'ID_0103_6344_222789', 'ID_0103_6344_222790', 'ID_0103_6344_222787'], \
    #                ['Low042810', 'High042810']
    # a.putOnshelf(stockDetails)
    # warehouseList = [116, 117, 118, 119]
    # nameList = ['Low042810', 'High042810', 'High042810']
    # a.get_storageLocation(warehouseList)
    a.all1([538, 539, 540, 541])
