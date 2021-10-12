# -*- coding: utf-8 -*-
# @Time : 2021/1/28 11:01 下午
# @Author : lsj
# @File : all_check.py
import jsonpath

import all_deliveryOrder
import request


# 科室标准验收
class Check:
    # 通过推送单code 获取验收单ID
    def get_acceptanceOrderId(self, codeList):
        acceptanceOrderId = []
        for i in codeList:
            params = {
                'pageNum': 0,
                'pageSize': 20,
                'deliveryOrderCode': i
                # 'status': status, #订单状态
            }
            response = request.get_params('/api/admin/acceptance/1.0/list', params)
            acceptanceOrderId.append(response['data']['rows'][0]['id'])
        # print(acceptanceOrderId)
        return acceptanceOrderId

    # 查询出 itemsId
    def get_itemsId(self, acceptanceOrderId):
        itemsIds = []
        for i in acceptanceOrderId:
            params = {
                'acceptanceOrderId': i
            }
            response = request.get_params('/api/admin/acceptance/1.0/detail', params)
            itemsId = []
            for j in response['data']['items']:
                itemsId.append(j['id'])
            # print(itemsId)
            itemsIds.append(itemsId)
        # print(itemsIds)
        return itemsIds

    # 批量验收
    def check(self, acceptanceOrderId, itemsIds):
        """
        :param acceptanceOrderId: 验收单 ID
        :param itemsIds: items id
        :return:
        """
        for x, y in zip(acceptanceOrderId, itemsIds):
            items = []
            for z in y:
                item = {
                    "id": z,
                    "status": True,
                    "acceptanceConclusion": ""
                }
                items.append(item)
            # print(items)
            body = {
                "id": x,
                "items": items
            }
            response = request.post_body('/api/admin/acceptance/1.0/check', body=body)
            try:
                response['msg'] == '操作成功'
            except:
                raise Exception(response)

    # 提交验收
    def submitOrder(self, acceptanceOrderId):
        """
        :param acceptanceOrderId: 验收单ID
        :return:
        """
        for i in acceptanceOrderId:
            body = {
                'id': i
            }
            response = request.post_body('/api/admin/acceptance/1.0/submitOrder', body=body)
            try:
                response['msg'] == '操作成功'
            except:
                raise Exception(response)

    def printDetail(self, acceptanceOrderId):
        """
        打印验收单
        :return:
        """
        params = {
            "acceptanceOrderId": acceptanceOrderId
        }
        request.get_params('/api/admin/acceptance/1.0/printDetail', params=params)

    def uncheck(self, acceptanceOrderId, id):
        """
        取消验收
        :return:
        """
        body = {
            "acceptanceOrderId": acceptanceOrderId,
            "id": id
        }
        request.post_body('/api/admin/acceptance/1.0/uncheck', body=body)

    def checkOneItem(self, acceptanceOrderId, code):
        """
        单个验收
        :return:
        """
        body = {
            "acceptanceOrderId": acceptanceOrderId,
            "code": code
        }
        request.post_body('/api/admin/acceptance/1.0/checkOneItem', body=body)

    # 科室批量验收 提交标准验收
    def all(self, codeList):
        acceptanceOrderId = self.get_acceptanceOrderId(codeList)
        itemsIds = self.get_itemsId(acceptanceOrderId)
        self.check(acceptanceOrderId, itemsIds)
        self.submitOrder(acceptanceOrderId)


# spw编辑

