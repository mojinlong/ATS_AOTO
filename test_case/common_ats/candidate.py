#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/9/14 13:20
# @Author   : 蓦然
# @File     : candidate.py
# Project   : ATS

from test_case.common import request


def candidate_create(name):
    url = '/pic/api/candidate/create'
    body = {
        "channelId": "161362469970203",
        "channelName": "",
        "passFlag": 0,
        "positionId": "162865242215821",
        "resumeBasicInfoVO": {
            "age": "30",
            "currentAddress": "上海浦东新区",
            "currentWorkStatus": 1,
            "dutyTime": "十天",
            "education": None,
            "email": "m17600888399@163.com",
            "expectCity": "北京/北京市/东城区",
            "expectIndustry": "软件",
            "expectPosition": "软件测试",
            "expectSalary": "20000",
            "gender": 1,
            "graduatedSchool": "",
            "name": name,
            "phone": "17600888399",
            "profession": "",
            "selfEvaluation": "良好",
            "skill": "1",
            "workYears": 8
        },
        "status": 10,
        "workExperienceVOS": [{
            "beginDate": "2014-08",
            "endDate": "至今",
            "leaveReason": "个人原因",
            "position": "java开发",
            "workCompany": "软通动力",
            "workContent": "1",
            "workResult": "1"
        }],
        "educationVOS": [{
            "beginDate": "2010-09",
            "education": 6,
            "endDate": "2014-07",
            "profession": "中文",
            "school": "浙江大学"
        }],
        "projectVOS": [{
            "beginDate": "2014-08",
            "endDate": "至今",
            "projectDescription": "1",
            "projectDuty": "1",
            "projectName": "喔趣企管",
            "projectPerformance": "1",
            "projectRole": "java开发"
        }],
        "workSkillVOS": [{
            "level": "1",
            "name": "1"
        }],
        "tags": []
    }
    response = request.post_body(url, body=body)
    print(response)
    page_url = '/pic/api/candidate/page'
    page_body = {
        "actualEntryTimeEnd": None,
        "actualEntryTimeStart": None,
        "ageEnd": None,
        "ageStart": None,
        "channelId": None,
        "createTimeEnd": None,
        "createTimeStart": None,
        "createrEwId": None,
        "education": None,
        "gender": None,
        "hrEwId": None,
        "interviewTimeEnd": None,
        "interviewTimeStart": None,
        "pageNum": 1,
        "pageSize": 20,
        "planEntryTimeEnd": None,
        "planEntryTimeStart": None,
        "positionId": None,
        "tagIds": [],
        "workYearsEnd": None,
        "workYearsStart": None,
        "expectCity": None
    }
    page_response = request.post_body(page_url, page_body)
    uid = ""
    for x in page_response['data']['records']:
        if x['name'] == name:
            uid = x['id']
            break
    rl = [name, uid]
    return rl


def delete_candidate(cid):
    url = '/pic/api/candidate/delete_candidate?candidateId={}'.format(cid)
    request.get(url)


def update_candidate_status(name, uid):
    url = '/pic/api/candidate/update_candidate_status'
    body = {
        "status": 20,
        "name": name,
        "candidateId": uid,
        "passFlag": None,
        "candidateIdSet": [uid]
    }
    response = request.post_body(url, body)
    print(response)


