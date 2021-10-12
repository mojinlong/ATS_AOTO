#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/1/27 16:52
# @File     : centralLibrary.py
# @Project  : integration-tests-insight
import pprint

import request, all_check


# 中心库标准验收
class receivingOrder:
    def __init__(self):
        pass

    # ['DN_0303_0001_210427_0003', 'DN_0303_0001_210427_0002', 'DN_0303_0001_210427_0001']
    def shippingCompleted(self, shippingCode):
        """
        中心库确认送达
        :param shippingCode: 配送单号
        :return:
        """

        params = {
            "code": shippingCode
        }
        request.get_params('/api/admin/shippingOrder/1.0/shippingCompleted', params)

    def getReceivingWithPage(self, shippingCode):
        """
        标准验收页面查询
        :param shippingCode: 配送单号code
        :return: 验收单id
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "shippingCode": shippingCode,
            "surgicalRequest": False
        }
        response = request.get_params('/api/admin/receivingOrder/1.0/getReceivingWithPage', params)

        return response['data']['rows'][0]['receivingId']

    def loadReceiving(self, receivingId):
        """
        批量验收明细查询
        获取操作operatorCodes操作员id
        :param receivingId: 验收单id    通过getReceivingWithPage()方法来获取
        :return:  验收单明细接收id
        """
        params = {
            "receivingOrderId": receivingId
        }
        response = request.get_params('/api/admin/receivingOrder/1.0/loadReceiving', params)

        return [i['operatorBarcode'] for i in response['data']['receiving']]

    def doBatchPass(self, operatorCodes_list, shippingOrderCode):
        """
        批量验收
        :param operatorCodes_list: 验收单明细接收id
        :return:
        """
        body = {
            "operatorCodes": operatorCodes_list,
            "shippingOrderCode": shippingOrderCode,
            "status": "passed"
        }
        response = request.post_body('/api/admin/receivingOrder/1.0/doBatchPass', body)

        return response

    def makeConclusion(self, receivingId):
        """
        验收单提交
        :param receivingId: 验收单id
        :return:
        """
        body = {
            "receivingOrderId": receivingId
        }
        response = request.post_body('/api/admin/receivingOrder/1.0/makeConclusion', body)

    def all_receivingOrder(self, shippingCode):
        """
        总验收流程
        :param shippingCode: 配送单code
        :return:
        """
        # 确认送达
        self.shippingCompleted(shippingCode)
        # 验收单id
        receivingId = self.getReceivingWithPage(shippingCode)
        # 验收单明细id
        operatorCodes_list = self.loadReceiving(receivingId)
        # 批量验收
        self.doBatchPass(operatorCodes_list, shippingCode)
        # 提交
        self.makeConclusion(receivingId)


class stock():
    """
    中心库库存
    """

    def putOnShelf(self, code, storageLocation):
        """
        上架
        :param code: 物资条码
        :param storageLocation: 货位号
        :return:
        """
        body = {
            "code": code,
            "storageLocation": storageLocation,
            "putOnShelfLot": True
        }
        response = request.post_body('/api/admin/stock/1.0/putOnShelf', body)

    def getStockDetails(self, goodsId, expirationDate, lotNum, warehouseId=1, status='put_on_shelf_pending'):
        """
        查询  商品  库存
        :return:
        """
        params = {
            "goodsId": goodsId,
            "lotNum": lotNum,
            "status": status,
            "warehouseId": warehouseId,
            "expirationDate": expirationDate
        }
        response = request.get_params('/api/admin/stock/1.0/getStockDetails', params)

        if status == 'picked':
            return [i['operatorBarcode'] for i in response['data']], \
                   [i['goodsItemId'] for i in response['data']]

        return [i['operatorBarcode'] for i in response['data']]

    def getPackageBulkStockDetails(self, packageId, expirationDate, status='put_on_shelf_pending'):
        """
        查询  定数包  库存
        :return:
        """
        params = {
            "packageId": packageId,
            "status": status,
            "warehouseId": 1,
            "expirationDate": expirationDate,
            "isExpired": False
        }
        response = request.get_params('/api/admin/stock/1.0/getPackageBulkStockDetails', params)

        return [i['operatorBarcode'] for i in response['data']]

    def getPackageSurgicalStockDetails(self, packageSurgicalId, expirationDate, status='put_on_shelf_pending'):
        """
        查询  手术套包  库存
        :return:
        """
        params = {
            "packageSurgicalId": packageSurgicalId,
            "status": status,
            "warehouseId": 1,
            "expirationDate": expirationDate,
            "isExpired": False
        }
        response = request.get_params('/api/admin/stock/1.0/getPackageSurgicalStockDetails', params)

        return [i['operatorBarcode'] for i in response['data']]

    ######################################################################################################################

    def add_pickOrder(self, pendingIds):
        """
        生成拣货单
        :param pendingIds: 待拣货单id
        :return:
        """
        body = {
            "pendingIds": pendingIds
        }
        response = request.post_body_01('/api/admin/pickOrder/1.0/add', body)

        return response['data']

    ##################################################################################################################

    def get_pickPending(self, goodsName, type):
        """
        待拣货单id
        :param goodsName:
        :param type:   商品：goods      定数包：package_bulk
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "type": type,
            "status": "generate_pick_order_pending",
            "goodsName": goodsName
        }
        response = request.get_params('/api/admin/pickPending/1.0/list', params)
        pendingIds_list = []
        departmentName_list = list(dict.fromkeys(x['departmentName'] for x in response['data']['rows']))
        for y in departmentName_list:
            pendingIds_list.append([z['id'] for z in response['data']['rows'] if z['departmentName'] == y])

        return pendingIds_list

    def pickPending_cancel(self, id):
        """
        取消待拣货数据
        :id: 带拣货单id
        :return:
        """
        body = {
            "id": id
        }
        request.post_body('/api/admin/pickPending/1.0/cancel', body=body)

    def get_pickOrderid(self, code):
        """
        查询拣货单id
        :return: pickOrder_id
        """
        params = {
            "pageNum": 0,
            "pageSize": 5000,
            "status": "pick_pending",
        }
        response = request.get_params('/api/admin/pickOrder/1.0/list', params)

        return [i['code'] for i in response['data']['rows'] if str(code) in i['departmentName']], \
               [i['id'] for i in response['data']['rows'] if str(code) in i['departmentName']]

    def detail_pickOrder(self, pickOrder_code):
        """
        查询拣货单id明细
        :return: 返回明细id
        """
        params = {
            "code": pickOrder_code,
        }
        response = request.get_params('/api/admin/pickOrder/1.0/detail', params)

        # detail_pickOrder_dict = {}
        # pickPendingId = []
        # for i in response['data']['detail']:
        #     detail_pickOrder_dict[i['goodsName']] = i['quantity']
        #     pickPendingId.append(i['id'])

        return [i['goodsName'] for i in response['data']['detail']], \
               [i['quantity'] for i in response['data']['detail']], \
               [i['id'] for i in response['data']['detail']]
        # return detail_pickOrder_dict, pickPendingId

    def get_RepositoryStockWithPage(self, name):
        """
        根据物资名称查询  商品  库存列表
        :return: 返回物资id
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "name": name,
        }
        response = request.get_params('/api/admin/stock/1.0/getRepositoryStockWithPage', params)

        if [i['goodsId'] for i in response['data']['rows']] == []:

            return [i['goodsId'] for i in response['data']['rows']], \
                   None, None

        else:
            return [i['goodsId'] for i in response['data']['rows']], \
                   response['data']['rows'][0]['expirationDate'], \
                   response['data']['rows'][0]['lotNum']

    def get_PackageBulkStock(self, name):
        """
        根据物资名称查询  定数包  库存列表
        :return: 返回物资id
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "goodsName": name,
        }
        response = request.get_params('/api/admin/stock/1.0/getPackageBulkStock', params)

        return response['data']['rows'][0]['packageId'], response['data']['rows'][0]['expirationDate']

    def get_PackageSurgicalStock(self, name):
        """
        根据物资名称查询  手术套包  库存列表
        :return: 返回物资id
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "packageSurgicalName": name,
        }
        response = request.get_params('/api/admin/stock/1.0/getPackageSurgicalStock', params)

        return response['data']['rows'][0]['packageSurgicalId'], response['data']['rows'][0]['expirationDate']

    def pick_pickOrder(self, goodsItemCode, pickOrderId, pickPendingId):
        """
        拣货
        :param goodsId: 商品id
        :param goodsItemCode: 商品条码
        :param pickOrderId: 拣货单id
        :param pickPendingId: 拣货单明细id
        :return:
        """
        body = {
            "goodsItemCode": goodsItemCode,
            "pickOrderId": pickOrderId,
            "quantity": 1,
            "pickPendingId": pickPendingId
        }
        request.post_body('/api/admin/pickOrder/1.0/pick', body)

    def aoto_pick_pickOrder(self, code, pickOrder_code=None, pickOrder_id=None, type='goods'):
        """
        自动拣货
        :return:
        """
        if pickOrder_code is None and pickOrder_id is None:
            # 查拣货单id
            pickOrder_code, pickOrder_id = self.get_pickOrderid(code)
        print('拣货单code{}'.format(pickOrder_code))
        print('拣货单id{}'.format(pickOrder_id))

        for x, j in zip(pickOrder_code, pickOrder_id):
            # 拣货单明细id
            goodsName_list, quantity, pickPendingId = self.detail_pickOrder(x)
            for y, z, num in zip(goodsName_list, pickPendingId, quantity):
                # 数量
                for i in range(num):
                    if type == 'goods':
                        goodsId, expirationDate, lotNum = self.get_RepositoryStockWithPage(y)
                        # 物资条码列表
                        goodsItemCode = self.getStockDetails(goodsId, expirationDate, lotNum, status='put_on_shelf')
                        if goodsItemCode != []:
                            # 取物资条码第一个
                            self.pick_pickOrder(goodsItemCode[0], j, z)
                    elif type == 'bag':
                        # 查询定数包信息
                        packageId, expirationDate = self.get_PackageBulkStock(y)
                        goodsItemCode = self.getPackageBulkStockDetails(packageId, expirationDate,
                                                                        status='put_on_shelf')
                        if goodsItemCode != []:
                            # 取物资条码第一个
                            self.pick_pickOrder(goodsItemCode[0], j, z)
                    elif type == 'pkg':
                        # 查询手术套包信息
                        packageSurgicalId, expirationDate = self.get_PackageSurgicalStock(y)
                        goodsItemCode = self.getPackageSurgicalStockDetails(packageSurgicalId, expirationDate,
                                                                            status='put_on_shelf')
                        if goodsItemCode != []:
                            # 取物资条码第一个
                            self.pick_pickOrder(goodsItemCode[0], j, z)

                    # # 先直接在商品库存查询数据
                    # # 查询商品id
                    # goodsId, expirationDate, lotNum = self.get_RepositoryStockWithPage(y)
                    # # 若查出数据为空时，转定数包查
                    # if goodsId == []:
                    #     # 查询定数包信息
                    #     packageId, expirationDate = self.get_PackageBulkStock(y)
                    #     goodsItemCode = self.getPackageBulkStockDetails(packageId, expirationDate,
                    #                                                     status='put_on_shelf')
                    #     if goodsItemCode != []:
                    #         # 取物资条码第一个
                    #         self.pick_pickOrder(goodsItemCode[0], j, z)
                    # else:
                    #     # 物资条码列表
                    #     goodsItemCode = self.getStockDetails(goodsId, expirationDate, lotNum, status='put_on_shelf')
                    #     if goodsItemCode != []:
                    #         # 取物资条码第一个
                    #         self.pick_pickOrder(goodsItemCode[0], j, z)

    def aoto_add_pickOrder(self, goodsName, type='goods'):
        """
        自动生成拣货单
        :param goodsName: 物资名称
        :return:
        """
        pickPending_id = self.get_pickPending(goodsName, type)
        for i in pickPending_id:
            self.add_pickOrder(i)

        return pickPending_id

    def printPickOrder(self, id=None):
        """
        @Author   : 蓦然
        打印拣货单
        :param id 拣货单id
        """
        params = {
            'id': id
        }
        response = request.get_params('/api/admin/pickOrder/1.0/printPickOrder', params=params)
        print(response)
        return response

    def batchGeneratePickOrder(self, warehouseIds):
        """
        @Author   : 蓦然
        根据仓库批量生成拣货单
        : body  warehouseIds 仓库id_list
        """
        body = {
            "warehouseIds": warehouseIds,
        }
        response = request.post_body('/api/admin/pickOrder/1.0/batchGeneratePickOrder', body=body)
        print(response)
        return response

    def cancelPickOrder(self, pickOrderId):
        """
        @Author   : 蓦然
        取消拣货单
        """
        response = request.post('/api/admin/pickOrder/1.0/cancelPickOrder/{}'.format(pickOrderId))
        return response

    def complete(self, pickorderid):
        """
        @Author   : 蓦然
        提前完成拣货单 : 拣货单内没有全部拣货时,调用此接口提前完成拣货单,生成推送单
        """
        response = request.post('/api/admin/pickOrder/1.0/complete/{}'.format(pickorderid))
        return response

    def aoto_putOnShelf(self, storageLocation, goods_name, type='commodity'):
        """
        自动上架
        :param goodsId: 商品id
        :param storageLocation: 货位号
        :return:
        """
        if type == 'commodity':
            # 失效日期   #商品
            goodsId, expirationDate, lotNum = self.get_RepositoryStockWithPage(goods_name)
            for x, y in zip(goodsId, storageLocation):
                while self.getStockDetails(x, expirationDate, lotNum) != []:
                    self.putOnShelf(self.getStockDetails(x, expirationDate, lotNum)[0], y)
        elif type == 'bag':
            # 失效日期   #定数包
            packageId, expirationDate = self.get_PackageBulkStock(goods_name)
            while self.getPackageBulkStockDetails(packageId, expirationDate) != []:
                self.putOnShelf(self.getPackageBulkStockDetails(packageId, expirationDate)[0], storageLocation)
        elif type == 'pkg':
            # 失效日期   #手术套包
            packageSurgicalId, expirationDate = self.get_PackageSurgicalStock(goods_name)
            while self.getPackageSurgicalStockDetails(packageSurgicalId, expirationDate) != []:
                self.putOnShelf(self.getPackageSurgicalStockDetails(packageSurgicalId, expirationDate)[0],
                                storageLocation)


# 加工组包
class processing_package:

    def __init__(self):
        self.stock = stock()

    def getWithPage(sele, code, statusList=None):
        """
        加工组包页面查询
        :return: 获取加工单号id列表， 拣货单号和id
        """
        params = {
            "pageNum": 0,
            "pageSize": 500,
            "statusList": statusList
        }
        response = request.get_params('/api/admin/processingOrder/1.0/getWithPage', params)

        # 加工单号id
        return [i['id'] for i in response['data']['rows'] if code in i['description']], \
               [i['pickOrderCode'] for i in response['data']['rows'] if code in i['description']], \
               [i['pickOrderId'] for i in response['data']['rows'] if code in i['description']], \
               [i['description'] for i in response['data']['rows'] if code in i['description']]  # 拣货单号和id

    def getOne(self):
        """
        查询详情
        :return:
        """
        params = {
            "processingOrderId": 1
        }
        request.get_params('/api/admin/processingOrder/1.0/getOne', params=params)

    def makingProcessingOrder(self, packageBulkId):
        """
        制作加工单
        :return:
        """
        body = [{
            "quantity": 1,
            "packageBulkId": packageBulkId
        }]
        response = request.post_body('/api/admin/processingOrder/1.0/makingProcessingOrder', body=body)

        return response['data']

    def removeProcessingOrder(self, processingOrderId):
        """
        删除加工单
        :return:
        """
        request.delete('/api/admin/processingOrder/1.0/removeProcessingOrder/{processingOrderId}'.format(
            processingOrderId=processingOrderId))

    def generatePickingPendingOrder(self, processingOrderId):
        """
        生成拣货单号
        :param processingOrderId: 加工单id
        :return:
        """
        body = {
            "processingOrderId": processingOrderId
        }
        request.post_body('/api/admin/processingOrder/1.0/generatePickingPendingOrder', body)

    def loadPackageBulkDetailsInOne(self, processingOrderId):
        """
        定数包--查询加工赋码明细
        :param processingOrderId: 加工单id
        :return: 加工赋码明细id
        """
        params = {
            "processingOrderId": processingOrderId
        }
        response = request.get_params('/api/admin/processingOrder/1.0/loadPackageBulkDetailsInOne', params)

        return response['data']['details'][0]['packageBulkId']

    def loadPackageBulkDetails(self, processingOrderId):
        """
        加载定数包加工信息
        :return:
        """
        params = {
            "processingOrderId": processingOrderId
        }
        request.get_params('/api/admin/processingOrder/1.0/loadPackageBulkDetails', params=params)

    def loadSurgicalPkgBulkDetailsInOne(self, processingOrderId):
        """
        手术套包--查询加工赋码明细
        :param processingOrderId: 加工单id
        :return: 加工赋码明细id
        """
        params = {
            "processingOrderId": processingOrderId
        }
        response = request.get_params('/api/admin/processingOrder/1.0/loadSurgicalPkgBulkDetailsInOne', params)

        return response['data']['details'][0]['surgicalPkgBulkId']

    def loadSurgicalPkgBulkDetails(self, processingOrderId):
        """
        加载手术套包加工信息
        :return:
        """
        params = {
            "processingOrderId": processingOrderId
        }
        request.get_params('/api/admin/processingOrder/1.0/loadSurgicalPkgBulkDetails', params=params)

    def makingPackageBulk(self, packageBulkId, processingOrderId):
        """
        加工赋码明细制作
        :param packageBulkId: 加工赋码明细id
        :param processingOrderId: 加工单id
        :return:
        """
        body = {
            "packageBulkId": packageBulkId,
            "processingOrderId": processingOrderId
        }
        response = request.post_body('/api/admin/processingOrder/1.0/makingPackageBulk', body)

    def getAllDetails(self, surgicalPkgBulkId):
        """
        查询手术套包制作详情
        :param surgicalPkgBulkId: 手术套包明细id
        :return: 返回商品名成列表
        """
        response = request.get('/api/admin/packageSurgical/1.0/getAllDetails/{}'.format(surgicalPkgBulkId))

        return [i['goodsName'] for i in response['data']['packageSurgicalGoods']]

    def batchMakingPackageBulk(self):
        """
        批量制作定数包
        :return:
        """
        body = {
            "packageBulkId": 0,
            "packageBulkIds": [
                0
            ],
            "processingOrderId": 0
        }
        request.get_body('/api/admin/processingOrder/1.0/batchMakingPackageBulk', body=body)

    def loadUnpacked(self, processOrderId):
        """
        查询拣货详情
        :return:m 需要展示制作的物资条码
        """
        params = {
            'processOrderId': processOrderId
        }
        response = request.get_params('/api/admin/processingOrder/1.0/loadUnpacked', params=params)

        return {i['goodsName']: i['operatorBarcode'] for i in response['data']}

    def getPackageSurgicalGoods(self, code, processOrderId):
        """
         手术套包扫码制作
        :param code: 物资条码
        :param processOrderId: 加工单id
        :return:
        """
        params = {
            "code": code,
            "processOrderId": processOrderId
        }
        response = request.get_params('/api/admin/processingOrder/1.0/getPackageSurgicalGoods', params)

    def makingSurgicalPkgBulk(self, goodsItemIds, processingOrderId, surgicalPkgBulkId):
        """
        手术套包扫码组包提交
        :param goodsItemIds: 商品列表
        :param processingOrderId: 加工单id
        :param surgicalPkgBulkId: 加工赋码明细id
        :return:
        """
        body = {
            "goodsItemIds": goodsItemIds,
            "processingOrderId": processingOrderId,
            "surgicalPkgBulkId": surgicalPkgBulkId
        }
        response = request.post_body('/api/admin/processingOrder/1.0/makingSurgicalPkgBulk', body)

    def aoto_makingPackageBulk(self, code):
        """
        自动加工赋码
        :param code:
        :return:
        """
        processingOrderId, pickOrder_code, pickOrder_id, description = self.getWithPage(code, 'process_pending')
        for x, y in zip(processingOrderId, description):
            if 'Lowbag' in y:
                packageBulkId = self.loadPackageBulkDetailsInOne(x)
                self.makingPackageBulk(packageBulkId, x)
            elif 'Pkg' in y:
                # 便利加工单id
                # 加工赋码明细id
                surgicalPkgBulkId = self.loadSurgicalPkgBulkDetailsInOne(x)
                # goodsName = self.getAllDetails(surgicalPkgBulkId)
                loadUnpacked_list = self.loadUnpacked(x)
                # 物资详情id
                goodsItemId_list = []
                for j in loadUnpacked_list.keys():
                    # 查询库存列表
                    goodsId, expirationDate, lotNum = stock().get_RepositoryStockWithPage(j)
                    # 查询库存明细
                    goodsItemCode, goodsItemId = stock().getStockDetails(goodsId, expirationDate, lotNum,
                                                                         status='picked')
                    if loadUnpacked_list[j] in goodsItemCode:
                        new_goodsItemId = goodsItemId[goodsItemCode.index(loadUnpacked_list[j])]
                        goodsItemId_list.append(new_goodsItemId)
                    # 扫码制作手术套包
                    self.getPackageSurgicalGoods(loadUnpacked_list[j], x)
                    # 扫码完成确认
                self.makingSurgicalPkgBulk(goodsItemId_list, x, surgicalPkgBulkId)

    def aoto_processingOrder(self, code):
        """
        定数包 - 自动
        :return:
        """
        # 获取加工单id
        processingOrderId, pickOrder_code, pickOrder_id, description = self.getWithPage(code)
        for i in processingOrderId:
            # 生成拣货单
            self.generatePickingPendingOrder(i)

        # 获取拣货单信息
        processingOrderId, pickOrder_code, pickOrder_id, description = self.getWithPage(code)
        print('加工包拣货单号{}'.format(pickOrder_code))
        self.stock.aoto_pick_pickOrder(code, pickOrder_code, pickOrder_id)


# 中心库 推送
class Delivery:

    # 查出推送单ID
    def get_deliveryId(self, departmentId):
        """
        :param departmentId: 科室ID
        :param warehouseId: 仓库ID
        """
        deliveryId = []
        codeList = []
        for i in departmentId:
            params = {
                'pageNum': 0,
                'pageSize': 20,
                'departmentIds': i
                # 'status': status, #订单状态
            }
            response = request.get_params('/api/admin/deliveryOrder/1.0/list', params=params)

            # 这里如果 定数包和商品都有的话 接口返回的格式不一样了，ID code 需要重新取一次
            for i in response['data']['rows']:
                deliveryId.append(i['id'])
                codeList.append(i['code'])
            # 拣货单code
            # codeList.append(response['data']['rows'][0]['code'])
            # print('推送单ID：--%s' % deliveryId)
            print(deliveryId)
        return deliveryId, codeList

    # 查出itemsID
    def get_itemsId(self, deliveryId):
        """
        :param deliveryId: 推送单id
        :return:
        """
        itemsIds = []
        for i in deliveryId:
            params = {
                'deliveryId': i
            }
            response = request.get_params('/api/admin/deliveryOrder/1.0/detail', params=params)
            itemId = []
            for j in response['data']['detail']:
                itemId.append(j['id'])
            itemsIds.append(itemId)
            # print('itemsId:%s' % itemsIds)
        return itemsIds

    # 批量复核
    def batch_check(self, deliveryId, itemsIds):
        """
        :param deliveryId: 推送单id
        :param itemsIds: items id
        :return:
        """
        for i, j in zip(deliveryId, itemsIds):
            body = {
                "deliveryOrderId": i,
                "status": "pass",
                "itemsIds": j
            }
            response = request.post_body('/api/admin/deliveryOrder/1.0/batchCheck', body=body)
            try:
                response['msg'] == '操作成功'
            except:
                raise Exception(response)

    # 复核推送单
    def set_pusher(self, deliveryId):
        for i in deliveryId:
            body = {
                "pusherId": 15,
                "deliveryOrderId": i
            }
            response = request.post_body('/api/admin/deliveryOrder/1.0/setPusher', body=body)
            try:
                response['msg'] == '操作成功'
            except:
                raise Exception(response)

    def check(self, code, deliveryOrderId):
        """
        推送单复核
        :param code: 物资条码
        :param deliveryOrderId: 推送单id
        :return:
        """
        body = {
            "code": "ID_0001_0227_10455",
            "deliveryOrderId": 70,
            "status": "pass"
        }
        response = request.post_body('/api/admin/deliveryOrder/1.0/check', body=body)

        return response['data'].get('id')

    def uncheck(self, id):
        """
        推送单撤销复核
        :param id: 推送单明细id
        :return:
        """
        body = {
            "id": id
        }
        request.post_body('/api/admin/deliveryOrder/1.0/uncheck', body=body)

    def printDeliveryOrder(self, deliveryId):
        """
        推送单复核
        :param deliveryId: 推送单id
        :return:
        """
        params = {
            "deliveryId": deliveryId
        }
        request.get_params('/api/admin/deliveryOrder/1.0/printDeliveryOrder', params=params)

    def export(self):
        """
        推送单导出
        :return:
        """
        request.get('/api/admin/deliveryOrder/1.0/export')

    def all(self, departmentId):
        """
        :param departmentId: 科室ID
        :return:
        """
        allList = self.get_deliveryId(departmentId)
        # 获取 推送单ID
        deliveryId = allList[0]
        # 获取 推送单 code
        codeList = allList[1]
        # 获取 itemsId
        itemsIds = self.get_itemsId(deliveryId)
        # 批量 复核商品
        self.batch_check(deliveryId, itemsIds)
        # 复核 推送单
        self.set_pusher(deliveryId)
        return codeList


# 扫码消耗
class consume(stock):

    def batchConsume(self, operatorBarcode):
        """
        批量扫码消耗
        :param operatorBarcode: 物资条码
        :return:
        """
        body = {
            "operatorBarcode": operatorBarcode
        }
        response = request.post_body('/api/admin/consume/1.0/batchConsume', body=body)

    def consume(self, barcode):
        """
        # 扫码消耗
        :param barcode: 物资条码
        :return:
        """
        body = {
            "adviceId": 1,
            "barcode": barcode
        }
        respomse = request.post_body('/api/admin/consume/1.0/consume', body=body)

    def search(self, operatorBarcode):
        """
        # 查询物资（商品、套包）
        :param operatorBarcode:物资条码
        :return:
        """
        params = {
            'operatorBarcode': operatorBarcode,
            'related': True
        }
        request.get_params('/api/admin/consume/1.0/search', params=params)

    def searchAndConsume(self, operatorBarcode):
        """
        查询并消耗
        :param operatorBarcode: 物资条码
        :return:
        """
        body = {
            "operatorBarcode": operatorBarcode,
            "related": False
        }
        request.post_body('/api/admin/consume/1.0/searchAndConsume', body=body)

    def getGoodsConsumeWithPage(self):
        """
        分页查询商品消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/getGoodsConsumeWithPage', params=params)

    def exportGoodsConsume(self):
        """
        导出商品消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/exportGoodsConsume', params=params)

    def getPackageBulkConsumeWithPage(self):
        """
        分页查询定数包消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/getPackageBulkConsumeWithPage', params=params)

    def exportPackageBulkConsume(self):
        """
        导出定数包消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/exportPackageBulkConsume', params=params)

    def getSurgicalPackageConsumeWithPage(self):
        """
        # 分页查询手术套包消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/getSurgicalPackageConsumeWithPage', params=params)

    def exportSurgicalPackageConsume(self):
        """
        导出手术套包消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/exportSurgicalPackageConsume', params=params)

    def getConsumeDetails(self):
        """
        查询消耗记录详情
        :return:
        """
        params = {
            'goodsItemId': 0,
            'packageBulkItemId': 50,
            'surgicalPackageBulkItemId': 0
        }
        request.get_params('/api/admin/consume/1.0/getConsumeDetails', params=params)

    def batchUnconsume(self, operatorBarcode_list):
        """
        批量扫码反消耗
        :operatorBarcode_list: 物资条码列表
        :return:
        """
        body = {
            "operatorBarcode": operatorBarcode_list,
            "reason": "ea ad veniam elit"
        }
        request.post_body('/api/admin/consume/1.0/batchUnconsume', body=body)

    def unconsume(self, barcode):
        """
        扫码反消耗
        :return:
        """
        body = {
            "barcode": barcode,
            "reason": "11111"
        }
        request.post_body('/api/admin/consume/1.0/unconsume', body=body)

    def goodsUnconsumeRecords(self):
        """
        查询商品反消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/goodsUnconsumeRecords', params=params)

    def packageBulkUnconsumeRecords(self):
        """
        查询定数包反消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/packageBulkUnconsumeRecords', params=params)

    def packageSurgicalUnconsumeRecords(self):
        """
        查询手术套包反消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/packageSurgicalUnconsumeRecords', params=params)

    def exportGoodsUnconsumeRecords(self):
        """
        导出商品反消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/exportGoodsUnconsumeRecords', params=params)

    def exportPackageBulkUnconsumeRecords(self):
        """
        导出定数包反消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/exportPackageBulkUnconsumeRecords', params=params)

    def exportPackageSurgicalUnconsumeRecords(self):
        """
        导出手术套包反消耗记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/consume/1.0/exportPackageSurgicalUnconsumeRecords', params=params)

    def getPackageBulkUnconsumeDetail(self):
        """
        查询定数包反消耗明细
        :return:
        """
        params = {
            'id': 1
        }
        request.get_params('/api/admin/consume/1.0/getPackageBulkUnconsumeDetail', params=params)

    def getPackageSurgicalUnconsumeDetail(self):
        """
        查询手术套包反消耗明细
        :return:
        """
        params = {
            'id': 0
        }
        request.get_params('/api/admin/consume/1.0/getPackageSurgicalUnconsumeDetail', params=params)


# 中心库退货
class returnGoods(stock, all_check.returnGoods):

    def search(self, code):
        """
        根据物资条码查询出商品信息
        :param code: 物资条码
        :return:
        """
        params = {
            "code": code,
            "warehouseId": 1
        }
        response = request.get_params('/api/admin/returnGoods/1.0/search', params=params)

        return response['data']['goodsItemId']

    def makeReturnGoods(self, goodsItemId_list):
        """
        中心库发起退货
        :param goodsItemId_list: 退货单商品明细id
        :return:
        """
        body = {
            "details": [],
            "warehouseId": 1
        }
        for i in goodsItemId_list:
            body['details'].append(
                {
                    "attachments": [],
                    "goodsItemId": i,
                    "quantity": 1,
                    "returnReason": "non_quality_problem"
                }
            )

        response = request.post_body('/api/admin/returnGoods/1.0/makeReturnGoods', body=body)

    # ====================================================================================================================

    def returningGoods(self, operatorBarcode, returnGoodsCode):
        """
        中心库扫码退货
        :param operatorBarcode: 物资条码
        :param returnGoodsCode: 退货单条码
        :return:
        """
        body = {
            "operatorBarcode": operatorBarcode,
            "returnGoodsCode": returnGoodsCode
        }
        response = request.post_body_01('/api/admin/returnGoods/1.0/returningGoods', body=body)

    # ==================================================================================================================

    def aoto_makeReturnGoods(self, name, supplierid):
        """
        中心库自动退货
        :param name: 退货商品名称
        :param supplierid: 供应商id
        :return:
        # @Author   : 蓦然
        """
        code_list = []
        # 查询物资id
        goodsId, expirationDate, lotNum = self.get_RepositoryStockWithPage(name)
        for id in goodsId:
            # 查询所有物资条码
            code_list += self.getStockDetails(id, expirationDate, lotNum, status='put_on_shelf')

        goodsItemId_list = []
        for code in code_list:
            # 根据商品条码, 获取明细id
            goodsItemId_list.append(self.search(code))

        # 中心库发起退货
        self.makeReturnGoods(goodsItemId_list)

        # 查询退货单id
        returnGoodsId = self.getWithPage(suppliers=supplierid, level=0)
        for j in returnGoodsId:
            # 审核
            self.approve(j)
            # 查询退货单详情商品id
            returnGoodsItemId, returnGoodsCode = self.getDetailsSeparated(j)
            for i in code_list:
                # 中心库扫码退货
                self.returningGoods(i, returnGoodsCode)


class logicStockTakingOrder:
    # 逻辑库盘库

    def add(self, warehouseId):
        """
        新增逻辑库盘库单
        :return:
        """
        body = {
            "warehouseId": warehouseId,
            "stockTakingOperator": 19
        }
        response = request.post_body('/api/admin/logicStockTakingOrder/1.0/add', body=body)

        return response['data']

    def delete(self, orderId):
        """
        删除逻辑库盘库单
        :return:
        """
        request.delete('/api/admin/logicStockTakingOrder/1.0/delete/{orderId}'.format(orderId=orderId))

    def submit(self, id):
        """
        提交逻辑库盘库单
        :return:
        """
        body = {
            "detail": [],
            "id": id
        }
        request.put_body('/api/admin/logicStockTakingOrder/1.0/submit', body=body)

    def approvalSuccess(self, id):
        """
        逻辑库盘库单审核通过
        :return:
        """
        request.put('/api/admin/logicStockTakingOrder/1.0/approvalSuccess/{id}'.format(id=id))

    def approvalFailure(self, id):
        """
        逻辑库盘库单审核不通过
        :return:
        """
        body = {
            "id": id,
            "reason": "1"
        }
        request.put_body('/api/admin/logicStockTakingOrder/1.0/approvalFailure', body=body)

    def pageList(self):
        """
        查询逻辑库盘库单列表
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/logicStockTakingOrder/1.0/pageList', params=params)

    def get_id(self, id):
        """
        查询逻辑库盘库单
        :return:
        """
        request.get('/api/admin/logicStockTakingOrder/1.0/get/{id}'.format(id=id))

    def print(self, id):
        """
        打印逻辑库盘库单
        :return:
        """
        request.get('/api/admin/logicStockTakingOrder/1.0/print/{id}'.format(id=id))