# 科室库退货
class returnGoods:

    def getWithPage(self, warehouseId=None, suppliers=None, level=1):
        """
        退货列表页面
        :param warehouseId: 仓库id
        :param suppliers: 供应商id
        :param level:  0:中心库退货页面;  1:科室库退货页面
        :return: 退货单号id
        """
        params = {
            'level': level,
            'pageNum': 0,
            'pageSize': 50,
            'warehouseId': warehouseId,
            'suppliers': suppliers
        }
        response = request.get_params('/api/admin/returnGoods/1.0/getWithPage', params)

        return [i['id'] for i in response['data']['rows']]

    def getDetailsSeparated(self, returnGoodsId):
        """
        查询退货单详情
        :param returnGoodsId: 退货单号
        :return: 退货物资明细id
        """
        params = {
            "returnGoodsId": returnGoodsId
        }
        response = request.get_params('/api/admin/returnGoods/1.0/getDetailsSeparated', params)

        return [i['returnGoodsItemId'] for i in response['data']['goodsList']], \
               response['data']['order']['code']

    def listDepartmentReturnable(self, warehouseId):
        """
        科室库发起退货页面查询接口
        :param warehouseId: 仓库ID
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50,
            'warehouseId': warehouseId
        }
        response = request.get_params('/api/admin/returnGoods/1.0/listDepartmentReturnable', params)

        return [i['goodsItemId'] for i in response['data']['rows']], \
               [i['packageBulkItemGoodsId'] for i in response['data']['rows']], \
               [i['packageBulkItemId'] for i in response['data']['rows']], \
               [i['recordId'] for i in response['data']['rows']]

    def approve(self, returnGoodsId):
        """
        审核退货单
        :param returnGoodsId: 退货单号
        :return:
        """
        body = {
            "agree": True,
            "returnGoodsId": returnGoodsId
        }
        response = request.post_body('/api/admin/returnGoods/1.0/approve', body=body)

    def delivered(self, itemsIds, returnGoodsId):
        """
        科室退货确认送达
        :param itemsIds: 退货商品明细id
        :param returnGoodsId: 退货单id
        :return:
        """
        body = {
            "itemsIds": itemsIds,
            "returnGoodsId": returnGoodsId
        }
        response = request.post_body('/api/admin/returnGoods/1.0/delivered', body=body)

    def makeDepartmentReturnGoods(self, goodsItemId, packageBulkItemGoodsId, packageBulkItemId, recordId, warehouseId):
        """
        科室发起退货
        :param goodsItemId:
        :param packageBulkItemGoodsId:
        :param packageBulkItemId:
        :param recordId:
        :param warehouseId:
        :return:
        """
        body = {
            "goodsList": [],
            "packageList": [],
            "surgicalList": [],
            "warehouseId": warehouseId
        }
        for a, b, c, d in zip(goodsItemId, packageBulkItemGoodsId, packageBulkItemId, recordId):
            item = {
                "attachments": [],
                "goodsItemId": a,
                "packageBulkItemGoodsId": b,
                "packageBulkItemId": c,
                "quantity": 1,
                "recordId": d,
                "returnReason": "non_quality_problem"
            }
            body['goodsList'].append(item)

        response = request.post_body('/api/admin/returnGoods/1.0/makeDepartmentReturnGoods', body=body)

    def aoto_makeDepartmentReturnGoods(self, warehouseId_list):
        for warehouseId in warehouseId_list:
            # 查询科室下面的商品
            goodsItemId, packageBulkItemGoodsId, packageBulkItemId, recordId = self.listDepartmentReturnable(
                warehouseId)
            # 发起退货
            self.makeDepartmentReturnGoods(goodsItemId, packageBulkItemGoodsId, packageBulkItemId, recordId,
                                           warehouseId)
            # 查询退货单id
            returnGoodsId = self.getWithPage(warehouseId=warehouseId)
            for i in returnGoodsId:
                # 审核
                self.approve(i)
                # 查询退货单详情商品id
                returnGoodsItemId, returnGoodsCode = self.getDetailsSeparated(i)
                # 科室退货确认送达
                self.delivered(returnGoodsItemId, i)


if __name__ == '__main__':
    # a = Check()
    # acceptanceOrderId = [2994, 2995, 2996, 2997]
    # codeList = ['UL_0103_210430_0064', 'UL_0103_210430_0065', 'UL_0103_210430_0066', 'UL_0103_210430_0067']
    # # a.all(deliveryId, itemsIds)
    # # a.get_acceptanceOrderId(codeList)
    # a.all(codeList)
    # # a.get_itemsId(acceptanceOrderId)

    test = returnGoods()
    test.aoto_makeDepartmentReturnGoods([36, 37, 38, 39])
    # 科室退货
    goodsItemId_list = returnGoods().aoto_makeDepartmentReturnGoods([19, 20, 21, 22])
    print(goodsItemId_list)
