#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/5/11 13:07
# @File     : test_baseData.py
# @Project  : integration-tests-insight
import allure
import pytest, time

from test_case.common.do_excel import DoExcel
from test_config.yamlconfig import body_data
from common import request

case_data = DoExcel(csv_dir='test_case.csv').get_cases_do_csv()


@allure.feature('创建物资')
@pytest.mark.usefixtures('b_data')
class Test_CreateGoods:
    time_now = int(time.time() * 1000)

    @pytest.mark.parametrize('title,data', [
        ['商品名称为空', {'name': None, 'msg': '请填写商品名称'}],
        ['商品名称超长限制', {'name': str('1').zfill(150), 'msg': '名称长度超出限制'}],
        ['生产商为空', {'manufacturerId': None, 'msg': '请选择生产商'}],
        ['不存在的生产商', {'manufacturerId': 999999, 'msg': '生产商没有有效的营业执照'}],
        ['商品规格为空', {'specification': None, 'msg': '请填写商品规格'}],
        ['商品价格为空', {'procurementPrice': None, 'msg': '请填写商品价格'}],
        ['商品每月限量或限制类型未设置', {'limitPerMonth': 0, 'msg': '商品每月限量或限制类型未设置'}],
        ['商品单位为空', {'minGoodsUnitId': None, 'msg': '请填写商品单位'}],
        ['商品purchaseGoodsUnitId为空', {'purchaseGoodsUnitId': None, 'msg': '请填写商品单位'}],
        ['商品minGoodsNum为空', {'minGoodsNum': None, 'msg': '请填写商品单位'}],
        ['商品属性为空', {'isHighValue': None, 'msg': '商品属性不能为空'}],
        ['是否植入物为空', {'isImplantation': None, 'msg': '是否植入物不能为空'}],
        ['是否条码管控为空', {'isBarcodeControlled': None, 'msg': '是否条码管控不能为空'}],
        ['注册证生效日期为空', {'registrationBeginDate': None, 'msg': '请填写注册证生效日期'}],
        ['商品注册证有效时间大于生产商营业执照', {'registrationBeginDate': time_now - 100000000000, 'msg': '商品注册证有效时间需在生产商营业执照有效期内'}],
        ['注册证失效日期小于生效日期', {'registrationBeginDate': time_now + 100000, 'msg': '注册证生效日期要小于失效日期'}],
        ['注册证有效时间在生产商营业执照有效期外',
         {'registrationBeginDate': time_now - 10000000000, 'registrationEndDate': time_now - 10000000000,
          'msg': '商品注册证有效时间需在生产商营业执照有效期内'}],
        ['注册证为空', {'registrationImg': None, 'msg': '请上传注册证'}],
        ['注册证号为空', {'registrationNum': None, 'msg': '请填写注册证号'}]
    ])
    @allure.story('创建商品')
    @allure.title("{title}")
    def test_creategoods(self, title, data: dict, addGoods):
        url = '/api/admin/goodsTypes/1.0/add'
        #

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)
        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['重复批量启用商品', {'msg': '已启用，不能再次操作'}],
        ['商品id为空', {'goodsIds': None, 'msg': '商品id不能为空'}],
        ['商品id不存在', {'goodsIds': [9999999], 'msg': '商品[9,999,999]不存在'}],
        ['未绑定供应商的商品', {'goodsIds': [21, 22], 'msg': '启用失败,请检查生产商和供应商授权以及供应商和一级供应商授权是否已启用'}],
        ['批量禁用商品', {'enabled': False, 'msg': '操作成功'}],
        ['重复批量禁用商品', {'enabled': False, 'msg': '已禁用，不能再次操作'}],
    ])
    @allure.story('批量启用商品')
    @allure.title('{title}')
    def test_batchUpdateStatus(self, title, data: dict, batchUpdateStatus):
        url = '/api/admin/goodsTypes/1.0/batchUpdateStatus'
        #
        # 批量启用商品

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)
        if title == '重复批量启用商品' or title == '重复批量禁用商品' or title == '未绑定供应商的商品':
            assert data['msg'] in response['msg']
        else:
            assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['重复启用商品', {'msg': '已启用，不能再次操作'}],
        ['商品id为空', {'goodsId': None, 'msg': '商品id不能为空'}],
        ['不存在的商品id', {'goodsId': 9999999, 'msg': '商品[9,999,999]不存在'}],
        ['未绑定的供应商的商品', {'goodsId': 21, 'msg': '启用失败,请检查生产商和供应商授权以及供应商和一级供应商授权是否已启用'}],
        ['是否启用为空', {'isEnabled': None, 'msg': '请选择操作类型'}],
        ['禁用商品', {'isEnabled': False, 'msg': '操作成功'}],
        ['重复禁用商品', {'isEnabled': False, 'msg': '已禁用，不能再次操作'}],
    ])
    @allure.story('启用商品')
    @allure.title('{title}')
    def test_updateEnabled(self, title, data: dict, useGoods):
        url = '/api/admin/goodsTypes/1.0/updateEnabled'
        #
        # 启用物资
        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)
        if title == '重复启用商品' or title == '重复禁用商品' or title == '未绑定的供应商的商品':
            assert data['msg'] in response['msg']
        else:
            assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['商品id为空', {'goodsId': None, 'msg': '商品ID不能为空'}],
        ['单个DI码绑定多个商品', {'goodsId': 1, 'msg': '码已绑定物资'}],
        ['DI码为空', {'diCode': None, 'msg': '操作成功'}],
    ])
    @allure.story('商品绑定DI码')
    @allure.title('{title}')
    def test_bindDI(self, title, data: dict, bindDI):
        url = '/api/admin/goodsTypes/1.0/bindDI'
        #
        # 商品绑定DI码

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)
        if title == '单个DI码绑定多个商品':
            assert data['msg'] in response['msg']
        else:
            assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['商品id为空', {'id': None, 'msg': '该生产商商品已存在'}],
        ['商品名称为空', {'name': None, 'msg': '请填写商品名称'}],
        ['商品名称超长限制', {'name': str('1').zfill(101), 'msg': '名称长度超出限制,长度最多为100个字符'}],
        ['生产商为空', {'manufacturerId': None, 'msg': '请选择生产商'}],
        ['不存在的生产商', {'manufacturerId': 999999, 'msg': '生产商没有有效的营业执照'}],
        ['商品规格为空', {'specification': None, 'msg': '请填写商品规格'}],
        ['商品价格为空', {'procurementPrice': None, 'msg': '请填写商品单价'}],
        ['商品每月限量或限制类型未设置', {'limitPerMonth': 0, 'msg': '商品每月限量或限制类型未设置'}],
        ['商品单位为空', {'minGoodsUnitId': None, 'msg': '请填写商品单位'}],
        ['商品purchaseGoodsUnitId为空', {'purchaseGoodsUnitId': None, 'msg': '请填写商品单位'}],
        ['商品minGoodsNum为空', {'minGoodsNum': None, 'msg': '请填写商品单位'}],
        ['商品属性为空', {'isHighValue': None, 'msg': '商品属性不能为空'}],
        ['是否植入物为空', {'isImplantation': None, 'msg': '是否植入物不能为空'}],
        ['是否条码管控为空', {'isBarcodeControlled': None, 'msg': '是否条码管控不能为空'}],
    ])
    @allure.story('编辑商品')
    @allure.title('{title}')
    def test_editGoods(self, title, data: dict, editGoods):
        url = '/api/admin/goodsTypes/1.0/edit'
        #
        # 编辑商品

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,url,data', [
        ['根据id获取商品详情', '/api/admin/goodsTypes/1.0/{}', {'msg': '操作成功'}],
        ['分页获取商品列表', '/api/admin/goodsTypes/1.0/pageList', {'msg': '操作成功'}],
        ['分页获取商品列表（去处价格）', '/api/admin/goodsTypes/1.0/pageListWithoutPrice', {'msg': '操作成功'}],
        ['根据部门获取商品列表，去除已生成定数包的', '/api/admin/goodsTypes/1.0/getGoodsByDepartment', {'msg': '操作成功'}],
        ['获取组合商品', '/api/admin/goodsTypes/1.0/getSurgicalGoods', {'msg': '操作成功'}],
        ['获取供应商关联的商品信息', '/api/admin/goodsTypes/1.0/supplierGoods', {'msg': '操作成功'}],
        ['导出商品', '/api/admin/goodsTypes/1.0/export', {'msg': '操作成功'}],
    ])
    def test_export(self, title, url, data, allGet_goodsType):
        # goodstype 所有get接口
        allure.dynamic.title(title)
        allure.dynamic.story(title)

        if title == '根据id获取商品详情':
            url = url.format(allGet_goodsType)
            body = None
        else:
            body = request.body_replace(url)

        response = request.get_params(url, params=body)

        assert response['msg'] == '操作成功'

    @pytest.mark.parametrize('title,data', [
        ['商品id为空', {'goodsId': None, 'msg': '商品id不能为空'}],
        ['供应商id为空', {'supplierId': None, 'msg': '操作成功'}],
        ['商品和供应商未绑定设置', {'goodsId': 999999, 'msg': '供应商和商品没有关联关系或关联关系已被删除'}]
    ])
    @allure.story('设置默认的供应商')
    @allure.title('{title}')
    def test_setDefaultSupplier(self, title, data: dict, setDefaultSupplier):
        url = '/api/admin/goodsTypes/1.0/setDefaultSupplier'
        #
        # 设置默认的供应商

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['商品id为空', {'goodsId': None, 'msg': '请选择商品'}],
        ['定数包名字为空', {'name': None, 'msg': '请填写套包名称'}],
        ['定数包数量为空', {'quantity': None, 'msg': '请填写套包中的商品数量'}],
        ['定数包数量为0', {'quantity': 0, 'msg': '商品数量最小为1'}]
    ])
    @allure.story('创建定数包')
    @allure.title('{title}')
    def test_createBag(self, title, data: dict, createBag):
        url = '/api/admin/packageBulks/1.0/add'
        #
        # 创建定数包

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['科室id为空', {'departmentId': None, 'msg': '请选择部门'}],
        ['科室id不存在', {'departmentId': 99999999, 'msg': '科室不存在'}],
        ['定数包ID为空', {'packageBulkId': None, 'msg': '请选择定数包'}],
        ['定数包ID不存在', {'packageBulkId': 999999, 'msg': '定数包不存在'}],
        ['仓库库存下限为空', {'lowerLimit': None, 'msg': '请设置仓库的库存下限'}],
        ['仓库库存下限为负数', {'lowerLimit': -1, 'msg': '库存下限不能小于0'}],
        ['仓库库存上限为空', {'upperLimit': None, 'msg': '请设置仓库的库存上限'}],
        ['库存上限小于下限', {'lowerLimit': 5, 'upperLimit': 1, 'msg': '库存上限必须大于下限'}],
        ['仓库id为空', {'warehouseId': None, 'msg': '请选择仓库'}],
        ['仓库和部门不匹配', {'warehouseId': 1, 'msg': '仓库和部门不匹配'}],
        ['仓库id不存在', {'warehouseId': 9999999, 'msg': '仓库不存在'}],
    ])
    @allure.story('定数包绑定仓库--科室')
    @allure.title('{title}')
    def test_bindWarehouse(self, title, data: dict, bindBag):
        url = '/api/admin/packageBulks/1.0/bindWarehouse'
        #
        # 定数包绑定仓库--科室

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['定数包名称为空', {'name': None, 'msg': '请填写套包名称'}],
        ['定数包ID为空', {'id': None, 'msg': '定数包不存在'}],
        ['定数包名字已存在', {'id': 1, 'msg': '定数包名称已存在,请重新输入'}]
    ])
    @allure.story('修改定数包')
    @allure.title('{title}')
    def test_editBag(self, title, data: dict, editBag):
        url = '/api/admin/packageBulks/1.0/edit'
        #
        # 修改定数包

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['定数包名称为空', {'msg': '定数包中的商品没有被启用，不能启用该定数包'}],
        ['定数包名称为空', {'id': None, 'msg': '定数包不存在'}]
    ])
    @allure.story('启用定数包')
    @allure.title('{title}')
    def test_useBag_01(self, title, data: dict, useBag_01):
        url = '/api/admin/packageBulks/1.0/enable'
        #
        # 启用定数包

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['定数包id为空', {'packageBulkId': None, 'msg': '请选择定数包'}],
        ['定数包id不存在', {'packageBulkId': 999999, 'msg': '定数包不存在'}],
        ['定数包名称为空', {'departmentId': None, 'msg': '请选择部门'}]
    ])
    @allure.story('定数包解绑科室--仓库')
    @allure.title('{title}')
    def test_unbindBag(self, title, data: dict, unbindBag):
        url = '/api/admin/packageBulks/1.0/unbindWarehouse'
        #
        # 定数包解绑科室--仓库

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['手术套包名称重复', {'msg': '手术套包名称已存在'}],
        ['套包名为空', {'name': None, 'msg': '套包名不能为空'}],
        ['手术套包使用不存在的商品', {'name': 'qqqqqqqq', 'goodsId': None, 'msg': '已被删除或禁用'}]
    ])
    @allure.story('创建手术套包')
    @allure.title('{title}')
    def test_createPkg(self, title, data: dict, createPkg):
        url = '/api/admin/packageSurgical/1.0'
        # 创建手术套包
        #

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        if title == '手术套包使用不存在的商品':
            assert data['msg'] in response['msg']
        else:
            assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['手术套包名称为空', {'name': None, 'msg': '套包名不能为空'}],
        ['手术套包名长度超出限制', {'name': str('1').zfill(101), 'msg': '套包名长度超出限制'}]
    ])
    @allure.story('修改手术套包')
    @allure.title('{title}')
    def test_editPkg(self, title, data: dict, editPkg):
        url = '/api/admin/packageSurgical/1.0/{}'.format(editPkg)
        # 修改手术套包
        #

        body = request.body_replace(url, data)

        response = request.put_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['手术套包id为空', {'packageSurgicalId': None, 'msg': '请选择套包'}],
        ['不存在的手术套包id', {'packageSurgicalId': 99999, 'msg': '手术套包不存在'}],
        ['科室id为空', {'departmentId': None, 'msg': '请选择部门'}],
        ['不存在的科室id', {'departmentId': 99999, 'msg': '科室不存在'}],
        ['库存上限小于下限', {'lowerLimit': 5, 'upperLimit': 1, 'msg': '库存上限必须大于下限'}],
        ['仓库id不存在', {'warehouseId': 9999999, 'msg': '该仓库不存在或已被删除'}],
    ])
    @allure.story('手术套包绑定科室---仓库')
    @allure.title('{title}')
    def test_binPkg(self, title, data: dict, bindPkg):
        url = '/api/admin/packageSurgical/1.0/bindDepartment'
        # 手术套包绑定科室---仓库
        #

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @pytest.mark.parametrize('title,data', [
        ['手术套包id为空', {'packageSurgicalId': None, 'msg': '请选择手术套包'}],
        ['定数包id不存在', {'packageSurgicalId': 999999, 'msg': '手术套包不存在'}],
        ['定数包名称为空', {'departmentId': None, 'msg': '请选择部门'}]
    ])
    @allure.story('手术套包解绑科室--仓库')
    @allure.title('{title}')
    def test_unbindPkg(self, title, data: dict, unbindPkg):
        url = '/api/admin/packageSurgical/1.0/unbindDepartment'
        #
        # 手术套包解绑科室--仓库

        body = request.body_replace(url, data)

        response = request.post_body(url, body=body)

        assert response['msg'] == data['msg']

    @allure.story('启用手术套包')
    @allure.title('手术套包中商品未启用，启用套包')
    def test_usePkg(self, usePkg):
        url = '/api/admin/packageSurgical/1.0/enable/{}'.format(usePkg)
        # 启用手术套包

        response = request.put(url)

        assert '套包中的商品' in response['msg']

    @allure.story('删除手术套包')
    @allure.title('重复删除')
    def test_delPkg(self, delPkg):
        url = '/api/admin/packageSurgical/1.0/{}'.format(delPkg)
        # 重复删除

        response = request.delete(url)

        assert response['msg'] == '记录不存在'


