# coding=gbk
import os, collections
import yaml, time, pprint
from collections import Counter  # ����Counter


class timeid():
    def __init__(self, file_yaml='config.yaml'):
        current_path = os.path.dirname(__file__)
        self.yaml_path = os.path.join(current_path, file_yaml)
        time_now = time.time()
        self.my_time = int(time_now * 1000)
        timeArray = time.localtime(time_now)
        self.otherStyleTime = time.strftime("%m%d%H%M%S", timeArray)
        # timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")

    # ��ȡ
    def _get_yaml_element_info(self):
        with open(self.yaml_path, "r", encoding="utf-8") as file:
            file_data = file.read()
            # ָ��Loader
            data = yaml.load(file_data, Loader=yaml.FullLoader)
            return data

    # д��
    def _set_yaml_time(self, data, type='w'):
        with open(self.yaml_path, type, encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)

    # ��ȡ֮��id
    def id(self):
        time_data = self._get_yaml_element_info()
        time_data['goods']['id'] += 1
        if self.otherStyleTime == time_data['time']:
            time_data['id'] += 1
            self._set_yaml_time(time_data)
        else:
            time_data['id'] = 0
            time_data['time'] = self.otherStyleTime
            self._set_yaml_time(time_data)

        department_name = []
        code = []
        for i in time_data['department_list']:
            department_name.append(time_data['testname'] + time_data['time'] + str(i))
            code.append(time_data['time'] + str(i))
        return {
            # ���Ŀ�Ψһid
            'core_code': time_data['time'],
            # һ����������
            'departmentname': time_data['testname'] + time_data['time'],
            # ������������
            'department_name': department_name,
            'code': code,
            'goodsname': {
                'low': time_data['goods']['name']['low'] + time_data['time'],
                'low1': time_data['goods']['name']['low1'] + time_data['time'],
                'high': time_data['goods']['name']['high'] + time_data['time'],
                'lowbag': time_data['goods']['name']['lowbag'] + time_data['time'],
                'pkg': time_data['goods']['name']['pkg'] + time_data['time'],
            },
            'rolename': {
              'custodian': time_data['role']['custodian'] + time_data['time'],
              'hospital': time_data['role']['hospital'] + time_data['time'],
              'operator': time_data['role']['operator'] + time_data['time'],
              'supplier': time_data['role']['supplier'] + time_data['time'],
            }
        }

    def body_data(self):
        return collections.defaultdict()

    def _get_body(self, path):
        if body_data.get(path) is not None:
            body = eval(str(body_data[path].copy()))
        else:
            body = body_data.get(path)
        return body

    def _body_replace(self, body, data):
        if type(data) is not dict:
            data = eval(data)
        if body is not None:
            for i in body.keys():
                if type(body[i]) is str:
                    pass
                elif type(body[i]) is dict:
                    self._body_replace(body[i], data)
                elif type(body[i]) is list:
                    for j in body[i]:
                        if type(j) is dict:
                            self._body_replace(j, data)

                if i in data.keys():
                    body[i] = data[i]
        return body

    def _body_replace1(self, body, data, b=None, num=None):
        if type(data) is not dict:
            data = eval(data)
        if body:
            for i in body.keys():
                if type(body[i]) is str:
                    pass
                elif type(body[i]) is dict:
                    self._body_replace1(body[i], data, b, num)
                elif type(body[i]) is list:
                    for j in body[i]:
                        if type(j) is dict:
                            self._body_replace1(j, data, b, num)

                if i in data.keys():
                    if not num or i not in num.keys():
                        body[i] = data[i]
                    else:
                        if num[i] == 1 and b[i] != 1:
                            body[i] = data[i]
                            num[i] -= 1
                        else:
                            num[i] -= 1
        return body

    def _keyNumber(self, body, a=list()):
        if body:
            for i in body.keys():
                a.append(i)
                if type(body[i]) is str:
                    pass
                elif type(body[i]) is dict:
                    self._keyNumber(body[i], a)
                elif type(body[i]) is list:
                    for j in body[i]:
                        if type(j) is dict:
                            self._keyNumber(j, a)

        b = dict(Counter(a))
        return {key: value for key, value in b.items() if value > 1}


body_data = timeid().body_data()

# elements=ElementdataYamlUtils().get_yaml_element_info(yaml_path)

if __name__ == '__main__':
    body = {
        "code": 0,
        "data": {
            "adhocOrderToolsKitBean": [
                {
                    "code": "",
                    "detailBeanList": [
                        {
                            "categoryCode": "",
                            "imageSource": [],
                            "warehouseStock": 0
                        }
                    ],
                    "id": 0,
                    "manufacturerName": "",
                    "warehouseStock": 0
                }
            ],
            "adhocOrderUiBean": {
                "addressId": 0,
                "airlineCompany": "",
                "districtCode": [],
                "encryptReceivingIdCard": "",
                "postcode": "",
                "powerOfAttorney": "",
                "procedureSite": [],
                "procedureSiteName": [],
                "procedureTime": 0
            },
            "goodsDetailList": [
                {
                    "categoryCode": "",
                    "di": "",
                    "goodsId": 0,
                    "goodsName": "",
                    "imageSource": []
                }
            ],
            "strategyList": [
                {
                    "orderList": [
                        {
                            "adhocOrderToolsKitBean": [
                                {}
                            ],
                            "goodsDetailList": [
                                {
                                    "categoryCode": "",
                                    "di": [
                                        {
                                            "goodsId": 0
                                        }
                                    ],
                                    "goodsId": 0,
                                }
                            ],
                            "warehouseId": 0,
                        }
                    ],
                    "strategyName": ""
                }
            ]
        },
        "exMsg": "",
    }
    # print(b)
    # a = timeid()
    # print(timeid()._keyNumber(body))
    # pprint.pprint(
    #     timeid()._body_replace1(body, {'goodsId': 888888888, 'goodsName': 9999999999}, timeid()._keyNumber(body),
    #                             {'goodsId': 2}))
    # a = None
    # if not a:
    #     print(1111)

    # data = {}
    # if data:
    #     print('11111')

    pprint.pprint(timeid().id())
