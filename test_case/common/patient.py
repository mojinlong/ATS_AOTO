#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/6/4 9:34 
# @Author   : 蓦然
# @File     : patient.py
# Project   : integration-tests-insight
import jsonpath

import request, random


def selectPatient(pid):
    """
        查询病人信息
    """
    response = request.get('/api/admin/patient/1.0/%s' % pid)
    print(response)
    return response


def getPatientSurgicalRequest(patientId):
    """
        查询病人手术信息
        :params  patientId
    """
    params = {
        'patientId': patientId
    }
    response = request.get_params('/api/admin/patient/1.0/getPatientSurgicalRequest', params=params)
    print(response)
    return response


def getPatientConsumed(patientId):
    """
        查询病人消耗信息
        :params  patientId
    """
    params = {
        'patientId': patientId
    }
    response = request.get_params('/api/admin/patient/1.0/getPatientConsumed', params=params)
    print(response)
    return response


if __name__ == '__main__':
    selectPatient(2)
    getPatientSurgicalRequest(1838)
    getPatientConsumed(1838)
