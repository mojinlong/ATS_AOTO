#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/1/27 10:47
# @File     : createPurchase.py
# @Project  : integration-tests-insight

import request
import time, pprint


# 采购管理
class purchase:

    def __init__(self, target_list=None):
        self.target_list = target_list
        self.time_now = int(time.time() * 1000)

    def getWithPage_purchase(self, supplierId, num = 16):
        """
        获取新增的采购计划id
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "parent": False,
            "supplierId": supplierId
        }

        i = 0
        while True:
            response = request.get_params('/api/admin/purchase/1.0/getWithPage', params)
            # 采购计划id_list
            target_list = [i['id'] for i in response['data']['rows'] if i['status'] == 'commit_pending']
            print(target_list)
            time.sleep(5)
            i += 1
            if len(target_list) == num:
                break
            if i >= 10:
                print('当前获取采购计划条数{}'.format(len(target_list)))
                assert (len(target_list) == num)
        return target_list
        return target_list

    def getWithPage_shippingOrder(self, supplierIds):
        """
        查询新增的配送单 code
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "surgicalRequest": False,
            "supplierIds": supplierIds
        }
        response = request.get_params('/api/admin/shippingOrder/1.0/getWithPage', params)
        # 配送单号
        return response['data']['rows'][0]['shippingOrderCode']

    def addPurchasePlan(self, goodsId_list, quantity=2):
        """
        新增采购计划
        @goodsId_list: 商品id_list
        """
        body = {
            "goodsList": []
        }
        for i in goodsId_list:
            body['goodsList'].append({
                "goodsId": i,
                "quantity": quantity
            })
        response = request.post_body('/api/admin/purchase/1.0/addPurchasePlan', body)
        print(response)

        return response['data']

    def doCommit(self, target_list):
        """
        提交采购计划
        """
        body = {
            "target": target_list,
            "status": "approval_pending"
        }

        response = request.post_body('/api/admin/purchase/1.0/doCommit', body)
        print(response)

    def doAudit(self, target_list):
        """
        审核采购计划
        """
        body = {
            "status": "approval_success",
            "target": target_list
        }

        response = request.post_body('/api/admin/purchase/1.0/doAudit', body)
        print(response)

    def convertOrder(self, target_list):
        """
        生成订单
        """
        body = {
            "planIds": target_list,
            "expectedTime": self.time_now
        }
        response = request.post_body('/api/admin/purchase/1.0/convertOrder', body)
        print(response)

    def getList(self, supplierIds=None, custodianIds=None, parent= False):
        """
        查询采购订单id
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "parent": parent,
            "supplierIds": supplierIds,
            "custodianIds": custodianIds
        }
        response = request.get_params('/api/admin/purchaseOrder/1.0/getList', params)
        ids = []
        for i in response['data']['rows']:
            ids.append(i['id'])

        self.id = ids[0]


    def details(self, orderId):
        """
        查询一级供应商采购订单详情id
        """
        params = {
            "orderId": orderId
        }
        response = request.get_params('/api/admin/purchaseOrder/1.0/details', params)

        return [i['id'] for i in response['data']]

    def custodianAcceptOrder(self,supplierId):
        """
        一级供应商接受采购订单
        """
        body = {
            "purchaseOrderId": self.id,
            "items": {},
            "status": "received"
        }
        for i in self.details(self.id):
            body['items'][i] = supplierId
        response = request.post_body('/api/admin/purchaseOrder/1.0/custodianAcceptOrder', body)
        print(response)

    def supplierAcceptOrder(self, supplierId):
        """
        供应商接受采购订单
        """
        self.getList(supplierId)
        body = {
            "purchaseOrderId": self.id,
            "items": {},
            "status": "received"
        }
        response = request.post_body('/api/admin/purchaseOrder/1.0/supplierAcceptOrder', body)
        print(response)

    def _loadShippingData(self, supplierId):
        """
        获取制作配送单单数据
        """
        self.getList(supplierId)
        params = {
            "purchaseOrderId": self.id
        }
        response = request.get_params('/api/admin/shippingOrder/1.0/loadShippingData', params)

        return response['data']['details']

    def makeShippingOrder(self, supplierId):
        """
        获取 - 制作配送单
        """

        loadShippingData = self._loadShippingData(supplierId)
        body = {
            "items": [],
            "orderId": self.id,
            "actionType": "add",
            "deliveryUserName": "spw",
            "deliveryUserPhone": "13097558562",
            "expectedDeliveryDate": self.time_now
        }
        for i in loadShippingData:
            data = {"lotError": False,
                    "lotNum": "11",
                    "productionDate": self.time_now,
                    "sterilizationDate": self.time_now,
                    "required": True,
                    "expirationDate": self.time_now + 100000000000,
                    "quantityError": False,
                    "change": True,
                    "quantityInMin": i['goodsQuantityInPurchase'],
                    "selectNum": i['goodsQuantityInPurchase']
                    }

            body['items'].append({**i, **data})

        request.post_body('/api/admin/shippingOrder/1.0/makeShippingOrder', body)

    def oaPurchase(self, supplierId, custodianIds=None, num = 16):
        # 获取采购计划id
        target_list = self.getWithPage_purchase(supplierId,num)
        # 提交
        self.doCommit(target_list)
        # 审核
        self.doAudit(target_list)
        # 生成订单
        self.convertOrder(target_list)
        try:
            # 查询订单id
            self.getList(supplierId)
        except:
            # 查询一级供应商
            self.getList(custodianIds=custodianIds, parent=True)
            # 一级供应商接受订单
            self.custodianAcceptOrder(supplierId)
            # 查询订单id
            self.getList(supplierId)

        # 接收订单
        self.supplierAcceptOrder(supplierId)
        # 制作配送单
        self.makeShippingOrder(supplierId)

        # 返回配送单id
        return self.getWithPage_shippingOrder(supplierId)


if __name__ == '__main__':
    test = purchase()
    # 新增
    test.addPurchasePlan([204650, 204649, 204648, 204647])
    # # 提交
    # test.doCommit()
    # # 审核
    # test.doAudit()
    # # 生成订单
    # test.convertOrder()
    # # 接收
    # test.supplierAcceptOrder(284)
    # # 制作配送单
    # test.makeShippingOrder(284)
    # print(test.getWithPage_shippingOrder(284))
    # ['DN_0010_0001_210428_0006', 'DN_0010_0001_210428_0005', 'DN_0010_0001_210428_0004']
    print(test.oaPurchase(1534))