def interview_create(uid, interTime):
    url = '/pic/api/candidate/interview/create'
    body = {
        "addressHouseNumber": "A栋2楼202",
        "attachmentUrlList": [],
        "candidateId": uid,
        "conferenceRoomName": "后裔会议室",
        "contactName": "莫金龙",
        "contactPhone": "17600888399",
        "email": "m17600888399@163.com",
        "emailCc": "",
        "emailNotifyOriginalTemplate": "<h2 style=\"text-align:center;\">面试通知</h2>\n<p>尊敬的 <span style=\"color: "
                                       "#0074ff;\">#候选人姓名#</span></p>\n<p style=\"text-indent: 2em;\">您好，感谢您对 <span "
                                       "style=\"color: #0074ff;\">#公司名称#</span> "
                                       "的信任和支持，您提供的应聘资料符合我司的面试要求，特邀您前来参与面试。为能顺利帮您安排面试，请详细了解以下信息：</p>\n<p>应聘职位：&nbsp"
                                       ";<span style=\"color: rgb(0, 116, "
                                       "255);\">#应聘职位#</span>&nbsp;</p>\n<p>面试时间：<span style=\"color: "
                                       "#0074ff;\">#面试时间#</span></p>\n<p>面试地址：<span style=\"color: "
                                       "#0074ff;\">#面试地址#</span></p>\n<p style=\"text-indent: "
                                       "2em;\">请您安排时间准时到达面试地点，如有问题请与 <span style=\"color: #0074ff;\">#联系人#</span>（ "
                                       "<span style=\"color: #0074ff;\">#联系人电话#</span> ）联系。</p>\n<p>祝您面试成功,袁帅测试</p>",
        "emailTitle": "【喔趣企业管理】面试邀请",
        "hrEwId": "MoJinLong",
        "interviewAddress": "上海市徐汇区斜土路2899号(近星游城)",
        "interviewAddressLat": 31.185694,
        "interviewAddressLng": 121.441156,
        "interviewEndTime": interTime,
        "interviewTime": interTime,
        "interviewerEwIds": ["MoJinLong"],
        "method": 0,
        "notifyCandidateMethods": [2],
        "notifyInterviewerMethods": [1],
        "positionId": "162865242215821",
        "addressShort": "光启文化广场",
        "regional": "上海市",
        "replyEmail": "",
        "corpNotifyTemplateId": "32127554227933184",
        "emailNotifyTemplate": "<h2 style=\"text-align:center;\">面试通知</h2>\n<p>尊敬的 <span style=\"color: "
                               "#0074ff;\">张三</span></p>\n<p style=\"text-indent: 2em;\">您好，感谢您对 <span style=\"color: "
                               "#0074ff;\">喔趣企业管理</span> "
                               "的信任和支持，您提供的应聘资料符合我司的面试要求，特邀您前来参与面试。为能顺利帮您安排面试，请详细了解以下信息：</p>\n<p>应聘职位：&nbsp;<span "
                               "style=\"color: rgb(0, 116, 255);\">测试</span>&nbsp;</p>\n<p>面试时间：<span style=\"color: "
                               "#0074ff;\">2021-09-14 10:45-11:00</span></p>\n<p>面试地址：<span style=\"color: "
                               "#0074ff;\">上海市徐汇区斜土路2899号(近星游城)A栋2楼202</span></p>\n<p style=\"text-indent: "
                               "2em;\">请您安排时间准时到达面试地点，如有问题请与 <span style=\"color: #0074ff;\">测试联系人张三</span>（ <span "
                               "style=\"color: #0074ff;\">166-0124-5399</span> ）联系。</p>\n<p>祝您面试成功,袁帅测试</p> "
    }
    response = request.post_body(url, body)
    print(response)


def resumParser(file_name):
    url = '/pic/api/candidate_resume/resumeParser'
    response = request.post_file(url, file_name=file_name)
    print(response)
    return response


if __name__ == '__main__':
    create = candidate_create(name='Xiaomi9')
    update_candidate_status(name=create[0], uid=create[1])
    file_name = '【测试工程师  _ 上海12-18K】高杰 12年.pdf'
    resumParser(file_name)

    # interview_create(create[1], 1631624188000)
    # delete_candidate(cid=create[1])


# 背调
def back_tone_order_choose_package():
    """
    查询套餐
    request : post
    """
    url = '/pic/api/candidate/back_tone_order/choose_package'
    response = request.post(url)
    return response


