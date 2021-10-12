#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/1/30 9:37
# @File     : test_smoke.py
# @Project  : integration-tests-insight

from common import createDeparments, addbusiness, createGoods, goodsRequest, createPurchase, centralLibrary, \
    all_Deparments_putOnShelf, all_check, baseData, finance
from test_config.yamlconfig import timeid
import allure
import pytest


# 主流程冒烟测试
@allure.feature('业务流程测试')
@pytest.mark.usefixtures('b_data')
class Test_smoke:

    @allure.title('商品、定数包流程测试--货票同行--有一级供应商')
    def test_Commodity_flow_01(self):
        """
        商品流程测试--货票同行--有一级供应商
        :return:
        """
        name = timeid().id()
        print('流程唯一id:{}'.format(name))
        business = addbusiness.addBusiness(name['core_code'])
        # 生产商
        manufacturer_id = business.createManufacturer('测试生产商')
        # 测试一级供应商
        custodian_id = business.createCustodian('测试一级供应商')
        print('生产商id', manufacturer_id)
        goods = createGoods.createGoods()
        # 商品
        goodsList = goods.addGoods(name['goodsname'], manufacturerId=manufacturer_id)
        print('商品id', goodsList)
        # 定数包
        bagId = goods.createBag(goodsList[-1], name['goodsname']['lowbag'])
        # 供应商
        supplierId, suppliername = business.createSuppliers('测试供应商')
        print('供应商id', supplierId)
        # 科室
        list_data = createDeparments.allCreate(name['departmentname'], name['department_name'])
        print('科室list', list_data)
        # 厂家授权
        business.manufacturerAuthorizations(supplierId, manufacturer_id, goodsList)
        # 一级供应商授权
        business.supplierAuthorization(supplierId, custodian_id, goodsList)
        # 绑定货票同行
        business.setInvoiceSync_and_getsupplierGoods_list(supplierId)
        # 启用商品
        goods.useGoods(goodsList)
        # 启用定数包
        goods.useBag(bagId)
        # 仓库ID
        warehouseData = baseData.warehouseData(list_data, name['code'])
        print('仓库list', warehouseData)
        # 新建中心库货位
        core_warehouseData = baseData.core_warehouseData(name['core_code'])
        print('中心库货位信息{}'.format(core_warehouseData))
        # 科室绑定商品
        goods.setDepartmentGoods(list_data[0], warehouseData[1], goodsList[:3])
        # 科室绑定定数包
        goods.bindBag(list_data[0], warehouseData[1], bagId)
        # 请领流程
        goodsRequest.Request().all(goodsList[:3], warehouseData[1], bagId)
        # 采购流程   返回配送单id
        shippingOrderCode = createPurchase.purchase().oaPurchase(supplierId, custodian_id)
        # 中心库验收
        centralLibrary.receivingOrder().all_receivingOrder(shippingOrderCode)
        # 中心库上架
        stock = centralLibrary.stock()
        stock.aoto_putOnShelf(core_warehouseData, name['core_code'])
        # 中心库生成拣货单
        stock.aoto_add_pickOrder(name['core_code'])
        # 中心库拣货
        stock.aoto_pick_pickOrder(name['core_code'])

        # 定数包加工组包
        package = centralLibrary.processing_package()
        # 定数包-生成拣货单
        package.aoto_processingOrder(name['core_code'])
        # 定数包-拣货
        stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
        # 加工赋码
        package.aoto_makingPackageBulk(name['core_code'])
        # 定数包上架
        stock.aoto_putOnShelf(core_warehouseData[-1], name['core_code'], type='bag')
        # 中心库 生成拣货单
        stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
        # 中心库拣货
        stock.aoto_pick_pickOrder(name['core_code'], type='bag')

        # 中心库推送
        codeList = centralLibrary.Delivery().all(list_data[0])
        print('推送单code: %s' % codeList)
        # 科室验收
        all_check.Check().all(codeList)
        # # 科室上架
        print('仓库id：%s' % warehouseData[1])
        # 上架商品
        goods_code = all_Deparments_putOnShelf.Deparment().all(warehouseData[1])
        # 上架定数包
        package_code = all_Deparments_putOnShelf.Deparment().all1(warehouseData[1])

        # 扫码消耗商品
        centralLibrary.consume().batchConsume(goods_code)
        # 扫码消耗定数包
        centralLibrary.consume().batchConsume(package_code)

        # 发票流程
        invoice = finance.invoice()
        invoiceIdNumber_list, invoiceId_list = invoice.aoto_doCommitInvoiceSync(name['core_code'], suppliername)

        # 科室退货
        goodsItemId_list = all_check.returnGoods().aoto_makeDepartmentReturnGoods(warehouseData[1])
        print(goodsItemId_list)
        # 中心库上架
        stock.aoto_putOnShelf(core_warehouseData, name['core_code'])

        # 中心库退货
        centralLibrary.returnGoods().aoto_makeReturnGoods(name['core_code'], supplierId)

        # 红冲票流程
        invoice.aoto_doCommitInvoiceManual(invoiceId_list)

        assert len(invoice.pageListPayPending(name['core_code'])) == 20

    @allure.title('商品、定数包流程测试--货票同行--无一级供应商')
    def test_Commodity_flow_02(self):
        """
        商品流程测试--货票同行--无一级供应商
        :return:
        """
        name = timeid().id()
        print('流程唯一id:{}'.format(name))
        business = addbusiness.addBusiness(name['core_code'])
        # 生产商
        manufacturer_id = business.createManufacturer('测试生产商')
        print('生产商id', manufacturer_id)
        goods = createGoods.createGoods()
        # 商品
        goodsList = goods.addGoods(name['goodsname'], manufacturerId=manufacturer_id)
        print('商品id', goodsList)
        # 定数包
        bagId = goods.createBag(goodsList[-1], name['goodsname']['lowbag'])
        # 供应商
        supplierId, suppliername = business.createSuppliers('测试供应商')
        print('供应商id', supplierId)
        # 科室
        list_data = createDeparments.allCreate(name['departmentname'], name['department_name'])
        print('科室list', list_data)
        # 厂家授权
        business.manufacturerAuthorizations(supplierId, manufacturer_id, goodsList)
        # 绑定货票同行
        business.setInvoiceSync_and_getsupplierGoods_list(supplierId)
        # 启用商品
        goods.useGoods(goodsList)
        # 启用定数包
        goods.useBag(bagId)
        # 仓库ID
        warehouseData = baseData.warehouseData(list_data, name['code'])
        print('仓库list', warehouseData)
        # 新建中心库货位
        core_warehouseData = baseData.core_warehouseData(name['core_code'])
        print('中心库货位信息{}'.format(core_warehouseData))
        # 科室绑定商品
        goods.setDepartmentGoods(list_data[0], warehouseData[1], goodsList[:3])
        # 科室绑定定数包
        goods.bindBag(list_data[0], warehouseData[1], bagId)
        # 请领流程
        goodsRequest.Request().all(goodsList[:3], warehouseData[1], bagId)
        # 采购流程   返回配送单id
        shippingOrderCode = createPurchase.purchase().oaPurchase(supplierId)
        # 中心库验收
        centralLibrary.receivingOrder().all_receivingOrder(shippingOrderCode)
        # 中心库上架
        # stock = centralLibrary.stock()
        # stock.aoto_putOnShelf(core_warehouseData, name['core_code'])
        # # 中心库生成拣货单
        # stock.aoto_add_pickOrder(name['core_code'])
        # # 中心库拣货
        # stock.aoto_pick_pickOrder(name['core_code'])
        #
        # # 定数包加工组包
        # package = centralLibrary.processing_package()
        # # 定数包-生成拣货单
        # package.aoto_processingOrder(name['core_code'])
        # # 定数包-拣货
        # stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
        # # 加工赋码
        # package.aoto_makingPackageBulk(name['core_code'])
        # # 定数包上架
        # stock.aoto_putOnShelf(core_warehouseData[-1], name['core_code'], type='bag')
        # # 中心库 生成拣货单
        # stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
        # # 中心库拣货
        # stock.aoto_pick_pickOrder(name['core_code'], type='bag')
        #
        # # 中心库推送
        # codeList = centralLibrary.Delivery().all(list_data[0])
        # print('推送单code: %s' % codeList)
        # # 科室验收
        # all_check.Check().all(codeList)
        # # # 科室上架
        # print('仓库id：%s' % warehouseData[1])
        # # 上架商品
        # goods_code = all_Deparments_putOnShelf.Deparment().all(warehouseData[1])
        # # 上架定数包
        # package_code = all_Deparments_putOnShelf.Deparment().all1(warehouseData[1])
        #
        # # 扫码消耗商品
        # centralLibrary.consume().batchConsume(goods_code)
        # # 扫码消耗定数包
        # centralLibrary.consume().batchConsume(package_code)
        #
        # # 发票流程
        # invoice = finance.invoice()
        # invoiceIdNumber_list, invoiceId_list = invoice.aoto_doCommitInvoiceSync(name['core_code'], suppliername)
        # print("发票号码:", invoiceIdNumber_list)
        #
        # # 科室退货
        # goodsItemId_list = all_check.returnGoods().aoto_makeDepartmentReturnGoods(warehouseData[1])
        # print(goodsItemId_list)
        # # 中心库上架
        # stock.aoto_putOnShelf(core_warehouseData, name['core_code'])
        #
        # # 中心库退货
        # centralLibrary.returnGoods().aoto_makeReturnGoods(name['core_code'], supplierId)
        #
        # # 红冲票流程
        # invoice.aoto_doCommitInvoiceManual(invoiceId_list)
        #
        # assert len(invoice.pageListPayPending(name['core_code'])) == 20

    @allure.title('手术套包流程测试--货票同行--无一级供应商')
    def test_Commodity_flow_03(self):
        """
        商品流程测试--货票同行--无一级供应商---添加手术套包
        :return:
        """
        name = timeid().id()
        print('流程唯一id:{}'.format(name))
        business = addbusiness.addBusiness(name['core_code'])
        # 生产商
        manufacturer_id = business.createManufacturer('测试生产商')
        print('生产商id', manufacturer_id)
        goods = createGoods.createGoods()
        # 商品
        goodsList = goods.addGoods(name['goodsname'], manufacturerId=manufacturer_id)
        print('商品id', goodsList)
        # 定数包
        bagId = goods.createBag(goodsList[-1], name['goodsname']['lowbag'])
        # 手术套包
        pkgid, combinedGoodsId = goods.createPkg([goodsList[1], goodsList[2]], name['goodsname']['pkg'])
        # 供应商
        supplierId, suppliername = business.createSuppliers('测试供应商')
        print('供应商id', supplierId)
        # 科室
        list_data = createDeparments.allCreate(name['departmentname'], name['department_name'])
        print('科室list', list_data)
        # 厂家授权
        business.manufacturerAuthorizations(supplierId, manufacturer_id, goodsList)
        # 绑定货票同行
        business.setInvoiceSync_and_getsupplierGoods_list(supplierId)
        # 启用商品
        goods.useGoods(goodsList)
        # 启用定数包
        goods.useBag(bagId)
        # 启用手术套包
        goods.usePkg(pkgid)
        # 仓库ID
        warehouseData = baseData.warehouseData(list_data, name['code'])
        print('仓库list', warehouseData)
        # 新建中心库货位
        core_warehouseData = baseData.core_warehouseData(name['core_code'])
        print('中心库货位信息{}'.format(core_warehouseData))
        # 科室绑定商品
        goods.setDepartmentGoods(list_data[0], warehouseData[1], goodsList[:3])
        # 科室绑定定数包
        goods.bindBag(list_data[0], warehouseData[1], bagId)
        # 科室绑定手术套包
        goods.bindDepartment(list_data[0], warehouseData[1], pkgid)
        # 请领流程
        goodsRequest.Request().all(goodsList=None, warehouseId=warehouseData[1], combinedGoodsId=combinedGoodsId)
        # 采购流程   返回配送单id
        shippingOrderCode = createPurchase.purchase().oaPurchase(supplierId, num=8)
        # 中心库验收
        centralLibrary.receivingOrder().all_receivingOrder(shippingOrderCode)
        # 中心库上架
        stock = centralLibrary.stock()
        stock.aoto_putOnShelf(core_warehouseData, name['core_code'])
        # 中心库生成拣货单
        stock.aoto_add_pickOrder(name['core_code'])
        # 中心库拣货
        stock.aoto_pick_pickOrder(name['core_code'])

        # 定数包加工组包
        package = centralLibrary.processing_package()
        # 定数包-生成拣货单
        package.aoto_processingOrder(name['core_code'])
        # 定数包-拣货
        stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
        # 加工赋码
        package.aoto_makingPackageBulk(name['core_code'])
        # 定数包上架
        stock.aoto_putOnShelf(core_warehouseData[-1], name['core_code'], type='pkg')
        # 中心库 生成拣货单
        stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
        # 中心库拣货
        stock.aoto_pick_pickOrder(name['core_code'], type='pkg')

        # 中心库推送
        codeList = centralLibrary.Delivery().all(list_data[0])
        print('推送单code: %s' % codeList)
        # 科室验收
        all_check.Check().all(codeList)
        # # 科室上架
        print('仓库id：%s' % warehouseData[1])
        # # 上架商品
        # goods_code = all_Deparments_putOnShelf.Deparment().all(warehouseData[1])
        # # 上架定数包
        # package_code = all_Deparments_putOnShelf.Deparment().all1(warehouseData[1])
        #
        # # 扫码消耗商品
        # centralLibrary.consume().batchConsume(goods_code)
        # # 扫码消耗定数包
        # centralLibrary.consume().batchConsume(package_code)
        #
        # # 发票流程
        # invoice = finance.invoice()
        # invoiceIdNumber_list, invoiceId_list = invoice.aoto_doCommitInvoiceSync(name['core_code'],suppliername)
        #
        # # 科室退货
        # goodsItemId_list = all_check.returnGoods().aoto_makeDepartmentReturnGoods(warehouseData[1])
        # print(goodsItemId_list)
        # # 中心库上架
        # stock.aoto_putOnShelf(core_warehouseData, name['core_code'])
        #
        # # 中心库退货
        # centralLibrary.returnGoods().aoto_makeReturnGoods(name['core_code'], supplierId)
        #
        # # 红冲票流程
        # invoice.aoto_doCommitInvoiceManual(invoiceId_list)
        #
        # assert len(invoice.pageListPayPending(name['core_code'])) == 20

    @allure.title('商品、定数包流程测试--销后结算--有一级供应商')
    def test_Commodity_flow_001(self):
        """
        商品流程测试--货票同行--有一级供应商
        :return:
        """
        name = timeid().id()
        print('流程唯一id:{}'.format(name))
        business = addbusiness.addBusiness(name['core_code'])
        # 生产商
        manufacturer_id = business.createManufacturer('测试生产商')
        # 测试一级供应商
        custodian_id = business.createCustodian('测试一级供应商')
        print('生产商id', manufacturer_id)
        goods = createGoods.createGoods()
        # 商品
        goodsList = goods.addGoods(name['goodsname'], manufacturerId=manufacturer_id)
        print('商品id', goodsList)
        # 定数包
        bagId = goods.createBag(goodsList[-1], name['goodsname']['lowbag'])
        # 供应商
        supplierId, suppliername = business.createSuppliers('测试供应商')
        print('供应商id', supplierId)
        # 科室
        list_data = createDeparments.allCreate(name['departmentname'], name['department_name'])
        print('科室list', list_data)
        # 厂家授权
        business.manufacturerAuthorizations(supplierId, manufacturer_id, goodsList)
        # 一级供应商授权
        business.supplierAuthorization(supplierId, custodian_id, goodsList)
        # 启用商品
        goods.useGoods(goodsList)
        # 启用定数包
        goods.useBag(bagId)
        # 仓库ID
        warehouseData = baseData.warehouseData(list_data, name['code'])
        print('仓库list', warehouseData)
        # 新建中心库货位
        core_warehouseData = baseData.core_warehouseData(name['core_code'])
        print('中心库货位信息{}'.format(core_warehouseData))
        # 科室绑定商品
        goods.setDepartmentGoods(list_data[0], warehouseData[1], goodsList[:3])
        # 科室绑定定数包
        goods.bindBag(list_data[0], warehouseData[1], bagId)
        # 请领流程
        goodsRequest.Request().all(goodsList[:3], warehouseData[1], bagId)
        # 采购流程   返回配送单id
        shippingOrderCode = createPurchase.purchase().oaPurchase(supplierId, custodian_id)
        # 中心库验收
        centralLibrary.receivingOrder().all_receivingOrder(shippingOrderCode)
        # 中心库上架
        stock = centralLibrary.stock()
        stock.aoto_putOnShelf(core_warehouseData, name['core_code'])
        # 中心库生成拣货单
        stock.aoto_add_pickOrder(name['core_code'])
        # 中心库拣货
        stock.aoto_pick_pickOrder(name['core_code'])

        # 定数包加工组包
        package = centralLibrary.processing_package()
        # 定数包-生成拣货单
        package.aoto_processingOrder(name['core_code'])
        # 定数包-拣货
        stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
        # 加工赋码
        package.aoto_makingPackageBulk(name['core_code'])
        # 定数包上架
        stock.aoto_putOnShelf(core_warehouseData[-1], name['core_code'], type='bag')
        # 中心库 生成拣货单
        stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
        # 中心库拣货
        stock.aoto_pick_pickOrder(name['core_code'], type='bag')

        # 中心库推送
        codeList = centralLibrary.Delivery().all(list_data[0])
        print('推送单code: %s' % codeList)
        # 科室验收
        all_check.Check().all(codeList)
        # # 科室上架
        print('仓库id：%s' % warehouseData[1])
        # 上架商品
        goods_code = all_Deparments_putOnShelf.Deparment().all(warehouseData[1])
        # 上架定数包
        package_code = all_Deparments_putOnShelf.Deparment().all1(warehouseData[1])

        # 扫码消耗商品
        centralLibrary.consume().batchConsume(goods_code)
        # 扫码消耗定数包
        centralLibrary.consume().batchConsume(package_code)

        # 发票流程
        invoice = finance.invoice()
        invoiceIdNumber_list, invoiceId_list = invoice.aoto_doCommitInvoiceSync(name['core_code'], suppliername)

        # 科室退货
        goodsItemId_list = all_check.returnGoods().aoto_makeDepartmentReturnGoods(warehouseData[1])
        print(goodsItemId_list)
        # 中心库上架
        stock.aoto_putOnShelf(core_warehouseData, name['core_code'])

        # 中心库退货
        centralLibrary.returnGoods().aoto_makeReturnGoods(name['core_code'], supplierId)

        # 红冲票流程
        invoice.aoto_doCommitInvoiceManual(invoiceId_list)

        assert len(invoice.pageListPayPending(name['core_code'])) == 20