class logicStockOperation:
    # 逻辑库库存日志

    def pageList(self):
        """
        分页查询库存日志
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/logicStockOperation/1.0/pageList', params=params)

    def export(self):
        """
        库存日志导出
        :return:
        """
        request.get('/api/admin/logicStockOperation/1.0/export')

    def process(self):
        """
        手工处理
        :return:
        """
        body = {
            "add": True,
            "goodsId": 1,
            "quantity": 1,
            "stockOperationId": 1
        }
        request.post_body('/api/admin/logicStockOperation/1.0/process', body=body)


class logicStock:
    # 逻辑仓库库存分页查询

    def pageList(self):
        """
        逻辑仓库库存分页查询
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/logicStock/1.0/pageList', params=params)

    def export(self):
        """
        逻辑库库存导出
        :return:
        """
        request.get('/api/admin/logicStock/1.0/export')


class unprocessedCount:
    # pda待办任务

    def getCount(self):
        """
        # pda待办任务数量
        :return:
        """
        request.get('/api/admin/unprocessedCount/1.0/getCount')


if __name__ == '__main__':
    # # 定数包加工组包
    # # package = processing_package()
    # # # # 定数包-生成拣货单
    # # # package.aoto_processingOrder('05112')
    # # # # 定数包-拣货
    # # # stock().aoto_add_pickOrder('05112', type='package_bulk')
    # # returnGoods().aoto_makeReturnGoods('051313', '12')
    # test = stock()
    # # test.aoto_putOnShelf(['ow-052039','Low-052039','High-052039'],'052039')
    # test.aoto_add_pickOrder('052039')
    # test.aoto_pick_pickOrder('052039')
    # stock().aoto_printPickOrder(1218)
    # stock().aoto_batchGeneratePickOrder(warehouseIds=[1, 3])
    # stock().aoto_cancelPickOrder(1218)
    stock().aoto_putOnShelf('1', '0610153636')
