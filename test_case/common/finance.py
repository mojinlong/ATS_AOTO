#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/5/6 17:24
# @File     : finance.py
# @Project  : integration-tests-insight
import pprint

import request
import time


# 发票
class invoice:

    def __init__(self):
        time_now = time.time()
        self.my_time = int(time_now * 1000)
        timeArray = time.localtime(time_now)
        self.otherStyleTime = time.strftime("%m%d%H%M", timeArray)

    def pageListPayPending(self, invoiceCode=None):
        """
        发票待支付列表页面查询
        :param invoiceCode: 发票代码
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "invoiceCode": invoiceCode
        }
        response = request.get_params('/api/admin/fin/invoice/1.0/pageListPayPending', params)

        return response['data']['rows']

    def getInvoiceDetailByInvoiceId(self, invoiceId):
        """
        发票红冲详情查询
        :param invoiceId: 发票id
        :return:
        """
        params = {
            "invoiceId": invoiceId
        }
        response = request.get_params('/api/admin/fin/invoice/1.0/getInvoiceDetailByInvoiceId', params)

        return response['data']

    def getinvoiceSyncPageList(self, goodsName=None):
        """
        开票列表查询
        :param goodsName: 物资名称
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "goodsName": goodsName
        }
        response = request.get_params('/api/admin/fin/invoice/1.0/invoiceSyncPageList', params)

        return [i['shippingOrderItemId'] for i in response['data']['rows']], \
               [i['price'] for i in response['data']['rows']]

    def doCommitInvoiceSync(self, shippingOrderItemId, totalAmount, serialCode, releaseType='manual_invoice'):
        """
        上传发票
        :param shippingOrderItemId: 上传发票id
        :param totalAmount: 发票金额
        :return:  发票id
        """
        time_now = time.time()
        my_time = int(time_now * 1000)
        body = {
            "invoiceDetailDtoList": [{
                "shippingOrderItemId": shippingOrderItemId,
                "quantity": 1
            }],
            "invoiceUploadDto": {
                "title": "大华医院",
                "serialNumber": my_time,
                "serialCode": serialCode,
                "releaseType": releaseType,
                "category": "value_added_tax_invoice",
                "releaseDate": my_time - 100000000,
                "taxRate": "100",
                "totalAmount": totalAmount,
                "invoiceUrl": "/file/2021/05/06/wqC6Ovss4jjmBnBnDUFhDYLm82wci5jk/src=http___cdn.duitang.com_uploads_item_201410_20_20141020162058_UrMNe.jpeg&refer=http___cdn.duitang.jfif",
                "invoiceDetailUrl": ""
            }
        }

        response = request.post_body('/api/admin/fin/invoice/1.0/doCommitInvoiceSync', body)

        return response['data'], my_time

    def approve(self, invoiceId, success=True):
        """
        审核发票
        :param invoiceId: 发票id
        :return:
        """
        body = {
            "invoiceId": invoiceId,
            "success": success
        }

        response = request.post_body('/api/admin/fin/invoice/1.0/approve', body)

    def check(self, invoiceId):
        """
        验收发票
        :param invoiceId: 发票id
        :return:
        """
        body = {
            "invoiceId": invoiceId,
            "success": True
        }

        response = request.post_body('/api/admin/fin/invoice/1.0/check', body)

    def pay(self, enterprise, paymentAmount, invoiceIds):
        """
        发票支付
        :param enterprise: 开票公司--供应商
        :param paymentAmount: 总金额
        :param invoiceIds: 发票id
        :return:
        """
        body = {
            "title": "大华医院",
            "enterprise": enterprise,
            "paymentType": "bank_draft",
            "paymentAmount": paymentAmount,
            "paymentDate": self.my_time,
            "paymentUrl": "/file/2021/05/06/STAXO5KB5ZXBX4tWPjlKz52HHRcYFiSp/src=http___cdn.duitang.com_uploads_item_201410_20_20141020162058_UrMNe.jpeg&refer=http___cdn.duitang.jfif",
            "invoiceIds": [invoiceIds]
        }

        response = request.post_body('/api/admin/fin/invoice/1.0/pay', body)

    def doCommitInvoiceManual(self, invoiceId):
        """
        上传红冲发票
        :param invoiceId: 发票id
        :return:
        """
        time_now = time.time()
        my_time = int(time_now * 1000)
        data = self.getInvoiceDetailByInvoiceId(invoiceId)

        body = {
            # 退货商品详情
            "invoiceManualDetailUploadDto": [{
                "shippingOrderItemId": data['detailList'][0]['shippingOrderItemId'],
                "quantity": data['detailList'][0]['passedQuantity']
            }],
            "invoiceUpdateDto": {
                "title": data['invoiceDto']['title'],
                "serialNumber": my_time,
                "serialCode": data['invoiceDto']['serialCode'],
                "releaseType": data['invoiceDto']['releaseType'],
                "category": data['invoiceDto']['category'],
                "releaseDate": my_time - 100000000,
                "taxRate": data['invoiceDto']['taxRate'],
                # 红冲发票金额
                "totalAmount": -data['invoiceDto']['totalAmount'],
                # 原发票号码
                "sourceInvoiceNumber": data['invoiceDto']['serialNumber'],
                "invoiceUrl": "/file/2021/05/07/gLIPXUKPdIvIax7XX4v4A9B2vol44mhn/src=http___cdn.duitang.com_uploads_item_201410_20_20141020162058_UrMNe.jpeg&refer=http___cdn.duitang.jfif",
                "invoiceDetailUrl": ""
            },
            "sourceId": data['invoiceDto']['id']
        }

        response = request.post_body('/api/admin/fin/invoice/1.0/doCommitInvoiceManual', body)

        return response['data']

    def aoto_doCommitInvoiceSync(self, goodsName, enterprise, releaseType='manual_invoice', type='sync',
                                 statementId=None):
        """
        发票流程
        :param goodsName: 商品名称
        :param enterprise: 开票公司--供应商
        :return:
        """
        # 发票号码
        invoiceIdNumber_list = []
        invoiceId_list = []
        if type == 'sync':
            # 查询发票信息
            shippingOrderItemId, totalAmount = self.getinvoiceSyncPageList(goodsName)
            x_list, y_list = shippingOrderItemId, totalAmount
        elif type == 'finStates':
            # 分页获取销后结算开票列表
            goodsItemId, totalAmount = self.invoiceFinStatesPageList(goodsName)
            x_list, y_list = goodsItemId, totalAmount
        else:
            return Exception('货票同行或销后结算类型为空')

        for x, y in zip(x_list, y_list):
            if type == 'sync':
                # 上传发票
                invoiceId, invoiceIdNumber = self.doCommitInvoiceSync(x, y, goodsName, releaseType=releaseType)
            elif type == 'finStates':
                invoiceId, invoiceIdNumber = self.doCommitInvoiceFinState(x, y, goodsName, releaseType=releaseType,
                                                                          statementId=statementId)
            else:
                return Exception('货票同行或销后结算类型为空')

            invoiceIdNumber_list.append(invoiceIdNumber)
            invoiceId_list.append(invoiceId)
            # 审核发票
            self.approve(invoiceId)
            # 验收发票
            self.check(invoiceId)
            # 支付发票
            self.pay(enterprise, y, invoiceId)

        return invoiceIdNumber_list, invoiceId_list

    def aoto_doCommitInvoiceManual(self, invoiceId_list):
        for i in invoiceId_list:
            # 上传红冲发票
            invoiceId = self.doCommitInvoiceManual(i)
            # 审核发票
            self.approve(invoiceId)
            # 验收发票
            self.check(invoiceId)
            # # 支付发票
            # self.pay(enterprise, y, invoiceId)

    def pageListApprovePending(self):
        """
        查询列表--待审核
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/pageListApprovePending', params=params)

    def exportApprovePending(self):
        """
        待审核导出
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/exportApprovePending', params=params)

    def pageListCheckPending(self):
        """
        查询列表--待验收
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/pageListCheckPending', params=params)

    def getEnterpriseList(self):
        """
        获取所有开票企业
        :return:
        """
        request.get('/api/admin/fin/invoice/1.0/getEnterpriseList')

    def exportCheckPending(self):
        """
        待验收导出
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/exportCheckPending', params=params)

    def exportPayPending(self):
        """
        待支付导出
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/exportPayPending', params=params)

    def pageListPayFinished(self):
        """
        查询列表--支付完成
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/pageListPayFinished', params=params)

    def exportPayFinished(self):
        """
        支付完成导出
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/exportPayFinished', params=params)

    def pageListRejected(self):
        """
        查询列表--驳回
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/pageListRejected', params=params)

    def exportRejected(self):
        """
        驳回导出
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/fin/invoice/1.0/exportRejected', params=params)

    def remove(self, invoiceId):
        """
        发票作废
        :param invoiceId: 发票id
        :return:
        """
        body = {
            "invoiceId": invoiceId,
            "reason": "fugiat minim",
            "success": True
        }
        request.delete_body('/api/admin/fin/invoice/1.0/remove', body=body)

    def getNormalInvoiceBySerialNumber(self, serialNumber):
        """
        根据发票号码查询蓝票
        :return:
        """
        params = {
            "serialNumber": serialNumber
        }
        request.get_params('/api/admin/fin/invoice/1.0/getNormalInvoiceBySerialNumber', params=params)

    def electronicReverse(self, invoiceId):
        """
        电子发票红冲
        :return:
        """
        time_now = time.time()
        my_time = int(time_now * 1000)
        data = self.getInvoiceDetailByInvoiceId(invoiceId)

        body = {
            "reverseInvoiceUploadDto": {
                "title": data['invoiceDto']['title'],
                "serialNumber": my_time,
                "serialCode": data['invoiceDto']['serialCode'],
                "releaseType": data['invoiceDto']['releaseType'],
                "category": data['invoiceDto']['category'],
                "releaseDate": my_time - 100000000,
                "taxRate": data['invoiceDto']['taxRate'],
                "totalAmount": -data['invoiceDto']['totalAmount'],
                "sourceInvoiceNumber": data['invoiceDto']['serialNumber'],
                "invoiceUrl": "/file/2021/06/09/tOKcsC5jIvO2Zr4SI7wREcmP1GzNAE5t/a.txt",
                "invoiceDetailUrl": ""
            },
            "resourceId": data['invoiceDto']['id']
        }
        request.post_body('/api/admin/fin/invoice/1.0/electronicReverse', body=body)

    def getInvoiceSummary(self, invoiceId):
        """
        查询发票汇总信息
        :return:
        """
        params = {
            "invoiceId": invoiceId
        }
        response = request.get_params('/api/admin/fin/invoice/1.0/getInvoiceSummary', params=params)

        return response['data']

    def updateElectronicInvoice(self, invoiceId):
        """
        编辑电子发票
        :return:
        """
        data = self.getInvoiceSummary(invoiceId)

        body = {
            "updateInvoiceDetailList": [{
                "shippingOrderItemId": data['detailList'][0]['shippingOrderItemId'],
                "quantity": data['detailList'][0]['quantity']
            }],
            "updateInvoice": {
                "title": data['invoice']['title'],
                "serialNumber": data['invoice']['serialNumber'],
                "serialCode": data['invoice']['serialCode'],
                "releaseType": data['invoice']['releaseType'],
                "category": data['invoice']['category'],
                "releaseDate": data['invoice']['releaseDate'],
                "taxRate": data['invoice']['taxRate'],
                "totalAmount": data['invoice']['totalAmount'],
                "sourceInvoiceNumber": data['invoice']['sourceInvoiceNumber'],
                "invoiceUrl": data['invoice']['invoiceUrl'],
                "invoiceDetailUrl": data['invoice']['invoiceDetailUrl'],
                "invoiceId": invoiceId
            }
        }
        request.post_body('/api/admin/fin/invoice/1.0/updateElectronicInvoice', body=body)

    def updateManualReverseInvoice(self, invoiceId):
        """
        修改手工红冲发票
        :return:
        """
        data = self.getInvoiceSummary(invoiceId)

        body = {
            "updateInvoice": {
                "category": data['invoice']['category'],
                "enterprise": data['invoice']['enterprise'],
                "invoiceDetailUrl": data['invoice']['invoiceDetailUrl'],
                "invoiceId": invoiceId,
                "invoiceUrl": data['invoice']['invoiceUrl'],
                "releaseDate": data['invoice']['releaseDate'],
                "releaseType": data['invoice']['releaseType'],
                "serialCode": data['invoice']['serialCode'],
                "serialNumber": data['invoice']['serialNumber'],
                "taxRate": data['invoice']['taxRate'],
                "title": data['invoice']['title'],
                "totalAmount": data['invoice']['totalAmount'],
                "updateDetails": [
                    {}
                ]
            },
            "updateInvoiceDetailList": [
                {
                    "quantity": data['detailList'][0]['quantity'],
                    "shippingOrderItemId": data['detailList'][0]['shippingOrderItemId']
                }
            ]
        }
        request.post_body('/api/admin/fin/invoice/1.0/updateManualReverseInvoice', body=body)

    def invoiceFinStatesPageList(self, goodsName=None):
        """
        分页获取销后结算开票列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "goodsName": goodsName
        }
        response = request.get_params('/api/admin/fin/invoice/1.0/invoiceFinStatesPageList', params=params)

        return [i['goodsItemId'] for i in response['data']['rows']], \
               [i['price'] for i in response['data']['rows']]

    def doCommitInvoiceFinState(self, goodsItemId, totalAmount, serialCode, releaseType='manual_invoice',
                                statementId=5):
        """
        销后结算发票上传
        :param goodsItemId: goodsItemId
        :param totalAmount: 发票金额
        :param serialCode: 发票代码
        :param releaseType: 发票类型
        :return:
        """
        time_now = time.time()
        my_time = int(time_now * 1000)

        body = {
            "invoiceStateDetailDtoList": [{
                "goodsItemId": goodsItemId,
                "quantity": 1,
                "statementId": statementId
            }],
            "invoiceUploadDto": {
                "title": "Phmedtech医院",
                "serialNumber": my_time,
                "serialCode": serialCode,
                "releaseType": releaseType,
                "category": "value_added_tax_invoice",
                "releaseDate": my_time - 100000000,
                "taxRate": 300,
                "totalAmount": totalAmount,
                "invoiceUrl": "/file/2021/06/09/PHct7dsKCEVxsYtHAZL795hIkHPEDCOH/a.txt",
                "invoiceDetailUrl": ""
            }
        }
        response = request.post_body('/api/admin/fin/invoice/1.0/doCommitInvoiceFinState', body=body)

        return response['data'], my_time

    def getInvoiceFinStateDetail(self):
        """
        销后结算待修改详情
        :return:
        """
        params = {
            "invoiceId": 424
        }
        request.get_params('/api/admin/fin/invoice/1.0/getInvoiceFinStateDetail', params=params)

    def updateInvoiceFinState(self, invoiceId):
        """
        销后结算修改
        :return:
        """
        data = self.getInvoiceSummary(invoiceId)

        body = {
            "updateInvoiceDetailList": [{
                "goodsItemId": data['detailList'][0]['goodsItemId'],
                "quantity": data['detailList'][0]['quantity']
            }],
            "updateInvoice": {
                "title": data['invoice']['title'],
                "serialNumber": data['invoice']['serialNumber'],
                "serialCode": data['invoice']['serialCode'],
                "releaseType": data['invoice']['releaseType'],
                "category": data['invoice']['category'],
                "releaseDate": data['invoice']['releaseDate'],
                "taxRate": data['invoice']['taxRate'],
                "totalAmount": data['invoice']['totalAmount'],
                "sourceInvoiceNumber": data['invoice']['sourceInvoiceNumber'],
                "invoiceUrl": data['invoice']['invoiceUrl'],
                "invoiceDetailUrl": data['invoice']['invoiceDetailUrl'],
                "invoiceId": invoiceId
            }
        }
        request.post_body('/api/admin/fin/invoice/1.0/updateInvoiceFinState', body=body)

    def getInvoiceSyncDetail(self, invoiceId):
        """
        货票同行原票待修改详情
        :return:
        """
        params = {
            "invoiceId": invoiceId
        }
        request.get_params('/api/admin/fin/invoice/1.0/getInvoiceSyncDetail', params=params)

    def updateInvoiceSync(self, invoiceId):
        """
        货票同行原票修改
        :return:
        """
        data = self.getInvoiceSummary(invoiceId)

        body = {
            "updateInvoiceDetailList": [{
                "shippingOrderItemId": data['detailList'][0]['shippingOrderItemId'],
                "quantity": data['detailList'][0]['quantity']
            }],
            "updateInvoice": {
                "title": data['invoice']['title'],
                "serialNumber": data['invoice']['serialNumber'],
                "serialCode": data['invoice']['serialCode'],
                "releaseType": data['invoice']['releaseType'],
                "category": data['invoice']['category'],
                "releaseDate": data['invoice']['releaseDate'],
                "taxRate": data['invoice']['taxRate'],
                "totalAmount": data['invoice']['totalAmount'],
                "sourceInvoiceNumber": data['invoice']['sourceInvoiceNumber'],
                "invoiceUrl": data['invoice']['invoiceUrl'],
                "invoiceDetailUrl": data['invoice']['invoiceDetailUrl'],
                "invoiceId": invoiceId
            }
        }
        request.post_body('/api/admin/fin/invoice/1.0/updateInvoiceSync', body=body)

    def getPaymentDetail(self, invoiceId):
        """
        查看转账凭证
        :return:
        """
        params = {
            "invoiceId": invoiceId
        }
        request.get_params('/api/admin/fin/invoice/1.0/getPaymentDetail', params=params)


