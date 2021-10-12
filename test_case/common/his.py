#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/16 14:51
# @File     : his.py
# @Project  : integration-tests-insight

import pprint

import request


class medicalAdvice:
    # 医嘱收费

    def getWithPage(self):
        """
        分页查询医嘱收费汇总
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/medicalAdvice/1.0/getWithPage', params=params)

    def exportSummary(self):
        """
        导出医嘱收费汇总
        :return:
        """
        request.get('/api/admin/medicalAdvice/1.0/exportSummary')

    def getListByNum(self):
        """
        根据病例号/病人号/医嘱号 查询医嘱列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "adviceNo": 1,
            "hospitalizationNum": 1,
            "patientNo": 1
        }
        request.get_params('/api/admin/medicalAdvice/1.0/getListByNum', params=params)

    def getConsumedGoodsList(self):
        """
        根据医嘱id查询该医嘱上已消耗的物资列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "adviceId": 1,
            "goodsName": 1,
            "manufacturerName": 1
        }
        request.get_params('/api/admin/medicalAdvice/1.0/getConsumedGoodsList', params=params)

    def getMedicalAdviceList(self):
        """
        分页查询医嘱信息(用于手术请领绑定医嘱)
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/medicalAdvice/1.0/getMedicalAdviceList', params=params)

    def getMedicalAdviceWithPage(self):
        """
        分页查询医嘱信息
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/medicalAdvice/1.0/getMedicalAdviceWithPage', params=params)

    def lock(self):
        """
        提交医嘱(锁定)
        :return:
        """
        body = {
            "adviceNo": "Ut ut qui"
        }
        request.post_body('/api/admin/medicalAdvice/1.0/lock', body=body)

    def getMedicalAdviceCharge(self):
        """
        查询医嘱收费详情(用于医嘱编辑)
        :return:
        """
        params = {
            "adviceNo": "magna laboris"
        }
        request.get_params('/api/admin/medicalAdvice/1.0/getMedicalAdviceCharge', params=params)

    def unconsume(self):
        """
        医嘱反消耗
        :return:
        """
        body = {
            "adviceChargeId": -67752902
        }
        request.post_body('/api/admin/medicalAdvice/1.0/unconsume', body=body)


class surgical:
    # 手术管理"

    def pageList(self):
        """
        分页查询手术管理列表
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50
        }
        request.get_params('/api/admin/surgical/1.0/pageList', params=params)

    def getDetail(self):
        """
        查看手术详情,包括手术信息,消耗物资信息
        :return:
        """
        params = {
            "id": 1
        }
        request.get_params('/api/admin/surgical/1.0/getDetail', params=params)

    def exportDetail(self):
        """
        查看手术详情,包括手术信息,消耗物资信息
        :return:
        """
        params = {
            "id": 1
        }
        request.get_params('/api/admin/surgical/1.0/exportDetail', params=params)


class doctor:
    # 医生

    def get_id(self):
        """
        根据id查询医生信息
        :return:
        """
        request.get('/api/admin/doctor/1.0/{id}'.format(id=1))

    def getDoctorSurgicalRequest(self):
        """
        根据医生查询手术请领
        :return:
        """
        params = {
            "pageNum": 0,
            "pageSize": 50,
            "doctorId": 1
        }
        request.get_params('/api/admin/doctor/1.0/getDoctorSurgicalRequest', params=params)


class patient:
    # 病人信息

    def get_id(self):
        """
        根据id查询病人信息
        :return:
        """
        request.get('/api/admin/patient/1.0/{id}'.format(id=1))

    def getPatientSurgicalRequest(self):
        """
        根据病人查询手术请领
        :return:
        """
        params = {
            "patientId": 1
        }
        request.get_params('/api/admin/patient/1.0/getPatientSurgicalRequest', params=params)

    def getPatientConsumed(self):
        """
        查询病人普通消耗
        :return:
        """
        params = {
            "patientId": 1
        }
        request.get_params('/api/admin/patient/1.0/getPatientConsumed', params=params)