def back_tone_order_create(amount, candidateId, candidateIdCard, candidateName, candidatePhoneNo, clientContact,
                           clientPhoneNo, companyName, itemCode, itemName, perfNum, witnessNum, xpNum):
    """
    创建背调订单
    request: POST
            参数名称  			参数说明  		    是否必须    数据类型
            submitRequest		订单提交				true
            amount				套餐金额				false	   string
            candidateId			候选人id				false	   integer(int64)
            candidateIdCard		候选人身份证号		false	   string
            candidateName		候选人姓名			false	   string
            candidatePhoneNo	候选人手机号			false	   string
            clientContact		委托方联系人			false	   string
            clientPhoneNo		委托方联系电话		false	   string
            itemList			背调数据项列表		false	   array
            companyName			公司名称				false	   string
            itemCode			数据项code			false	   string
            itemName			数据项名称			false	   string
            perfNum				工作经历之表现个数	false	   integer
            witnessNum			证明人数量			false	   integer
            xpNum				工作经历之履历个数	false	   integer
            productId			套餐id				false	   string
            productName			套餐名称				false	   string
    """

    body = {
        "amount": amount,
        "candidateId": candidateId,
        "candidateIdCard": candidateIdCard,
        "candidateName": candidateName,
        "candidatePhoneNo": candidatePhoneNo,
        "clientContact": clientContact,
        "clientPhoneNo": clientPhoneNo,
        "itemList": [
            {
                "companyName": companyName,
                "itemCode": itemCode,
                "itemName": itemName,
                "perfNum": perfNum,
                "witnessNum": witnessNum,
                "xpNum": xpNum
            }
        ],
        "productId": "",
        "productName": ""
    }
    url = '/pic/api/candidate/back_tone_order/create'
    response = request.post_body(url, body=body)


def back_tone_order_cancel(orderNo):
    """
    取消订单
    request : POST
    params : orderNo
    参数名称   是否必须    数据类型
    orderNo   true      string
    """
    url = '/pic/api/candidate/back_tone_order/cancel={orderNo}'.format(orderNo=orderNo)
    response = request.post(url)


def back_tone_order_delete(Id):
    """
    删除订单
    request : post
    params : id
    参数名称    参数说明    是否必须    数据类型
    id         订单id     true       integer
    """
    url = '/pic/api/candidate/back_tone_order/delete={Id}'.format(Id=Id)
    assert Id != '' and Id is not None
    response = request.post(url)


def back_tone_order_list(candidateId):
    """
    背调订单列表
    request : post
    params : candidateId
    参数名称    参数说明    是否必须    数据类型
    candidateId          true       integer
    """
    url = '/pic/api/candidate/back_tone_order/list={candidateId}'.format(candidateId=candidateId)
    assert candidateId != '' and candidateId is not None
    response = request.post(url)
    # assert response['code'] != ""
    return response


def back_tone_order_open(ewUserId, corpId=0):
    """"
    开通背调
    request : post
    parameter
    参数名称     参数说明    是否必须    数据类型
    corpId	   企业客户id   false     integer
    ewUserId   企业微信ID   false     string
    """
    url = '/pic/api/candidate/back_tone_order/open'
    body = {
        "corpId": corpId,
        "ewUserId": ewUserId
    }
    response = request.post_body(url, body=body)
    return response
    # assert response['code'] != ""


def back_tone_order_open_flag():
    """
    是否开通背调
    request : post
    """
    url = '/pic/api/candidate/back_tone_order/open_flag'
    response = request.post(url)
    return response


def back_tone_order_view(orderNo=0):
    """
    查看报告
    params : orderNo
    参数名称    参数说明    是否必须    数据类型
    orderNo   orderNo    true      integer
    """
    url = '/pic/api/candidate/back_tone_order/view/{orderNo}'.format(orderNo=orderNo)
    response = request.post(url)
    return response


if __name__ == '__main__':
    flag = back_tone_order_open_flag
    back_tone_order_open(ewUserId=1, corpId=2)
    package = back_tone_order_choose_package()
    back_tone_order_create()