class statement:
    # 结算单

    def getStatementWithPage(self, supplierIds):
        """
        结算单一级供应商查询
        :param supplierIds: 供应商id
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "supplierIds": supplierIds
        }
        response = request.get_params('/api/admin/statement/1.0/getStatementWithPage', params=params)

        return [i['id'] for i in response['data']['rows']]

    def commit(self, statementId):
        """
        提交结算单
        :param statementId: 结算单id
        :return:
        """
        body = {
            "statementId": statementId
        }
        request.post_body('/api/admin/statement/1.0/commit', body=body)

    def audit(self, statementList):
        """
        结算单审核
        :param statementList: 结算单id 列表
        :return:
        """
        body = {
            "status": "approval_success",
            "statementList": statementList
        }
        request.post_body('/api/admin/statement/1.0/audit', body=body)

    def review(self, statementId):
        """
        结算单复核
        :param statementId: 结算单id
        :return:
        """
        body = {
            "status": "review_success",
            "statementId": statementId
        }
        request.post_body('/api/admin/statement/1.0/review', body=body)

    def auto_statement(self, supplierIds):
        """
        结算单流程
        :return:
        """
        # 结算单页面查询
        id_list = self.getStatementWithPage(supplierIds)
        # 重新生成结算单
        self.rebuild(id_list[0])
        # 分页显示结算单组
        self.getStatementDetailGroupWithPage(id_list[0])

        # 结算单页面查询
        id_list = self.getStatementWithPage(supplierIds)
        for i in id_list:
            # 结算单提交
            self.commit(i)
        # 结算单审核
        self.audit(id_list)
        for i in id_list:
            # 结算单复核
            self.review(i)

            # 上传发票
            self.uploadReceipt(i)
            # 加载发票
            self.loadReceipt(i)
            # 导出结算单数据
            self.export(i)
            # 获取结算单打印数据
            self.getPrintData(i)
            # 导出托管商结算单
            self.exportCustodianStatementSummary()

        return id_list

    def getStatementDetailGroupWithPage(self, statementId):
        """
        分页显示结算单组
        :return:
        """
        params = {
            "statementId": statementId,
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/statement/1.0/getStatementDetailGroupWithPage', params=params)

    def rebuild(self, statementId):
        """
        重新生成结算单
        :return:
        """
        body = {
            "statementId": statementId
        }
        request.post_body('/api/admin/statement/1.0/rebuild', body=body)

    def uploadReceipt(self, statementId):
        """
        上传发票
        :return:
        """
        body = {
            "statementId": statementId,
            "statementReceiptDtoList": [{
                "urlName": "/file/2021/06/11/Ck1krRkbHWoZH7AzSu73XShCk0NYXZJq/a.txt",
                "originName": "a.txt"
            }]
        }
        request.post_body('/api/admin/statement/1.0/uploadReceipt', body=body)

    def loadReceipt(self, statementId):
        """
        加载发票
        :return:
        """
        params = {
            "statementId": statementId
        }
        request.get_params('/api/admin/statement/1.0/loadReceipt', params=params)

    def export(self, statementId):
        """
        导出结算单数据
        :return:
        """
        params = {
            "statementId": statementId
        }
        request.get_params('/api/admin/statement/1.0/export', params=params)

    def getPrintData(self, id):
        """
        获取结算单打印数据
        :return:
        """
        params = {
            "id": id
        }
        request.get_params('/api/admin/statement/1.0/getPrintData', params=params)

    def exportCustodianStatementSummary(self):
        """
        导出托管商结算单
        :return:
        """
        params = {
            "custodianId": 73,
            "name": "Phmedtech医院2021年05月结算单"
        }
        request.get_params('/api/admin/statement/1.0/exportCustodianStatementSummary', params=params)


class cost:
    # 成本

    def pageList(self):
        """
        分页查询
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/cost/1.0/pageList', params=params)

    def getDetail(self):
        """
        查询成本明细
        :return:
        """
        params = {
            "departmentId": -3873603,
            "goodsId": -3873603,
            "periodId": -3873603,
            "price": -3873603,
            "type": "all"
        }
        request.get_params('/api/admin/cost/1.0/getDetail', params=params)

    def export(self):
        """
        导出
        :return:
        """
        request.get('/api/admin/cost/1.0/export')


class invoicing:
    # 进销存

    def pageList(self):
        # 列表查询
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/invoicing/1.0/pageList', params=params)

    def export(self):
        # 导出
        request.get('/api/admin/invoicing/1.0/export')


if __name__ == '__main__':
    statement().auto_statement(80)
    # invoice().aoto_doCommitInvoiceSync('0609110932', 333,
    #                                  type='finStates', statementId=[5])