class Test_CreateGoods_01:
    # 手术套包和定数包查询接口补充

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['get_Bag_Pkg'])
    def test_CreateGoods_01(self, feature, story, method, url, title, data, get_Bag_Pkg):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if story == '根据id获取普通套包详情':
            url = url.format(id=get_Bag_Pkg[0])
        elif story == '根据id获取手术套包详情':
            url = url.format(id=get_Bag_Pkg[1])

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


@pytest.mark.usefixtures('b_data')
class Test_CreateDepartments:
    # 创建科室

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['CreateDepartments'])
    def test_CreateDepartments(self, feature, story, method, url, title, data, batchBindDepartmentGoods,
                               addDepartments, editDepartments, removeDepartmentGoods, delDepartments, departments_01):
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if story == '更新科室信息':
            url = url.format(departmentsId=editDepartments)
            if title == '上级科室选择当前科室':
                data = data.replace('departmentsId', str(editDepartments))
        elif story == '移除科室商品':
            url = url.format(departmentsId=removeDepartmentGoods)
        elif story == '删除科室':
            url = url.format(departmentsId=delDepartments)
        elif story == '根据id获取组织详情' or story == '根据id获取父级组织':
            url = url.format(id=addDepartments[1])
        # 批量绑定商品和科室
        body = request.body_replace(url, data)
        if title == '院区字段为空' or title == '行政地区不存在':
            body['name'] += '--测试'
        elif title == '导出科室商品失败':
            body['goodsId'] = eval(data)['goodsId']

        response = request.Resp(path=url, method=method, body=body)

        if title == '院区字段为空' and story == '新增科室':
            assert '院区[null]不存在' in response['msg']
        elif title == '同一商品、仓库，重复设置仓库商品上下限':
            assert eval(data)['msg'] in response['msg']
        else:
            assert response['msg'] == eval(data)['msg']


