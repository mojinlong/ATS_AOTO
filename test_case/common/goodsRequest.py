# -*- coding: utf-8 -*-
# @Time : 2021/1/27 1:22 下午
# @Author : lsj
# @File : goodsRequest.py
import request, time


class Request:

    # 请领商品 返回请领ID
    def goodsRequest(self, goodsList, warehouseId, bagId=None, combinedGoodsId=None):
        """
        :param goodsList: 商品ID 列表
        :param warehouseId: 仓库ID 列表
        :param bagId: 定数包 ID  int
        :return:
        """
        self.Id = []
        for i in warehouseId:
            body = {
                "warehouseId": i,
                "items": []
            }
            if goodsList != None:
                for j in goodsList:
                    item = {
                        "goodsId": j,
                        "quantity": 1,
                        "reason": ""
                    }
                    body['items'].append(item)
            if bagId != None:
                item = {
                    "packageBulkId": bagId,
                    "quantity": 1
                }
                body['items'].append(item)
            if combinedGoodsId != None:
                item = {
                    "goodsId": combinedGoodsId,
                    "quantity": 1,
                    "reason": ""
                }
                body['items'].append(item)
            response = request.post_body('/api/admin/goodsRequest/1.0/add', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)
            self.Id.append(response['data'])

        return self.Id

    # 修改请领单
    def edit_goodsRequest(self, id_list, goodsList, warehouseId, bagId=None, combinedGoodsId=None):
        """
        :param goodsList: 商品ID 列表
        :param warehouseId: 仓库ID 列表
        :param bagId: 定数包 ID  int
        :return:
        """
        for i, j in zip(warehouseId, id_list):
            body = {
                "warehouseId": i,
                "items": [],
                'id': j
            }
            if goodsList != None:
                for j in goodsList:
                    item = {
                        "goodsId": j,
                        "quantity": 1,
                        "reason": ""
                    }
                    body['items'].append(item)
            if bagId != None:
                item = {
                    "packageBulkId": bagId,
                    "quantity": 1
                }
                body['items'].append(item)
            if combinedGoodsId != None:
                item = {
                    "goodsId": combinedGoodsId,
                    "quantity": 1,
                    "reason": ""
                }
                body['items'].append(item)
            response = request.post_body('/api/admin/goodsRequest/1.0/edit', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    def withdraw(self, id_list):
        """
        请领单撤回
        :param id_list: 请领单id
        :return:
        """
        for i in id_list:
            body = {
                "goodsRequestId": i
            }
            response = request.post_body('/api/admin/goodsRequest/1.0/withdraw', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    def getById(self,id):
        """
        根据id获取请领单信息
        :param id:
        :return:
        """
        params = {
            'id':id
        }
        request.get_params('/api/admin/goodsRequest/1.0/getById',params=params)

    def getByIdAndMessageType(self,id):
        """
        根据id获取请领单信息
        :param id:
        :return:
        """
        params = {
            'id':id,
            'messageType':1
        }
        request.get_params('/api/admin/goodsRequest/1.0/getByIdAndMessageType',params=params)

    def remove(self,goodsRequestId):
        """
        删除请领单
        :param goodsRequestId:
        :return:
        """
        body = {
            'goodsRequestId':goodsRequestId
        }
        request.delete_body('/api/admin/goodsRequest/1.0/remove',body=body)



    # 通过请领ID查出 items id
    def get_allList(self, Id):
        """

        :param Id: 请领单 ID
        :return:
        """
        allList = []
        for x in Id:
            idList = []
            params = {
                'goodsRequestId': x
            }
            response = request.get_params('/api/admin/goodsRequest/1.0/detail', params)
            for i in response['data']:
                idList.append(i['id'])
            allList.append(idList)
        return allList

    # 审核请领  待审核状态
    def goodsApproval(self, allList, idlist=None):
        """
        :param allList: 请领物资ID 列表
        :return:
        """
        if not idlist:
            idlist = self.Id
        bodyList = self.__body(idlist, allList, 'approval_review_pending')
        for body in bodyList:
            response = request.post_body('/api/admin/goodsRequest/1.0/approval', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    # 驳回请领  驳回状态
    def approvalRejct(self, allList, idlist=None):

        if not idlist:
            idlist = self.Id
        bodyList = self.__body(idlist, allList, 'approval_failure')

        for body in bodyList:
            response = request.post_body('/api/admin/goodsRequest/1.0/approval', body=body)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    # 复核请领单 复核通过状态
    def approvalReview(self, allList, idlist=None):
        if not idlist:
            idlist = self.Id
        bodyList = self.__body(idlist, allList, 'approval_review_success')
        for body in bodyList:
            response = request.post_body('/api/admin/goodsRequest/1.0/approvalReview', body=body)
            # time.sleep(2)
            try:
                assert response['msg'] == '操作成功'
            except:
                raise Exception(response)

    def __body(self, idlist, allList, status):
        bodyList = []
        for x, y in zip(idlist, allList):
            body = {
                "id": x,
                "status": status,
                "items": []
            }
            for i in y:
                item = {
                    "id": i,
                    "quantity": 1,
                    "reason": ""
                }
                body['items'].append(item)
            bodyList.append(body)
        return bodyList

    def all(self, goodsList, warehouseId, bagId=None, combinedGoodsId=None):
        # 获取请领单ID
        Id = self.goodsRequest(goodsList, warehouseId, bagId, combinedGoodsId)
        # 获取 物资详情
        allList = self.get_allList(Id)
        # 审核 请领
        self.goodsApproval(allList)
        # 复核 请领
        self.approvalReview(allList)

    # 查询普通请领列表
    def get_list(self):
        """
        # 查询普通请领列表
        """

        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        response = request.get_params('/api/admin/goodsRequest/1.0/list', params)


if __name__ == '__main__':
    a = Request()
    a.get_allList([487])
