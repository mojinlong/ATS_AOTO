# __author:"zonglr"
# date:2020/5/23
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import requests, urllib3
from test_config import param_config

urllib3.disable_warnings()
login_phone = param_config.login_phone
login_pwd = param_config.login_pwd
api_url = param_config.api_url

headers = {}
hospital_name = ''
hospital_id = ''


def login():
    global headers, hospital_name, hospital_id
    payload = {
        'loginPassword': login_pwd,
        'loginPhone': login_phone
    }
    r = requests.post(api_url + '/api/admin/login/web/1.0/login', data=payload, verify=False)
    try:
        assert r.json()['code'] == 0
    except Exception:
        raise Exception(r.json())
    hospital_name = r.json()['data']['hospitals'][0]['name']
    hospital_id = r.json()['data']['hospitals'][0]['id']
    token = r.headers['X-AUTH-TOKEN']
    # headers
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-TOKEN': token
    }
    return headers, hospital_name, hospital_id


login()
