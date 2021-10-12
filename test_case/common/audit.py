# -*- coding: utf-8 -*-
# @Time : 2021/6/02 2:55 下午
# @Author : mjl
# @File :audit
import jsonpath

import request, random


# 审计
def getAuditHistory(key=None, target=None):
    """
    分页查询审计记录
    """
    params = {
        'key': key,
        'target': target
    }
    response = request.get_params('/api/admin/audit/1.0/getHistory', params=params)
    try:
        assert response['msg'] == '操作成功'
    except:
        raise Exception(response)
    return response


def getAuditWithPage(end, target, freeText, hospitalId, key, loginPhone, start, userId, pageNum=None, pageSize=None,
                     userName=None, targetList=None, type=None):
    """
    查询操作历史
    """
    params = {
        'end': end,
        'target': target,
        'freeText': freeText,
        'hospitalId': hospitalId,
        'key': key,
        'loginPhone': loginPhone,
        'pageNum': pageNum,
        'pageSize': pageSize,
        'start': start,
        'targetList': targetList,
        'type': type,
        'typeList': targetList,
        'userId': userId,
        'userName': userName
    }
    response = request.get_params('/api/admin/audit/1.0/getWithPage', params=params)
    try:
        assert response['msg'] == '操作成功'
    except:
        raise Exception(response)
    return response


# getAuditHistory(1, 'md_warehouse')
# getAuditWithPage(end=None, target='md_goods', freeText=None, hospitalId=104,
# key=1, loginPhone=None, start=None,targetList=None, type='modify', userId=1, pageNum=0, pageSize=50)
if __name__ == '__main__':
    # getAuditHistory(1, 'md_warehouse')
    getAuditWithPage(end=None, target='md_goods', freeText=None, hospitalId=104,
key=1, loginPhone=None, start=None,targetList=None, type='modify', userId=1, pageNum=0, pageSize=50)