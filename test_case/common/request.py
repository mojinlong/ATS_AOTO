# __author:"zonglr"
# date:2020/6/10
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import requests, json

import common_ats.get_token as get_token, os
import test_case.common.logger as logger
from test_config import param_config, yamlconfig

headers = get_token.headers
api_url = param_config.api_url

upload_file_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'test_data/upload_file')
# print(upload_file_dir)

log = logger.Log()
request_data = yamlconfig.timeid(file_yaml='request_data.yaml')


def Resp(path, method, body=None, file_name=None):
    if method == 'get_params':
        return get_params(path=path, params=body)
    elif method == 'get_body':
        return get_body(path=path, body=body)
    elif method == 'get':
        return get(path=path)
    elif method == 'post_body':
        return post_body(path=path, body=body)
    elif method == 'post_params':
        return post_params(path=path, params=body)
    elif method == 'post_file':
        return post_file(path=path, file_name=file_name)
    elif method == 'post':
        return post(path=path)
    elif method == 'delete_body':
        return delete_body(path=path, body=body)
    elif method == 'delete_params':
        return delete_params(path=path, params=body)
    elif method == 'delete':
        return delete(path=path)
    elif method == 'put_body':
        return put_body(path=path, body=body)
    elif method == 'put':
        return put(path=path)
    else:
        Exception('不支持该请求类型，请查看你的得请求方式是否正确！！！')


def get_params(path, params, headers=headers):
    r = requests.get(api_url + path, headers=headers, params=params, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (path, json.dumps(params, ensure_ascii=False),
                                                                                json.dumps(response, ensure_ascii=False)))
    yamlconfig.body_data.setdefault(path, params)

    return response


def get_body(path, body, headers=headers):
    r = requests.get(api_url + path, headers=headers, json=body, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (path, json.dumps(body, ensure_ascii=False)
                                                                                ,json.dumps(response, ensure_ascii=False)))
    yamlconfig.body_data.setdefault(path, body)

    return response


def get(path):
    r = requests.get(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error(
            '----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning(
            '----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 10000:
        log.info('----------请求成功---------- \n 请求地址：%s \n 响应内容：%s ' % (path, json.dumps(response, ensure_ascii=False)))
    return response


def get_notResp(path):
    r = requests.get(api_url + path, headers=headers, verify=False)
    assert (r.status_code == 200)
    return r


def post_body(path, body):
    r = requests.post(api_url + path, headers=headers, json=body, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 50000:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 40003:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 10000:
        log.info('----------post请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    return response

# def post_body(path, body):
#     r = requests.post(api_url + path, headers=headers, json=body, verify=False)
#     response = r.json()
#     assert (r.status_code == 200)
#     if response['code'] == 2:
#         log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
#             path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
#     elif response['code'] == 1:
#         log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
#             path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
#     elif response['code'] == 0:
#         log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
#             path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
#     # if path not in request_data._get_yaml_element_info().keys():
#     #     request_data._set_yaml_time({path:body},'a')
#     # yamlconfig.body_data.setdefault(path, body)
#     return response


def post_params(path, params):
    r = requests.post(api_url + path, headers=headers, params=params, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    # if path not in request_data._get_yaml_element_info().keys():
    #     request_data._set_yaml_time({path:body},'a')
    yamlconfig.body_data.setdefault(path, params)
    return response


# def post_params(path, params):
#     r = requests.post(api_url + path, headers=headers, params=params, verify=False)
#     response = r.json()
#     assert (r.status_code == 200)
#     if response['code'] == 2:
#         log.error(
#             '----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
#     elif response['code'] == 1:
#         log.warning(
#             '----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
#     elif response['code'] == 0:
#         log.info('----------请求成功---------- \n 请求地址：%s ' % (path))
#     return response


def post_body_01(path, body):
    # r = requests.post(api_url + path, headers=headers, data=json.dumps(body), verify=False)
    r = requests.post(api_url + path, headers=headers, json=body, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    yamlconfig.body_data.setdefault(path, body)
    return response


def post_file(path, file_name):
    Content_Type = headers.pop('Content-Type')
    files = {'file': open(os.path.join(upload_file_dir, file_name),
                          'rb')}
    r = requests.post(api_url + path, headers=headers, files=files, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, files, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, files, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, files, json.dumps(response, ensure_ascii=False)))
    # if path not in request_data._get_yaml_element_info().keys():
    #     request_data._set_yaml_time({path:body},'a')
    yamlconfig.body_data.setdefault(path, files)
    headers['Content-Type'] = Content_Type
    return response


def post(path):
    r = requests.post(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error(
            '----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning(
            '----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info(
            '----------请求成功---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    return response


def delete_body(path, body):
    r = requests.delete(api_url + path, headers=headers, data=json.dumps(body), verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
        yamlconfig.body_data.setdefault(path, body)

    return response


def delete_params(path, params):
    r = requests.delete(api_url + path, headers=headers, params=params, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(params, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    return response


def delete(path):
    r = requests.delete(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error(
            '----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning(
            '----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info(
            '----------请求成功---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    yamlconfig.body_data.setdefault(path)
    return response


def put_body(path, body):
    r = requests.put(api_url + path, headers=headers, data=json.dumps(body), verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error('----------系统错误---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning('----------接口报错---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info('----------请求成功---------- \n 请求地址：%s \n 传入参数：%s \n 响应内容：%s' % (
            path, json.dumps(body, ensure_ascii=False), json.dumps(response, ensure_ascii=False)))

    yamlconfig.body_data.setdefault(path, body)

    return response


def put(path):
    r = requests.put(api_url + path, headers=headers, verify=False)
    response = r.json()
    assert (r.status_code == 200)
    if response['code'] == 2:
        log.error(
            '----------系统错误---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 1:
        log.warning(
            '----------接口报错---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    elif response['code'] == 0:
        log.info(
            '----------请求成功---------- \n 请求地址：%s \n 响应内容：%s' % (path, json.dumps(response, ensure_ascii=False)))
    return response


def body_replace(path, data=None, **kwargs):
    body = yamlconfig.timeid()
    if not kwargs:
        kwargs = None

    if not data or type(body._get_body(path)) is not dict:
        return body._get_body(path)
    # return body._body_replace(body._get_body(path), data)
    return body._body_replace1(body._get_body(path), data, body._keyNumber(body._get_body(path)), kwargs)