class Test_DistributionUnit_orderUnit_std95GoodsCategory:
    # 配送单位 和 订货单位

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['DistributionUnit_orderUnit'])
    def test_DistributionUnit_orderUnit(self, feature, story, method, url, title, data, distributionUnit,
                                        orderUnit):
        # 配送单位 和 订货单位
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if story == '删除配送单位' and title == '配送单位id为空':
            url = url.format(id=distributionUnit[1])

        elif story == '删除配送单位' and title == '重复删除配送单位':
            url = url.format(id=distributionUnit[0])

        elif story == '删除订货单位' and title == '订货单位id为空':
            url = url.format(id=orderUnit)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']

    @pytest.mark.parametrize('feature,story,method,url, title, data',
                             case_data['std95GoodsCategory_goodsQuantityUnits'])
    def test_std95GoodsCategory(self, feature, story, method, url, title, data, std95GoodsCategory, goodsQuantityUnits):
        # 95分类 和 获取商品计量单位信息列表
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_custodian:
    # 一级供应商

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['custodian_01'])
    def test_DistributionUnit_orderUnit(self, feature, story, method, url, title, data, custodian):
        # 一级供应商
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title == '已经启用的状态下，编辑一级供应商' or title == '根据id获取一级供应商详情':
            url = url.format(id=custodian)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_consume:
    # 扫码消耗

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['consume_01'])
    def test_consume_01(self, feature, story, method, url, title, data, consume_01):
        # 一级供应商
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        if title == '批量消耗':
            assert response['msg'] == eval(data)['msg']
            assert response['data'][0]['errorMessage'] == eval(data)['errorMessage']
        elif story == '扫码消耗' or story == '扫码反消耗':
            assert response['msg'] == eval(data)['msg'].format(barcode=eval(data)['barcode'])
        else:
            assert response['msg'] == eval(data)['msg']

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['consume_02'])
    def test_consume_02(self, feature, story, method, url, title, data, consume_02):
        # 一级供应商
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']
        assert response['data'][0]['errorMessage'] == eval(data)['errorMessage']


