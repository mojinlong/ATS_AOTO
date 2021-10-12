#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/9/10 13:16 
# @Author   : 蓦然
# @File     : wework.py
# Project   : ATS

import request

# api_url = "https://ats-test.51zhaopin.cn"


def authMode():
    url = '/pic/api/wework/authMode'
    response = request.get(url)
    return response['data']['authMode']

authMode()