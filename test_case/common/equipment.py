#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/6/30 16:56 
# @Author   : 蓦然
# @File     : equipment.py
# Project   : integration-tests-insight
import request
import os


class equipment:

    def addEquipment(self, equipmentName, assetClassification, equipmentStoragePlace, departmentName, equipmentCode,
                     price, getTime):
        body = {
            "equipmentName": equipmentName,  # 名称
            "assetClassification": assetClassification,  # 资产分类
            "equipmentStoragePlace": equipmentStoragePlace,  # 存放地址
            "departmentName": departmentName,  # 部门
            "equipmentCode": equipmentCode,  # 卡片编号
            "price": price,  # 价格
            "getTime": getTime  # 取得时间

        }
        response = request.post_body('/api/admin/equipment/1.0/add', body=body)
        print(response)
        return response


if __name__ == '__main__':
    eq = equipment()
    eq.addEquipment(equipmentName='键盘', assetClassification='电脑耗材',
                    equipmentStoragePlace='思南路84号', departmentName='游戏部',
                    equipmentCode='EC000001', price=10000000, getTime='1625051226')