class Test_manufacturer:
    # 生产商

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['manufacturer'])
    def test_manufacturer(self, feature, story, method, url, title, data, createManufacturer, manufacturer_01):
        # 生产商
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if story == '更新厂商信息' or title == '根据id获取厂商详情':
            url = url.format(id=createManufacturer)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['manufacturerAuthorizations'])
    def test_manufacturerAuthorizations(self, feature, story, method, url, title, data, manufacturerAuthorizations,
                                        manufacturerAuthorizations_01):
        # 授权书
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title == '根据id获取授权书详情':
            url = url.format(id=manufacturerAuthorizations)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_diagnosisProject:
    # 诊疗项目管理

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['diagnosisProject'])
    def test_diagnosisProject(self, feature, story, method, url, title, data, diagnosisProject):
        # 诊疗项目管理
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title in ['根据id查询诊疗项目', '启用诊疗项目', '禁用诊疗项目']:
            url = url.format(id=diagnosisProject)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        if title == '同名重复新增诊疗项目':
            assert eval(data)['msg'] in response['msg']
        else:
            assert response['msg'] == eval(data)['msg']

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['diagnosis_project_department'])
    def test_diagnosis_project_department(self, feature, story, method, url, title, data, diagnosis_project_department):
        # 诊疗项目科室绑定
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        body = request.body_replace(url, data)

        response = request.Resp(path=url, method=method, body=body)

        assert response['msg'] == eval(data)['msg']


class Test_warehouses:
    # 仓库

    @pytest.mark.parametrize('feature,story,method,url, title, data', case_data['warehouses'])
    def test_warehouses(self, feature, story, method, url, title, data, warehouseData_01):
        # 仓库
        allure.dynamic.title(title)
        allure.dynamic.feature(feature)
        allure.dynamic.story(story)

        if title in ['更新仓库信息', '根据id获取仓库详情']:
            url = url.format(id=warehouseData_01[0])
        elif title == '根据库房id获取详情':
            url = url.format(id=warehouseData_01[0])
        elif story == '删除库房信息':
            url = url.format(id=warehouseData_01[1])
        elif title in ['更新货架信息', '根据id获取货柜详情']:
            url = url.format(id=warehouseData_01[2])
        elif story == '根据id删除货柜信息':
            url = url.format(id=warehouseData_01[2])

        body = request.body_replace(url, data)

        if story == '新增库区':
            body['code'] += 1

        response = request.Resp(path=url, method=method, body=body)

        if story == '新增货架':
            assert eval(data)['msg'] in response['msg']
        else:
            assert response['msg'] == eval(data)['msg']
