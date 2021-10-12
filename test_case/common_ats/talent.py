#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/9/10 14:44 
# @Author   : 蓦然
# @File     : talent.py
# Project   : ATS


from ATS.test_case.common import request


def lastTimeArchiveInfo():
    """
    获取当前登录人最后一次使用的归档信息
    Type: get
    """
    url = "/pic/api/talent/lastTimeArchiveInfo"
    response = request.get(url)
    # print(response)
    return response['data']


def talent_pool_create(name, parentId):
    """
    新增人才库树节点
    Type: psot
    talentPoolCreateDTO:(body)
        name:	人才库名称   必填  string
        parentId:   人才库父id   必填   integer
    """
    url = "/pic/api/talent_pool/create"

    talentPoolCreateDTO = {
        'name': name,
        'parentId': parentId
    }
    response = request.post_body(url, body=talentPoolCreateDTO)
    print(response)


def talent_pool_delete(talentPoolId):
    """
    删除人才库树节点
    Tpye: delete
    params:
        talentPoolId:   talentPoolId    必填    integer
    """
    url = "/pic/api/talent_pool/delete/{talentPoolId}".format(talentPoolId=talentPoolId)
    response = request.delete(url)
    print(response)


def talent_pool_get(talentPoolId):
    """
    通过id获取人才库详情（一个人才库）
    Tpye: get
    params:
        talentPoolId:   talentPoolId    必填    integer
    """
    url = "/pic/api/talent_pool/get/{talentPoolId}".format(talentPoolId=talentPoolId)
    response = request.get(url)
    return response['date']


def talent_pool_list(type):
    """
    人才库列表
    Tpye: get
    params:
        type: type    必填    integer
    """
    url = '/pic/api/talent_pool/list/{type}'.format(type=type)
    response = request.get(url)
    print(response)
    return response


def talent_pool_update(id, name):
    """
    修改人才库树节点
    Type: post
    params:
        id: id    必填    string
        name : name    必填       string
    """
    url = "/pic/api/talent_pool/update"
    talentPoolUpdateDTO = {
        'id': id,
        'name': name
    }
    response = request.post_body(url, body=talentPoolUpdateDTO)
    print(response)
    return response
# talent_pool_list(1)


talent_pool_update(id="49907071172349952", name="上海徐汇人才库")
