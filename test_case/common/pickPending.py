#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/6/4 10:25 
# @Author   : 蓦然
# @File     : pickPending.py
# Project   : integration-tests-insight
import jsonpath

import request, random


class pick():

    def pickPendingCancel(self, pid):
        """
            取消待拣货数据
            body : id
        """
        body = {
            "id": pid
        }
        response = request.post_body('/api/admin/pickPending/1.0/cancel', body=body)
        print(response)
        return response

    def getPickPendinglist(self, departmentIds=None, start=None, end=None, goodsName=None, materialCode=None,
                           source=None, warehouseIds=None, status=None, goodsId=None, packageBulkName=None,
                           sortableColumnName=None,
                           type=None):
        """
            查询待拣货列表
            params : departmentIds
                    start
                    end
                    goodsId
                    goodsName
                    materialCode
                    packageBulkName
                    pageNum
                    pageSize
                    sortList[0].desc
                    sortList[0].nullsLast
                    sortList[0].sortName
                    sortableColumnName
                    source
                    status
                    type
                    warehouseIds
        """
        params = {
            'departmentIds': departmentIds,
            'start': start,
            'end': end,
            'goodsId': goodsId,
            'goodsName': goodsName,
            'materialCode': materialCode,
            'packageBulkName': packageBulkName,
            'pageNum': 0,
            'pageSize': 50,
            'sortList[0].desc': None,
            'sortList[0].nullsLast': None,
            'sortList[0].sortName': None,
            'sortableColumnName': sortableColumnName,
            'source': source,
            'status': status,
            'type': type,
            'warehouseIds': warehouseIds
        }
        response = request.get_params('/api/admin/pickPending/1.0/list', params=params)
        print(response)
        return response


if __name__ == '__main__':
    # pickPendingCancel(298)
    pick().getPickPendinglist(start=1619798400000, end=1622822399999, source='goods_request', goodsName='High05138',
                              materialCode='ID_951010101001_0080', warehouseIds=20, departmentIds=27,
                              status='generate_pick_order_pending', type='goods')
    pick().getPickPendinglist()
