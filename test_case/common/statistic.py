#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/17 19:52
# @File     : statistic.py
# @Project  : integration-tests-insight


import request


class statistic:
    # 报表

    def list(self):
        """
        获取所有可以访问的报表
        :return:
        """
        request.get('/api/admin/statistic/1.0/list')

    def get_id(self):
        """
        获取单个报表的源数据
        :return:
        """
        request.get('/api/admin/statistic/1.0/get/{id}'.format(id=1))

    def query(self):
        """
        查询数据
        :return:
        """
        body = {
            "exportParams": {},
            "pageNum": 0,
            "pageSize": 80700935,
            "params": {},
            "sortList": [
                {
                    "desc": False,
                    "nullsLast": False,
                    "sortName": "consequat"
                },
                {
                    "desc": False,
                    "nullsLast": True,
                    "sortName": "ut aliqua"
                }
            ],
            "templateId": 90349589
        }
        request.post_body('/api/admin/statistic/1.0/query', body=body)

    def export(self):
        """
        导出数据
        :return:
        """
        body = {
            "exportParams": {},
            "pageNum": 57430770,
            "pageSize": -95371764,
            "params": {},
            "sortList": [
                {
                    "desc": False,
                    "nullsLast": False,
                    "sortName": "anim incididunt"
                },
                {
                    "desc": False,
                    "nullsLast": True,
                    "sortName": "magna"
                }
            ],
            "templateId": -893768
        }
        request.post_body('/api/admin/statistic/1.0/export', body=body)


class reagentReport:
    # 试剂库存

    def reagentStockAmount(self):
        """
        分页查询科室试剂库存报表
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/reagentReport/1.0/reagentStockAmount', params=params)

    def exportReagentStockAmount(self):
        """
        导出试剂库存报表
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/reagentReport/1.0/exportReagentStockAmount', params=params)

    def reagentStockRecord(self):
        """
        试剂库存记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/reagentReport/1.0/reagentStockRecord', params=params)

    def exportReagentStockRecord(self):
        """
        "试剂库存记录
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/reagentReport/1.0/exportReagentStockRecord', params=params)


class departmentConsumeSummary:
    # 科室消耗汇总表

    def pageList(self):
        """
        分页查询科室消耗汇总数据
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/departmentConsumeSummary/1.0/pageList', params=params)

    def export(self):
        """
        导出科室消耗汇总报表数据
        :return:
        """
        request.get('/api/admin/departmentConsumeSummary/1.0/export')


class repositoryInBoundSummary:
    # 入库汇总报表

    def pageList(self):
        """
        分页获取入库汇总列表
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/repositoryInBoundSummary/1.0/pageList', params=params)

    def export(self):
        """
        导出入库汇总报表数据
        :return:
        """
        request.get('/api/admin/repositoryInBoundSummary/1.0/export')


class reportDepartment:
    # 科室/医院报表

    def getMonthlyAmount(self):
        """
        查询科室/全院月度金额报表
        :return:
        """
        request.get('/api/admin/report/department/1.0/getMonthlyAmount')

    def getMonthlyGrowth(self):
        """
        查询科室/全院月度消耗的同比和环比
        :return:
        """
        request.get('/api/admin/report/department/1.0/getMonthlyGrowth')

    def getDepartmentCompare(self):
        """
        查询全院科室消耗对照
        :return:
        """
        request.get('/api/admin/report/department/1.0/getDepartmentCompare')

    def getGoodsCompare(self):
        """
        查询科室/全院商品消耗对照
        :return:
        """
        request.get('/api/admin/report/department/1.0/getGoodsCompare')

    def goodsConsumedRank(self):
        """
        查询耗材消耗排名
        :return:
        """
        request.get('/api/admin/report/department/1.0/goodsConsumedRank')

    def monthlyTotalAmount(self):
        """
        各科室耗材采购总金额按月排名
        :return:
        """
        request.get('/api/admin/report/department/1.0/monthlyTotalAmount')

    def getOverBaseDepartment(self):
        """
        查询超过基准值的科室
        :return:
        """
        params = {
            "target": 1
        }
        request.get_params('/api/admin/report/department/1.0/getOverBaseDepartment', params=params)

    def timeConsume(self):
        """
        各个流程之间时间耗时
        :return:
        """
        request.get('/api/admin/report/department/1.0/timeConsume')

    def returnGoodsTimeConsume(self):
        """
        退货流程各环节时间耗时
        :return:
        """
        request.get('/api/admin/report/department/1.0/returnGoodsTimeConsume')

    def getIncrements(self):
        """
        查询新增商品
        :return:
        """
        request.get('/api/admin/report/department/1.0/getIncrements')

    def getDepartmentGrowthCompare(self):
        """
        查询各科室增长率对比
        :return:
        """
        request.get('/api/admin/report/department/1.0/getDepartmentGrowthCompare')

    def getHospitalTotalAmount(self):
        """
        查询医院采购总金额
        :return:
        """
        request.get('/api/admin/report/department/1.0/getHospitalTotalAmount')

    def getDepartmentTotalAmount(self):
        """
        查询各科室采购总金额
        :return:
        """
        request.get('/api/admin/report/department/1.0/getDepartmentTotalAmount')


class reportSupplier:
    # 供应商/一级供应商报表

    def getMonthlyAmount(self):
        """
        查询供应商/一级供应商月度消耗金额
        :return:
        """
        params = {
            "num": 1
        }
        request.get_params('/api/admin/report/supplier/1.0/getMonthlyAmount', params=params)

    def getSupplierConsumeCompare(self):
        """
        查询一级供应商所有供应商消耗对照
        :return:
        """
        request.get('/api/admin/report/supplier/1.0/getSupplierConsumeCompare')

    def getMonthlyGrowth(self):
        """
        查询全院每月消耗的同比、环比
        :return:
        """
        params = {
            "num": 1
        }
        request.get_params('/api/admin/report/supplier/1.0/getMonthlyGrowth', params=params)

    def timeConsume(self):
        """
        供应商耗时查询
        :return:
        """
        request.get('/api/admin/report/supplier/1.0/timeConsume')

    def getIncrements(self):
        """
        查询新增供应商
        :return:
        """
        request.get('/api/admin/report/supplier/1.0/getIncrements')


class reportReturnGoods:
    # 退货统计

    def centralWarehouseReturnGoodsStat(self):
        """
        中心库退货统计
        :return:
        """
        params = {
            'pageNum': 0,
            'pageSize': 50
        }
        request.get_params('/api/admin/report/returnGoods/1.0/centralWarehouseReturnGoodsStat', params=params)

    def export(self):
        """
        导出中心库退货统计
        :return:
        """
        request.get('/api/admin/report/returnGoods/1.0/export')


class reportWarehouse:
    # 仓库报表

    def duration(self):
        """
        仓库人员的平均工作耗时
        :return:
        """
        request.get('/api/admin/report/warehouse/1.0/duration')

    def info(self):
        """
        未知接口
        :return:
        """
        params = {
            "barcode": 'ID_0001_0195_10317'
        }
        request.get_params('/api/admin/report/tracesource/1.0/info', params=params)
