# _*_ coding: utf-8 _*_
# @Time     : 2021/9/10 10:58 
# @Author   : 蓦然
# !/usr/bin/env python
# @File     : get_token.py
# Project   : ATS

import requests
import urllib3

urllib3.disable_warnings()
# login_phone = param_config.login_phone
# login_pwd = param_config.login_pwd
api_url = "https://ats-test.51zhaopin.cn"

headers = {}


def login():
    global headers
    payload = {
        'code': 110120,
        'suiteId': 'wwbddcd1884a9dc2c5',
        'state': 'wwbddcd1884a9dc2c5'
    }
    r = requests.get(api_url + '/pic/api/login/wework/third/code', params=payload, verify=False)
    try:
        assert r.json()['code'] == 10000
        assert r.json()['data']['expire'] != ""
        assert r.headers['Authorization'] != ""
        print(r.headers['Authorization'])
    except Exception:
        raise Exception(r.json())

    # token = r.headers['Authorization']
    token = 'Bearer eyJhbGciOiJIUzI1NiJ9' \
            '.eyJzdWIiOiI0OTQ5NjI1MTExNjQyNTIxNiIsImlhdCI6MTYzMzc0Mzg5NCwiZXhwIjoxNjMzNzg3MDk0fQ.zaVF4YWP0dya-O_IWU' \
            '-SaLJU8EHkwB5YurAk74L0DmY '
    # headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    return headers


login()
