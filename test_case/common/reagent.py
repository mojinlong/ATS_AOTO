#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/6/30 14:32 
# @Author   : 蓦然
# @File     : reagent.py
# Project   : integration-tests-insight
import request


class reagent:

    def goods(self):
        body = {
            "name": "红牛条码管控_0701",
            "commonName": "红牛条码管控_0701",
            "pmCode": "红牛条码管控_0701",
            "manufacturerId": 344,  # 生产商
            "brand": "红牛条码管控_0701",
            "specification": "123",
            "model": "1",
            "procurementPrice": "100000000",
            "limitType": "forbid",
            "limitPerMonth": 1000,  # 每月限制
            "nearExpirationDays": 9099,  # 近效期
            "antiEpidemic": "false",
            "materialCategory": "试剂",  # 物资类别
            "storagePlace": "恒温柜",
            "materialActivationTime": 1624982400000,
            "instrument": "显微镜",
            "minGoodsUnitId": "5",
            "purchaseGoodsUnitId": "5",
            "minGoodsNum": 1,
            "isHighValue": "true",
            "isImplantation": "true",
            "isBarcodeControlled": "true",
            "detectionCapacity": 10,  # 检测容量
            "scanCapacity": 1,  # 扫码容量
            "isConsumableMaterial": "true",
            "category": ["Ⅰ", "6801-Ⅰ", "3"],
            "categoryType": "12",
            "lowTemperature": "-10",
            "highTemperature": "10",
            "registrationList": [{
                "registrationBeginDate": 1624982400000,
                "registrationEndDate": "",
                "registrationImg": "/file/2021/06/30/rtKAVXnDeZ0rhImscLOhmXecDp0W80iI"
                                   "/b21c8701a18b87d6b74647d9629a6f301e30fd0f.png",
                "registrationNum": "963253255",
                "registrationDate": "true"
            }],
            "std2012GoodsCategoryId": "3"
        }
        request.post_body('/api/admin/goodsTypes/1.0/add', body=body)


if __name__ == '__main__':
    re = reagent()
    re.goods()