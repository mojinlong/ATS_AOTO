#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/6/4 9:55 
# @Author   : 蓦然
# @File     : pda.py
# Project   : integration-tests-insight
import jsonpath

import request, random


# PDA待办任务数量总数查询
def PdaGetCount():
    response = request.get('/api/admin/unprocessedCount/1.0/getCount')
    print(response)
    return response


if __name__ == '__main__':
    PdaGetCount()
