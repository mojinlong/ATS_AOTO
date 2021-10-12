# __author:"zonglr"
# date:2020/11/27
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import dis

import pytest
import platform
import sys, os
from test_config.putProperties import Properties
from test_config import param_config
from test_case.common import request
from test_case.common import audit
from test_case.common import systemData
from test_case.common import role
# api_url = param_config.api_url
# loginPhone = param_config.login_phone
# # 文件目录
# dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '\\test_data'
# excelPath = os.path.join(dir, "RFID模板.xlsx")
# yamlPath = os.path.join(dir, "test_data.yaml")
#
#
# # 全局只执行一次，根据模板导入EPC TEST0000010000~TEST0000050000
# @pytest.fixture(scope="session")
# def upload_rfid():
#     payload = {
#         'loginPassword': '123456',
#         'loginPhone': loginPhone
#     }
#     r = requests.post(api_url + '/api/admin/login/web/1.0/login', data=payload, verify=False)
#     assert r.status_code == 200
#     token = r.headers['X-AUTH-TOKEN']
#     headers = {
#         'X-AUTH-TOKEN': token
#     }
#     f = open(excelPath, 'rb')
#     files = {
#         'file': (excelPath, f, 'application/x-zip-compressed'),
#     }
#     response = requests.post(api_url + '/api/admin/rfidStock/1.0/uploadRfidByTemplate', headers=headers, files=files,
#                              verify=False)
#     f.close()
#     return response.json()
#
#
# # 根据已使用的epc生成一个新的epc
# @pytest.fixture(scope="function")
# def generate_epc():
#     # 读取文件
#     with open(yamlPath, 'r', encoding='utf-8') as f:
#         try:
#             content = ruamel.yaml.load(f, Loader=ruamel.yaml.RoundTripLoader)
#         except ruamel.yaml.YAMLError as exc:
#             print(exc)
#     # 获取最后一个epc
#     epc = content['EPC'][-1]
#     # 通过正则获取数字
#     num = re.sub(r'\D', "", epc)
#     # 数字+1，并生成新的epc, EA+10位数字
#     new_num = int(num) + 1
#     # 补0
#     new_epc = 'TEST' + str(new_num).zfill(10)
#     return epc, new_epc
#
#
# # 将指定epc添加到已使用的epc列表中
# @pytest.fixture(scope="function")
# def add_used_epc():
#     def _add_used_epc(epc):
#         # 读取文件
#         with open(yamlPath, 'r', encoding='utf-8') as f:
#             try:
#                 content = ruamel.yaml.load(f, Loader=ruamel.yaml.RoundTripLoader)
#             except ruamel.yaml.YAMLError as exc:
#                 print(exc)
#         # 将指定epc追加到列表中
#         content['EPC'].append(epc)
#         # 追加epc
#         with open(yamlPath, 'w+', encoding='utf-8') as w_f:
#             # 覆盖原先的配置文件
#             try:
#                 ruamel.yaml.dump(content, w_f, default_flow_style=False, allow_unicode=True,
#                                  Dumper=ruamel.yaml.RoundTripDumper)
#             except ruamel.yaml.YAMLError as exc:
#                 print(exc)
#
#     return _add_used_epc
#

# spw编辑

from common import createDeparments, addbusiness, createGoods, goodsRequest, createPurchase, centralLibrary, \
    all_Deparments_putOnShelf, all_check, baseData, finance, sql, his, statistic
from test_config.yamlconfig import body_data, timeid
import collections


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


# # body数据清空
# @pytest.fixture(scope='class')
# def res_data():
#     timeid(file_yaml='request_data.yaml')._set_yaml_time({'url': 'body'}, 'w')


# import platform
# import sys, os
# from test_config.putProperties import Properties
# from test_config import param_config
# from test_case.common import request
# from test_case.common import audit
# from test_case.common import systemData
# from test_case.common import role


# 脚本运行信息
@pytest.fixture(scope='session', autouse=True)
def authorData():
    a = platform.platform()

    new = a.split('-')
    systemVersion = new[0] + new[1]
    proper = Properties(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs/environment.properties'))
    proper.put('author', 'spw')
    proper.put('systemVersion', systemVersion)
    proper.put('pythonVersion', sys.version.split(' ')[0])
    proper.put('baseUrl', param_config.api_url)
    resp = request.get('/api/admin/version/1.0/version')['data']['md-beans']
    proper.put('projectName',
               resp['git.branch'] + '--' + resp['git.build.host']
               )


# body数据清空
@pytest.fixture(scope='class', autouse=True)
def b_data():
    yield
    body_data.clear()


# 创建生产商，返回id
@pytest.fixture(scope='class')
def createManufacturer():
    global name
    name = timeid().id()
    print('流程唯一id:{}'.format(name))
    global business
    business = addbusiness.addBusiness(name['core_code'])
    # 生产商
    global manufacturer_id
    manufacturer_id = business.createManufacturer('测试生产商')
    yield manufacturer_id


# 生产商流程
@pytest.fixture(scope='class')
def manufacturer_01(createManufacturer):
    # 启用/禁用
    business.operate('manufacturer', manufacturer_id, type=2)
    # 更新厂商信息
    business.edit_manufacturer('测试生产商', manufacturer_id)
    # 根据id获取厂商详情
    business.get_manufacturer_id(manufacturer_id)
    # 获取厂商列表
    business.get_manufacturer()
    # 根据供应商id获取厂商列表
    business.listBySupplier()


# 创建商品
@pytest.fixture(scope='class')
def addGoods(createManufacturer):
    global goods
    goods = createGoods.createGoods()
    # 商品
    global goodsList
    goodsList = goods.addGoods(name['goodsname'], manufacturerId=createManufacturer)
    print('商品id', goodsList)
    yield goodsList


# 新增诊疗项目
@pytest.fixture(scope='class')
def diagnosisProject(useGoods):
    diagnosisProject = baseData.diagnosisProject()
    # 新增诊疗项目
    diagnosisProject_id = diagnosisProject.add(name['core_code'], goodsList[0])
    # 修改诊疗项目
    diagnosisProject.edit(diagnosisProject_id)
    # 启用诊疗项目
    diagnosisProject.enable(diagnosisProject_id)
    # 禁用诊疗项目
    diagnosisProject.forbid(diagnosisProject_id)
    # 列表
    diagnosisProject.pageList()
    # 导出诊疗项目
    diagnosisProject.export()

    yield diagnosisProject_id


@pytest.fixture(scope='class')
def distributionUnit(addGoods):
    goodsid = goodsList[0]
    # 配送单
    distribution = baseData.distributionUnit()
    # 新增
    distribution.add(goodsid)
    distribution.add(goodsid)
    # 查询
    distribution_idList = distribution.list(goodsid)
    # 更新
    distribution.update(distribution_idList[0], goodsid)
    # 设置配送单位
    distribution.setDefault(distribution_idList[0], goodsid)
    # 清空默认配送单位
    distribution.unsetDefault(distribution_idList[0], goodsid)
    # 删除
    distribution.delete(distribution_idList[0])
    yield distribution_idList[0], distribution_idList[1]


@pytest.fixture(scope='class')
def orderUnit(addGoods):
    goodsid = goodsList[0]
    # 配送单
    orderUnit = baseData.orderUnit()
    # 新增
    orderUnit.add(goodsid)
    orderUnit.add(goodsid)
    # 查询
    orderUnit_idList = orderUnit.list(goodsid)
    # 更新
    orderUnit.update(orderUnit_idList[0], goodsid)
    # 设置配送单位
    orderUnit.setDefault(orderUnit_idList[0], goodsid)
    # 清空默认配送单位
    orderUnit.unsetDefault(orderUnit_idList[0], goodsid)
    # 删除
    orderUnit.delete(orderUnit_idList[0])
    yield orderUnit_idList[1]


# 95分类查询
@pytest.fixture(scope='class')
def std95GoodsCategory():
    # 获取所有分类
    baseData.std95GoodsCategory_goodsQuantityUnits().treeList()
    # 获取根节点列表
    baseData.std95GoodsCategory_goodsQuantityUnits().rootList()
    # 获取每个根节点下面的子列表
    baseData.std95GoodsCategory_goodsQuantityUnits().singleList()


# 获取商品计量单位信息列表
@pytest.fixture(scope='class')
def goodsQuantityUnits():
    baseData.std95GoodsCategory_goodsQuantityUnits().pageList()


# 创建供应商
@pytest.fixture(scope='class')
def createSuppliers(createPkg, createBag):
    # 供应商
    global supplierId, suppliername
    supplierId, suppliername = business.createSuppliers('测试供应商')


# 厂家授权
@pytest.fixture(scope='class')
def manufacturerAuthorizations(createSuppliers):
    # 厂家授权
    manufacturerAuthorizations_id = business.manufacturerAuthorizations(supplierId, manufacturer_id, goodsList)
    # 绑定货票同行
    business.setInvoiceSync_and_getsupplierGoods_list(supplierId)

    yield manufacturerAuthorizations_id


# 厂家授权用例前置
@pytest.fixture(scope='class')
def manufacturerAuthorizations_01(manufacturerAuthorizations):
    # 根据id获取授权书详情
    business.manufacturerAuthorizations_id(manufacturerAuthorizations)
    # 修改供应商授权书
    business.edit_manufacturerAuthorizations(manufacturerAuthorizations)
    # 禁用授权书
    business.setDisabled(manufacturerAuthorizations)
    # 获取授权书中的商品信息
    business.getAuthorizationGoods(manufacturerAuthorizations)
    # 获取授权书列表
    business.getAuthorizationList(supplierId)
    # 根据厂商id和供应商id获取授权书列表
    business.get_manufacturerAuthorizations(manufacturerId=manufacturer_id, supplierId=supplierId)


# 启用商品
@pytest.fixture(scope='class')
def useGoods(manufacturerAuthorizations):
    # 启用商品
    goods.useGoods(goodsList[:1])


# 批量启用商品
@pytest.fixture(scope='class')
def batchUpdateStatus(manufacturerAuthorizations):
    # 批量启用商品
    goods.batchUpdateStatus(goodsList[1:])


# 绑定DI
@pytest.fixture(scope='class')
def bindDI(addGoods):
    # 绑定DI
    goods.bindDI(goodsList[0])


# 修改商品
@pytest.fixture(scope='class')
def editGoods(addGoods):
    # 修改商品
    goods.editGoods(goodsList[0])
    yield goodsList[0]  # 返回商品信息


# goods 所有查询接口
@pytest.fixture(scope='class')
def allGet_goodsType(editGoods):
    # 导出商品
    goods.export_goodsType()
    # 根据id获取商品详情
    goods.get_pageList_goods()
    # 分页获取商品列表（去处价格）
    goods.get_pageListWithoutPrice()
    # 根据部门获取商品列表，去除已生成定数包的
    goods.get_GoodsByDepartment()
    # 获取组合商品
    goods.get_SurgicalGoods()
    # 获取供应商关联的商品信息
    goods.get_supplierGoods()
    # 导出商品
    goods.export_goodsType()
    yield editGoods


# 设置默认的供应商
@pytest.fixture(scope='class')
def setDefaultSupplier(manufacturerAuthorizations):
    # 设置默认的供应商
    goods.setDefaultSupplier(goodsList[0], supplierId)


# 创建定数包
@pytest.fixture(scope='class')
def createBag(addGoods):
    # 定数包
    global bagId
    bagId = goods.createBag(goodsList[-1], name['goodsname']['lowbag'])


# 修改定数包
@pytest.fixture(scope='class')
def editBag(createBag):
    # 定数包
    goods.editBag(bagId, goodsList[-1], '修改' + name['goodsname']['lowbag'])


# 启用定数包 -- 异常
@pytest.fixture(scope='class')
def useBag_01(createBag):
    # 启用定数包
    goods.useBag(bagId)


# 启用定数包
@pytest.fixture(scope='class')
def useBag(useGoods, batchUpdateStatus):
    # 启用定数包
    goods.useBag(bagId)


# 创建科室
@pytest.fixture(scope='class')
def addDepartments(useGoods, useBag, usePkg_01):
    # 科室
    global list_data
    list_data = createDeparments.allCreate(name['departmentname'], name['department_name'])
    yield list_data[0]


# 编辑科室
@pytest.fixture(scope='class')
def editDepartments(addDepartments):
    createDeparments.editDepartments(list_data[0][0])
    yield list_data[0][0]


# 批量绑定科室和商品
@pytest.fixture(scope='class')
def batchBindDepartmentGoods(addDepartments):
    createDeparments.batchBindDepartmentGoods(list_data[0], goodsList[0])


# 移除科室商品
@pytest.fixture(scope='class')
def removeDepartmentGoods(addDepartments):
    createDeparments.removeDepartmentGoods(list_data[0][0])
    yield list_data[0][0]


# 删除科室信息
@pytest.fixture(scope='class')
def delDepartments(addDepartments):
    createDeparments.delDepartments(list_data[0][0])
    yield list_data[0][0]


# 科室剩余接口调用
@pytest.fixture(scope='class')
def departments_01(warehouseData):
    # 根据id获取组织详情
    createDeparments.getdepartmentsName(departmentsId=list_data[0][1])
    # 分页获取直接子节点组织列表
    createDeparments.pageList()
    # 获取组织树列表
    createDeparments.treeList()
    # 根据id获取父级组织
    createDeparments.getParent(list_data[0][1])
    # 分页查询科室商品
    createDeparments.getDepartmentGoodsWithPage(list_data[0][1])
    # 导出科室商品
    createDeparments.exportDepartmentGoods(list_data[0][1])
    # 设置仓库商品上下限
    createDeparments.addWarehouseGoodsLimit(goodsId=goodsList[0], warehouseId=warehouseData[1][0])
    # 修改仓库商品上下限
    createDeparments.updateWarehouseGoodsLimit(goodsId=goodsList[0], warehouseId=warehouseData[1][0])
    # 删除仓库商品上下限
    createDeparments.removeWarehouseGoodsLimit(list_data[0][1])
    # 设置科室商品并设置上下限
    createDeparments.setDepartmentGoods(goodsId=goodsList[2], departmentId=list_data[0][1],
                                        warehouseId=warehouseData[1][1])
    # 查询仓库商品列表
    createDeparments.getWarehouseGoodsList(departmentId=list_data[0][1], goodsId=goodsList[0])
    # 获取可以访问的非一级科室的科室名称和id
    createDeparments.getSelections()
    # 获取所有非一级科室的科室名称和id
    createDeparments.getAllSubDepartment()
    # 获取所有科室(包含一级科室)的科室名称和id
    createDeparments.getAllDepartment()
    # 解绑商品和部门
    createDeparments.unbindDepartmentGoods(goodsId=goodsList[2], departmentId=list_data[0][1])


@pytest.fixture(scope='class')
def hospital():
    # 设置当前医院
    createDeparments.hospital().setCurrentHospital()
    # 医院列表
    createDeparments.hospital().list()
    # 根据id获取医院院区详情
    createDeparments.hospital().get_id()
    # 获取医院院区列表
    createDeparments.hospital().get_list()
    # 获取医院职务列表
    createDeparments.hospital().get_jobTitle()


# 新增科室仓库、货区、货架流程
@pytest.fixture(scope='class')
def warehouseData(addDepartments):
    # 仓库ID
    global warehouseData
    warehouseData = baseData.warehouseData(list_data, name['code'])
    yield warehouseData


# 新增科室仓库、货区、货架--用例前置
@pytest.fixture(scope='class')
def warehouseData_01(addDepartments):
    barCode_list = []
    storageCabinets_list = []
    storageArea_list = []
    warehouse_list = []
    for x, y, z in zip(list_data[1], list_data[0], name['code']):
        warehouse_id = baseData.createWarehouse(x + '-仓库', y)
        storageArea_id = baseData.createCargo(x + '-货区', warehouse_id)
        barCodes = baseData.storageCabinets(x + '-货架', warehouse_id, storageArea_id, z)
        # 分页获取货柜列表
        storageCabinets_id = baseData.pageListStorageCabinets(x + '-货架')
        barCode_list.append(barCodes)
        storageCabinets_list.append(storageCabinets_id)
        storageArea_list.append(storageArea_id)
        warehouse_list.append(warehouse_id)

    # 仓库
    # 更新仓库信息
    baseData.editWarehouses(warehouse_list[0])
    # 根据id获取仓库详情
    baseData.get_id_warehouses(warehouse_list[0])
    # 查询部门的仓库信息
    baseData.getListByDepartment(list_data[0][0])
    # 查询部门的仓库信息
    baseData.getListByDepartmentIds(list_data[0][0])
    # 根据当前用户查询用户部门下所有的仓库
    baseData.getByUser()
    # 查询中心仓库
    baseData.getCentralWarehouse()
    # 推送组列表
    baseData.groupList()
    # 仓库货位汇总查询
    baseData.getSummaryInfo()
    # 仓库货位汇总导出
    baseData.exportWarehouses()

    # 货区
    # 更新库房信息
    baseData.update_storageAreas(storageArea_list[2])
    # 根据仓库id获取库房列表
    baseData.listByWarehouse(warehouse_list[2])
    # 查询中心库的库房列表
    baseData.listByCentralWarehouse()
    # 删除库房信息
    baseData.del_storageAreas(storageArea_list[3])

    # 货架
    # 更新货架信息
    baseData.edit_storageCabinets(storageCabinets_list[0])
    # 根据库房id获取货柜列表
    baseData.listByStorageArea(storageArea_list[0])
    # 根据id删除货柜信息
    baseData.del_storageCabinets(storageCabinets_list[1])

    # # 货区
    # storageArea_id = baseData.createCargo(list_data[1][0] + '-货区', warehouse_id)
    # # 货位
    # barCodes = baseData.storageCabinets(list_data[1][0] + '-货架', warehouse_id, storageArea_id, name['code'])

    yield warehouse_list[0], storageArea_list[2], storageCabinets_list[0]


# 科室绑定定数包
@pytest.fixture(scope='class')
def bindBag(warehouseData):
    # 科室绑定定数包
    goods.bindBag(list_data[0], warehouseData[1], bagId)


# 科室解绑定数包
@pytest.fixture(scope='class')
def unbindBag(bindBag):
    goods.unbindBag(list_data[0], bagId)


# 创建手术套包
@pytest.fixture(scope='class')
def createPkg(addGoods):
    # 手术套包
    global pkgId, combinedGoodsId
    pkgId, combinedGoodsId = goods.createPkg([goodsList[1], goodsList[2]], name['goodsname']['pkg'])
    yield pkgId


# 手术套包和定数吧哦查询接口补充
@pytest.fixture(scope='class')
def get_Bag_Pkg(addDepartments):
    # 手术套包和定数吧哦查询接口补充

    # 定数包
    # 根据id获取普通套包详情
    createGoods.createGoods().get_id_Bag(bagId)
    # 分页获取普通套包列表
    createGoods.createGoods().pageList_packageBulks()
    # 导出定数包
    createGoods.createGoods().export_packageBulks()
    # 普通套包条码打印
    createGoods.createGoods().printBarcode_packageBulks(bagId)
    # 查询部门绑定的定数包
    createGoods.createGoods().getDepartmentPackageBulk(list_data[0][0])
    # 查询部门未绑定的定数包
    createGoods.createGoods().getUnbindPackageBulk(list_data[0][0])
    # 查询部门所有仓库设置的定数包上下限
    createGoods.createGoods().findPackageWarehouseLimits()

    # 手术套包
    # 根据id获取手术套包详情
    createGoods.createGoods().get_id_Pkg(pkgId)
    # 根据id获取手术套包详情
    createGoods.createGoods().get_Pkg_getAllDetails(pkgId)
    # 导出手术套包
    createGoods.createGoods().export_Pkg()
    # 分页获取部门绑定的手术套包列表
    createGoods.createGoods().getDepartmentPackageSurgical(list_data[0][0])
    # 查询未绑定手术套包
    createGoods.createGoods().getUnbindSurgicalBulk()

    yield bagId, pkgId


# 修改手术套包
@pytest.fixture(scope='class')
def editPkg(createPkg):
    # 手术套包
    goods.editPkg(pkgId, name['goodsname']['pkg'])
    yield createPkg


# 修改手术套包
@pytest.fixture(scope='class')
def delPkg(createPkg):
    # 手术套包
    goods.delPkg(pkgId)
    yield createPkg


# 科室绑定手术套包
@pytest.fixture(scope='class')
def bindPkg(warehouseData):
    # 科室绑定手术套包
    goods.bindDepartment(list_data[0], warehouseData[1], pkgId)


# 诊疗项目科室绑定
@pytest.fixture(scope='class')
def diagnosis_project_department(warehouseData, diagnosisProject):
    # 查询科室诊疗项目列表
    baseData.diagnosis_project_department().getDepartmentDiagnosisProjectWithPage(departmentId=list_data[0][0])
    # 科室绑定诊疗项目
    baseData.diagnosis_project_department().bind(departmentId=list_data[0][0], warehouseId=warehouseData[0],
                                                 projectId=diagnosisProject)
    # 科室解绑诊疗项目
    baseData.diagnosis_project_department().unbin(departmentId=list_data[0][0], projectId=diagnosisProject)


# 科室解绑手术套包
@pytest.fixture(scope='class')
def unbindPkg(bindPkg):
    # 科室解绑手术套包
    goods.unbindDepartment(list_data[0], pkgId)


@pytest.fixture(scope='class')
def audit_History():
    audit.getAuditHistory(1, target='md_license_custodian_business')


@pytest.fixture(scope='class')
def audit_getPage():
    audit.getAuditWithPage(end=None, target='md_goods', freeText=None, hospitalId=104,
                           key=1, loginPhone=None, start=None, targetList=None, type='modify', userId=1, pageNum=0,
                           pageSize=50)


# 禁用手术套包
@pytest.fixture(scope='class')
def unUsePkg(createPkg):
    # 禁用手术套包
    goods.unUsePkg(pkgId)


# 异常——启用手术套包
@pytest.fixture(scope='class')
def usePkg(unUsePkg):
    # 启用手术套包
    goods.usePkg(pkgId)
    yield pkgId


# 异常——启用手术套包
@pytest.fixture(scope='class')
def usePkg_01(useGoods):
    # 启用手术套包
    goods.usePkg(pkgId)
    yield pkgId


# 科室绑定商品
@pytest.fixture(scope='class')
def setDepartmentGoods(warehouseData):
    # 科室绑定商品
    goods.setDepartmentGoods(list_data[0], warehouseData[1], goodsList[:3])


# 普通请领流程
@pytest.fixture(scope='class')
def goodsR_01(setDepartmentGoods, bindBag, bindPkg):
    # 请领流程
    goodsRequest.Request().all(goodsList[:3], warehouseData[1], bagId, combinedGoodsId)


# 采购流程
@pytest.fixture(scope='class')
def oaPurchase_01(goodsR_01):
    # 采购流程   返回配送单id
    global shippingOrderCode
    shippingOrderCode = createPurchase.purchase().oaPurchase(supplierId, num=24)


# 新建中心库货位
@pytest.fixture(scope='class')
def coreWarehouseData(createManufacturer):
    # 新建中心库货位
    global core_warehouseData
    core_warehouseData = baseData.core_warehouseData(name['core_code'])


# 中心库验收、上架
@pytest.fixture(scope='class')
def receivingOrder(coreWarehouseData, oaPurchase_01):
    # 中心库验收
    centralLibrary.receivingOrder().all_receivingOrder(shippingOrderCode)
    # 中心库上架
    global stock
    stock = centralLibrary.stock()
    stock.aoto_putOnShelf(core_warehouseData, name['core_code'])


# 中心库拣货
@pytest.fixture(scope='class')
def pickOrder(receivingOrder):
    # 中心库生成拣货单
    stock.aoto_add_pickOrder(name['core_code'])
    # 中心库拣货
    stock.aoto_pick_pickOrder(name['core_code'])


# 加工单
@pytest.fixture(scope='class')
def processingOrder(pickOrder):
    # 定数包加工组包
    package = centralLibrary.processing_package()
    # 定数包-生成拣货单
    package.aoto_processingOrder(name['core_code'])
    # 定数包-拣货
    stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
    # 加工赋码
    package.aoto_makingPackageBulk(name['core_code'])
    # 定数包上架
    stock.aoto_putOnShelf(core_warehouseData[-1], name['core_code'], type='bag')
    # 中心库 生成拣货单
    stock.aoto_add_pickOrder(name['core_code'], type='package_bulk')
    # 中心库拣货
    stock.aoto_pick_pickOrder(name['core_code'], type='bag')


# 用例前置加工单
@pytest.fixture(scope='class')
def processingOrder_01(pickOrder):
    # 定数包加工组包
    package = centralLibrary.processing_package()
    # # 定数包-生成拣货单
    package.aoto_processingOrder(name['core_code'])

    # 获取加工单id
    processingOrderId, pickOrder_code, pickOrder_id, description = package.getWithPage('Lowbag' + name['core_code'])

    # 查询详情
    package.getOne()
    # 制作加工单
    processingOrderId_new = package.makingProcessingOrder(bagId)
    # 加载定数包加工信息
    package.loadPackageBulkDetails(processingOrderId[0])
    # 加载定数包加工信息(在一个列表中)
    packageBulkId = package.loadPackageBulkDetailsInOne(processingOrderId[1])
    # 制作定数包
    package.makingPackageBulk(packageBulkId, processingOrderId[1])
    # 批量制作定数包
    package.batchMakingPackageBulk()

    # 获取加工单id
    processingOrderId, pickOrder_code, pickOrder_id, description = package.getWithPage('Pkg' + name['core_code'])
    # 加载手术套包加工信息
    package.loadSurgicalPkgBulkDetails(pkgId)
    # 加载手术套包加工信息(在一个列表中)
    surgicalPkgBulkId = package.loadSurgicalPkgBulkDetailsInOne(processingOrderId[0])
    # 查询未组包的拣货单明细
    loadUnpacked_list = package.loadUnpacked(processingOrderId[0])
    # 物资详情id
    goodsItemId_list = []
    for j in loadUnpacked_list.keys():
        # 查询库存列表
        goodsId, expirationDate, lotNum = stock.get_RepositoryStockWithPage(j)
        # 查询库存明细
        goodsItemCode, goodsItemId = stock.getStockDetails(goodsId, expirationDate, lotNum,
                                                           status='picked')
        if loadUnpacked_list[j] in goodsItemCode:
            new_goodsItemId = goodsItemId[goodsItemCode.index(loadUnpacked_list[j])]
            goodsItemId_list.append(new_goodsItemId)
        # 扫码制作手术套包
        package.getPackageSurgicalGoods(loadUnpacked_list[j], processingOrderId[0])
        # 扫码完成确认
    package.makingSurgicalPkgBulk(goodsItemId_list, processingOrderId[0], surgicalPkgBulkId)

    # 删除加工单
    package.removeProcessingOrder(processingOrderId_new)

    yield processingOrderId_new


# 测试前置---中心库拣货
@pytest.fixture(scope='class')
def pickOrder_01(receivingOrder):
    pickPending_id = stock.get_pickPending(name['core_code'], type='goods')
    # 取消待拣货数据
    stock.pickPending_cancel(pickPending_id[-1][-1])
    # 生成拣货单
    stock.add_pickOrder(pickPending_id[0])
    # 查询拣货单列表
    pickOrder_code, pickOrder_id = stock.get_pickOrderid(name['core_code'])
    # 查询拣货单明细
    goodsName_list, quantity, pickPendingId = stock.detail_pickOrder(pickOrder_code[0])

    goodsId, expirationDate, lotNum = stock.get_RepositoryStockWithPage(goodsName_list[0])
    # 物资条码列表
    goodsItemCode = stock.getStockDetails(goodsId, expirationDate, lotNum, status='put_on_shelf')
    if goodsItemCode != []:
        # 取物资条码第一个
        stock.pick_pickOrder(goodsItemCode[0], pickOrder_id[0], pickPendingId[0])

    # 打印拣货单
    stock.printPickOrder(pickOrder_id)
    # 根据仓库批量生成拣货单
    stock.batchGeneratePickOrder(warehouseData[1][:1])
    # 取消拣货单
    pickOrder_id_1 = stock.add_pickOrder(pickPending_id[1])
    stock.cancelPickOrder(pickOrder_id_1)

    # 取消拣货单
    pickOrder_id = stock.add_pickOrder(pickPending_id[2])
    stock.complete(pickOrder_id)

    yield pickOrder_id_1


# 推送单流程
@pytest.fixture(scope='class')
def Delivery(processingOrder):
    # 中心库推送
    global codeList
    codeList = centralLibrary.Delivery().all(list_data[0])


# 推送单用例前置
@pytest.fixture(scope='class')
def Delivery_01(processingOrder):
    delivery = centralLibrary.Delivery()
    # # 查出推送单ID
    allList = delivery.get_deliveryId(list_data[0])
    # 获取 推送单ID
    deliveryId = allList[0]
    # 获取 推送单 code
    codeList = allList[1]

    # 推送单复核
    checkId = delivery.check(codeList[0], deliveryId[0])
    # 推送单撤销复核
    delivery.uncheck(checkId)

    # 获取 itemsId
    itemsIds = delivery.get_itemsId(deliveryId)
    # 批量 复核商品
    delivery.batch_check(deliveryId, itemsIds)
    # 复核 推送单
    delivery.set_pusher(deliveryId)

    # 打印推送单
    delivery.printDeliveryOrder(deliveryId[0])
    # 推送单导出
    delivery.export()

    return codeList


# 科室验收
@pytest.fixture(scope='class')
def acceptance_Check(Delivery):
    print('推送单code: %s' % codeList)
    # 科室验收
    all_check.Check().all(codeList)


# 科室验收用例前置
@pytest.fixture(scope='class')
def acceptance_Check_01(Delivery):
    print('推送单code: %s' % codeList)
    check = all_check.Check()
    acceptanceOrderId = check.get_acceptanceOrderId(codeList)
    itemsIds = check.get_itemsId(acceptanceOrderId)
    # 验收
    check.check(acceptanceOrderId[:1], itemsIds[:1])
    # 取消验收
    check.uncheck(acceptanceOrderId[0], itemsIds[0][0])

    check.checkOneItem(acceptanceOrderId[0], codeList[0])

    check.submitOrder(acceptanceOrderId)

    # 打印验收单
    check.printDetail(acceptanceOrderId[0])


# 科室验收、上架
@pytest.fixture(scope='class')
def Department_Library(acceptance_Check):
    # # 科室上架
    print('仓库id：%s' % warehouseData[1])
    # 上架商品
    global goods_code
    goods_code = all_Deparments_putOnShelf.Deparment().all(warehouseData[1])
    # 上架定数包
    global package_code
    package_code = all_Deparments_putOnShelf.Deparment().all1(warehouseData[1])


# 扫码消耗-所有
@pytest.fixture(scope='class')
def consume_all(Department_Library):
    # 扫码消耗商品
    centralLibrary.consume().batchConsume(goods_code)
    # 扫码消耗定数包
    centralLibrary.consume().batchConsume(package_code)


# 货票同行
@pytest.fixture(scope='class')
def sybc_invoice():
    # 查询发票信息
    shippingOrderItemId, totalAmount = finance.invoice().getinvoiceSyncPageList(name['core_code'])
    x_list, y_list = shippingOrderItemId, totalAmount
    yield x_list, y_list


# 销后结算
@pytest.fixture(scope='class')
def finStates_invoice():
    # 分页获取销后结算开票列表
    goodsItemId, totalAmount = finance.invoice().invoiceFinStatesPageList('0609110932')
    x_list, y_list = goodsItemId, totalAmount
    yield x_list, y_list


# 发票流程
@pytest.fixture(scope='class')
def invoice_01(consume_all, sybc_invoice):
    # 发票流程
    invoice = finance.invoice()

    # 正向流程
    # 上传发票
    invoiceId_3, invoiceIdNumber = invoice.doCommitInvoiceSync(sybc_invoice[0][0], sybc_invoice[1][0],
                                                               name['core_code'],
                                                               releaseType='manual_invoice')
    # 审核发票
    invoice.approve(invoiceId_3)
    # 验收发票
    invoice.check(invoiceId_3)
    # 支付发票
    invoice.pay(suppliername, sybc_invoice[1][0], invoiceId_3)
    # 查看转账凭证
    invoice.getPaymentDetail(invoiceId_3)

    # 审核驳回作废
    # 上传发票
    invoiceId, invoiceIdNumber = invoice.doCommitInvoiceSync(sybc_invoice[0][1], sybc_invoice[1][1], name['core_code'],
                                                             releaseType='manual_invoice')
    # 审核发票
    invoice.approve(invoiceId, success=False)
    # 发票作废
    invoice.remove(invoiceId)

    # 审核驳回修改--手工货票同行
    # 上传发票
    invoiceId, invoiceIdNumber = invoice.doCommitInvoiceSync(sybc_invoice[0][2], sybc_invoice[1][2], name['core_code'],
                                                             releaseType='manual_invoice')
    # 审核发票
    invoice.approve(invoiceId, success=False)
    # 货票同行原票修改
    invoice.updateInvoiceSync(invoiceId)

    # 审核驳回 编辑---电子发票货票同行
    # 上传发票
    invoiceId, invoiceIdNumber = invoice.doCommitInvoiceSync(sybc_invoice[0][3], sybc_invoice[1][3], name['core_code'],
                                                             releaseType='electronic_invoice')
    # 审核发票
    invoice.approve(invoiceId, success=False)
    # 编辑电子发票
    invoice.updateElectronicInvoice(invoiceId)

    # 查询列表--待审核
    invoice.pageListApprovePending()
    # 待审核导出
    invoice.exportApprovePending()
    # 查询列表--待验收
    invoice.pageListCheckPending()
    # 获取所有开票企业
    invoice.getEnterpriseList()
    # 待验收导出
    invoice.exportCheckPending()
    # 查询列表--待支付
    invoice.pageListPayPending()
    # 待支付导出
    invoice.exportPayPending()
    # 查询列表--支付完成
    invoice.pageListPayFinished()
    # 支付完成导出
    invoice.exportPayFinished()
    # 查询列表--驳回
    invoice.pageListRejected()
    # 驳回导出
    invoice.exportRejected()
    # 分页获取销后结算开票列表
    invoice.invoiceFinStatesPageList()
    # # 根据发票号码查询蓝票
    invoice.getNormalInvoiceBySerialNumber(invoiceIdNumber)
    # 查询发票汇总信息
    invoice.getInvoiceSummary(invoiceId)

    # # 电子发票红冲
    # invoice.electronicReverse(invoiceId)

    # # 手工发票红冲
    # invoice.doCommitInvoiceManual(invoiceId)

    # # 修改手工红冲发票
    # invoice.updateManualReverseInvoice(invoiceId)
    # # 销后结算发票上传
    # invoice.doCommitInvoiceFinState(invoiceId)
    # 分页获取货票同行开票列表
    invoice.getinvoiceSyncPageList()

    # # 销后结算修改
    # invoice.updateInvoiceFinState(invoiceId)
    # 货票同行原票待修改详情
    invoice.getInvoiceSyncDetail(invoiceId)

    # 剩余发票流程
    # invoiceIdNumber_list, invoiceId_list = invoice.aoto_doCommitInvoiceSync(name['core_code'], suppliername)
    # 正向流程--手工发票
    # 上传发票
    invoiceId_1, invoiceIdNumber = invoice.doCommitInvoiceSync(sybc_invoice[0][-1], sybc_invoice[1][-1],
                                                               name['core_code'],
                                                               releaseType='manual_invoice')
    # 审核发票
    invoice.approve(invoiceId_1)
    # 验收发票
    invoice.check(invoiceId_1)
    # 支付发票
    invoice.pay(suppliername, sybc_invoice[1][-1], invoiceId_1)

    # 正向流程--电子发票
    # 上传发票
    invoiceId_2, invoiceIdNumber = invoice.doCommitInvoiceSync(sybc_invoice[0][-2], sybc_invoice[1][-2],
                                                               name['core_code'],
                                                               releaseType='electronic_invoice')
    # 审核发票
    invoice.approve(invoiceId_2)
    # 验收发票
    invoice.check(invoiceId_2)
    # 支付发票
    invoice.pay(suppliername, sybc_invoice[1][-2], invoiceId_2)

    yield invoiceId_1, invoiceId_2, invoiceId_3


# 退货流程
@pytest.fixture(scope='class')
def returngoods(invoice_01):
    # 科室退货
    goodsItemId_list = all_check.returnGoods().aoto_makeDepartmentReturnGoods(warehouseData[1])
    # 中心库上架
    centralLibrary.stock().aoto_putOnShelf(core_warehouseData, name['core_code'])

    # 中心库退货
    centralLibrary.returnGoods().aoto_makeReturnGoods(name['core_code'], supplierId)

    yield invoice_01


# 红冲发票
@pytest.fixture(scope='class')
def invoiceManual(returngoods):
    invoice = finance.invoice()
    # 红冲票流程
    # invoice.aoto_doCommitInvoiceManual(invoiceId_list)

    # 正向发票红冲--手工发票
    # 上传红冲发票
    invoiceId = invoice.doCommitInvoiceManual(returngoods[0])
    # 审核发票--不通过
    invoice.approve(invoiceId, success=False)
    # 修改手工红冲发票
    invoice.updateManualReverseInvoice(invoiceId)
    # 审核发票
    invoice.approve(invoiceId)
    # 验收发票
    invoice.check(invoiceId)

    # 正向发票红冲--电子发票
    # 上传红冲发票
    invoiceId = invoice.electronicReverse(returngoods[1])
    # 审核发票
    invoice.approve(invoiceId)
    # 验收发票
    invoice.check(invoiceId)

    yield returngoods[2]


# 发票流程--销后结算
@pytest.fixture(scope='class')
def invoice_02(statement, finStates_invoice):
    # 发票流程--销后结算
    invoice = finance.invoice()
    # invoiceIdNumber_list, invoiceId_list = invoice.aoto_doCommitInvoiceSync('0609110932', suppliername,
    # type='finStates', statementId=statement[0])

    # 正向流程
    # 上传发票
    invoiceId, invoiceIdNumber = invoice.doCommitInvoiceFinState(finStates_invoice[0][0], finStates_invoice[1][0],
                                                                 '0609110932', releaseType='manual_invoice',
                                                                 statementId=statement[0])
    # 审核发票
    invoice.approve(invoiceId)
    # 验收发票
    invoice.check(invoiceId)
    # 支付发票
    invoice.pay(suppliername, finStates_invoice[1][0], invoiceId)

    # 审核驳回修改--手工货票同行
    # 上传发票
    invoiceId, invoiceIdNumber = invoice.doCommitInvoiceFinState(finStates_invoice[0][1], finStates_invoice[1][1],
                                                                 '0609110932', releaseType='manual_invoice',
                                                                 statementId=statement[0])
    # 审核发票
    invoice.approve(invoiceId, success=False)
    # 货票同行原票修改
    invoice.updateInvoiceFinState(invoiceId)

    # 销后结算待修改详情
    invoice.getInvoiceFinStateDetail()


# 结算单流程
@pytest.fixture(scope='class')
def statement(consume_all):
    # 删除五月份结算单数据
    sql.sql_199().delete_fin_statement()
    # 自动生成结算单
    systemData.common().autoGenerateStatement()
    # 结算单流程
    statementId = finance.statement().auto_statement(supplierIds=80)

    yield statementId


@pytest.fixture(scope='class')
def consume_01(Department_Library):
    # 批量扫码消耗
    centralLibrary.consume().batchConsume(goods_code[:1])
    # 扫码消耗
    centralLibrary.consume().consume(goods_code[3])
    # 查询物资（商品、套包）
    centralLibrary.consume().search(goods_code[1])
    # 查询并消耗
    centralLibrary.consume().searchAndConsume(goods_code[2])
    # 分页查询商品消耗记录
    centralLibrary.consume().getGoodsConsumeWithPage()
    # 导出商品消耗记录
    centralLibrary.consume().exportGoodsConsume()
    # 分页查询定数包消耗记录
    centralLibrary.consume().getPackageBulkConsumeWithPage()
    # 导出定数包消耗记录
    centralLibrary.consume().exportPackageBulkConsume()
    # 分页查询手术套包消耗记录
    centralLibrary.consume().getSurgicalPackageConsumeWithPage()
    # 导出手术套包消耗记录
    centralLibrary.consume().exportSurgicalPackageConsume()
    # 查询消耗记录详情
    centralLibrary.consume().getConsumeDetails()
    # 扫码反消耗
    centralLibrary.consume().unconsume(goods_code[3])
    # 查询商品反消耗记录
    centralLibrary.consume().goodsUnconsumeRecords()
    # 查询定数包反消耗记录
    centralLibrary.consume().packageBulkUnconsumeRecords()
    # 查询手术套包反消耗记录
    centralLibrary.consume().packageSurgicalUnconsumeRecords()
    # 导出商品反消耗记录
    centralLibrary.consume().exportGoodsUnconsumeRecords()
    # 导出定数包反消耗记录
    centralLibrary.consume().exportPackageBulkUnconsumeRecords()
    # 导出手术套包反消耗记录
    centralLibrary.consume().exportPackageSurgicalUnconsumeRecords()
    # 查询定数包反消耗明细
    centralLibrary.consume().getPackageBulkUnconsumeDetail()
    # 查询手术套包反消耗明细
    centralLibrary.consume().getPackageSurgicalUnconsumeDetail()


@pytest.fixture(scope='class')
def consume_02(Department_Library):
    # 批量扫码反消耗
    centralLibrary.consume().batchUnconsume(goods_code[:1])


# 新增普通请领
@pytest.fixture(scope='class')
def goodsR(setDepartmentGoods, bindBag):
    # 请领流程
    goodsR = goodsRequest.Request()
    # 获取请领单ID
    Id = goodsR.goodsRequest(goodsList[:3], warehouseData[1], bagId)
    # 撤回
    goodsR.withdraw(Id[:2])
    # 修改请领单
    goodsR.edit_goodsRequest(Id[:1], goodsList[:3], warehouseData[1], bagId)
    # 获取 物资详情
    allList = goodsR.get_allList(Id)[2:]
    # 审核 请领
    goodsR.goodsApproval(allList, idlist=Id[2:])
    # 复核 请领
    goodsR.approvalReview(allList, idlist=Id[2:3])

    # 查询普通请领列表
    goodsR.get_list()
    # 根据id获取请领单信息
    goodsR.getById(Id[0])
    # 根据id和状态获取请领单信息
    goodsR.getByIdAndMessageType(Id[0])
    yield Id


# 删除请领单
@pytest.fixture(scope='class')
def goodsR_remove(goodsR):
    goodsRequest.Request().remove(goodsR[1])


# 医嘱收费
@pytest.fixture(scope='class')
def medicalAdvice():
    # 分页查询医嘱收费汇总
    his.medicalAdvice().getWithPage()
    # 导出医嘱收费汇总
    his.medicalAdvice().exportSummary()
    # 根据病例号/病人号/医嘱号 查询医嘱列表
    his.medicalAdvice().getListByNum()
    # 根据医嘱id查询该医嘱上已消耗的物资列表
    his.medicalAdvice().getConsumedGoodsList()
    # 分页查询医嘱信息(用于手术请领绑定医嘱)
    his.medicalAdvice().getMedicalAdviceList()
    # 分页查询医嘱信息
    his.medicalAdvice().getMedicalAdviceWithPage()
    # 提交医嘱(锁定)
    his.medicalAdvice().lock()
    # 查询医嘱收费详情(用于医嘱编辑)
    his.medicalAdvice().getMedicalAdviceCharge()
    # 医嘱反消耗
    his.medicalAdvice().unconsume()


# 手术管理
@pytest.fixture(scope='class')
def surgical():
    # 手术管理
    # 分页查询手术管理列表
    his.surgical().pageList()
    # 查看手术详情,包括手术信息,消耗物资信息
    his.surgical().getDetail()
    # 导出手术详情
    his.surgical().exportDetail()


# 报表
@pytest.fixture(scope='class')
def Statistic():
    #  获取所有可以访问的报表
    statistic.statistic().list()
    # 获取单个报表的源数据
    statistic.statistic().get_id()
    # 查询数据
    statistic.statistic().query()
    # 导出数据
    statistic.statistic().export()
    # 分页查询科室试剂库存报表
    statistic.reagentReport().reagentStockAmount()
    # 导出试剂库存报表
    statistic.reagentReport().exportReagentStockAmount()
    # 试剂库存记录
    statistic.reagentReport().reagentStockRecord()
    # 试剂库存记录
    statistic.reagentReport().exportReagentStockRecord()

    # 科室消耗汇总表
    statistic.departmentConsumeSummary().pageList()
    statistic.departmentConsumeSummary().export()

    # 入库汇总报表
    statistic.repositoryInBoundSummary().pageList()
    statistic.repositoryInBoundSummary().export()

    # 科室/医院报表
    statistic.reportDepartment().getMonthlyAmount()
    statistic.reportDepartment().getMonthlyGrowth()
    statistic.reportDepartment().getDepartmentCompare()
    statistic.reportDepartment().goodsConsumedRank()
    statistic.reportDepartment().monthlyTotalAmount()
    statistic.reportDepartment().getOverBaseDepartment()
    statistic.reportDepartment().timeConsume()
    statistic.reportDepartment().returnGoodsTimeConsume()
    statistic.reportDepartment().getIncrements()
    statistic.reportDepartment().getDepartmentGrowthCompare()
    statistic.reportDepartment().getHospitalTotalAmount()
    statistic.reportDepartment().getDepartmentTotalAmount()

    # 供应商/一级供应商报表
    statistic.reportSupplier().getMonthlyAmount()
    statistic.reportSupplier().getSupplierConsumeCompare()
    statistic.reportSupplier().getMonthlyGrowth()
    statistic.reportSupplier().timeConsume()
    statistic.reportSupplier().getIncrements()

    # 退货统计
    statistic.reportReturnGoods().centralWarehouseReturnGoodsStat()
    statistic.reportReturnGoods().export()
    # 仓库报表
    statistic.reportWarehouse().duration()
    statistic.reportWarehouse().info()


# 逻辑库盘库
@pytest.fixture(scope='class')
def logicStockTakingOrder():
    # 新增逻辑库盘库单
    logicStockTakingOrder_id = centralLibrary.logicStockTakingOrder().add(417)
    # 提交逻辑库盘库单
    centralLibrary.logicStockTakingOrder().submit(logicStockTakingOrder_id)
    # 逻辑库盘库单审核不通过
    centralLibrary.logicStockTakingOrder().approvalFailure(logicStockTakingOrder_id)
    # 删除逻辑库盘库单
    centralLibrary.logicStockTakingOrder().delete(logicStockTakingOrder_id)

    # 新增逻辑库盘库单
    logicStockTakingOrder_id = centralLibrary.logicStockTakingOrder().add(417)
    # 提交逻辑库盘库单
    centralLibrary.logicStockTakingOrder().submit(logicStockTakingOrder_id)
    # 逻辑库盘库单审核通过
    centralLibrary.logicStockTakingOrder().approvalSuccess(logicStockTakingOrder_id)

    # 查询逻辑库盘库单列表
    centralLibrary.logicStockTakingOrder().pageList()
    # 查询逻辑库盘库单
    centralLibrary.logicStockTakingOrder().get_id(logicStockTakingOrder_id)
    # 打印逻辑库盘库单
    centralLibrary.logicStockTakingOrder().print(logicStockTakingOrder_id)

    # 新增逻辑库盘库单
    logicStockTakingOrder_id = centralLibrary.logicStockTakingOrder().add(417)

    yield logicStockTakingOrder_id


# 逻辑库库存日志 & 逻辑库库存日志
@pytest.fixture(scope='class')
def logicStockOperation_logicStock():
    # 分页查询库存日志
    centralLibrary.logicStockOperation().pageList()
    # 库存日志导出
    centralLibrary.logicStockOperation().export()
    # 手工处理
    centralLibrary.logicStockOperation().process()

    # 逻辑仓库库存分页查询
    centralLibrary.logicStock().pageList()
    # 逻辑库库存导出
    centralLibrary.logicStock().export()


# 获取消息
@pytest.fixture(scope='class')
def message():
    # weChat拉取数据
    systemData.message().pull()
    systemData.message().pullMessage()
    systemData.message().unRead()
    systemData.message().doHander()
    systemData.message().doRead()
    systemData.message().list()
    systemData.message().loadMessageTypeByUser()
    systemData.message().doBatchRead()
    systemData.message().doBatchDelete()
    systemData.message().single()
    systemData.message().fetchLatestMessage()
    systemData.message().getMessageAndPermission()
    systemData.message().addMessageAndPermission()
    systemData.message().updateMessageAndPermission()
    systemData.message().deleteMessageAndPermission()


# 用户、角色、权限
@pytest.fixture(scope='class')
def usersPermissions(createManufacturer):
    # 添加用户
    loginPhone = systemData.users().add(name['core_code'])
    # 查询列表
    userId = systemData.users().usersPageList(loginPhone)
    # 修改
    systemData.users().editUser(userId)
    # 启用
    systemData.users().operate(userId)

    # 根据角色Id获取用户列表
    systemData.users().listByRoleId()
    # 根据组织Id获取用户列表
    systemData.users().listByDepartmentId()
    # 修改密码
    systemData.users().updatePwd('123456', '123456')
    # 重置密码
    systemData.users().adminUpdatePwd(userId)
    # 查询拣货员列表
    systemData.users().getPickerList()
    # 查询推送员列表
    systemData.users().getPusherList()
    # 查询用户基本信息
    systemData.users().getUserBaseInfo(userId)

    # 角色
    # 新增角色
    roleName = systemData.role().add(name['core_code'])
    # 分页获取角色列表
    roleId = systemData.role().pageList(roleName)
    # 更新角色信息
    systemData.role().editRole(roleId)
    # 根据id获取角色详情
    systemData.role().get_id(roleId)
    # 角色启用/禁用
    systemData.role().operate(roleId)
    # 根据type获取角色列表
    systemData.role().listByTypeAndHospitalId()

    # 权限
    # 新增权限数据
    systemData.permissions().add(name['core_code'])
    # 获取权限列表
    permissionsId = systemData.permissions().permissionsPageList()
    # 更新权限信息
    systemData.permissions().editPermissions(permissionsId)
    # 根据医院查询用户的权限
    systemData.permissions().findByHospital()
    # 根据医院查询菜单
    systemData.permissions().getMenus()
    # 查询菜单权限树
    systemData.permissions().getPermissionTree()
    # 重新加载接口权限
    systemData.permissions().reloadPermissionInterface()

    # 角色绑定用户
    systemData.roleUser().bind(roleId, [userId])
    # 用户解绑角色
    systemData.roleUser().unbind(roleId, [userId])

    yield userId, roleId, permissionsId


@pytest.fixture(scope='class')
def usersPermissions_01():
    body_data.clear()

    # 查询列表
    userId = systemData.users().usersPageList()


# 打印机相关接口
@pytest.fixture(scope='class')
def printer():
    systemData.printer().getListByUser()


@pytest.fixture(scope='class')
def SystemData():
    # 判断是否已登录
    systemData.Login().verify_login()

    # 词典
    systemData.dictionary().list()
    systemData.dictionary().getDictByCategory()
    systemData.dictionary().getByCategory()
    systemData.dictionary().listDictAllCategory()
    systemData.dictionary().getDictLabelAllCategory()
    systemData.dictionary().getDictAllCategory()

    # 地区
    systemData.districts().listProvinces()
    systemData.districts().listChildren()
    systemData.districts().listSiblings()
    systemData.districts().getParentPaths()

    # 一键审批
    systemData.batchApproval().oneClick()

    # 验证码
    systemData.captcha().get()
    systemData.captcha().check()

    # 物资类别管理
    systemData.category().getAll12()
    systemData.category().getAll18()

    # 配置
    systemData.config().list()
    systemData.config().fields()

    # 公共接口
    systemData.common().autoGenerateProcessingOrder()
    systemData.common().autoGeneratePurchasePlan()
    systemData.common().autoGenerateStatement()
    systemData.common().autoGeneratePickPendingOrder()
    systemData.common().autoGenerateHistoryInventory()
    systemData.common().autoCheckDepartmentReturnGoods()
    systemData.common().loadMessageRecord()
    systemData.common().redeliveryMessage()

    # 打印服务
    systemData.print_api().loadPrintingData()
    systemData.print_api().batchLoadPrintingData()
    systemData.print_api().printSuccess()


# 医生
@pytest.fixture(scope='class')
def doctor():
    # 根据id查询医生信息
    his.doctor().get_id()
    # 根据医生查询手术请领
    his.doctor().getDoctorSurgicalRequest()


# 病人信息
@pytest.fixture(scope='class')
def patient():
    # 根据id查询病人信息
    his.patient().get_id()
    # 根据病人查询手术请领
    his.patient().getPatientSurgicalRequest()
    # /查询病人普通消耗
    his.patient().getPatientConsumed()


# pda待办任务
@pytest.fixture(scope='class')
def unprocessedCount():
    centralLibrary.unprocessedCount().getCount()


# 新建一级供应商
@pytest.fixture(scope='class')
def custodian(createManufacturer):
    custodian = addbusiness.addBusiness(name['core_code'])
    # 新增一级供应商
    custodian_id = custodian.createCustodian('测试一级供应商')
    # 更新一级供应商
    custodian.edit_Custodian(custodian_id, '测试一级供应商')
    # 启用/禁用
    custodian.operateCustodian(custodian_id)
    # 根据id获取一级供应商详情
    custodian.get_Custodian_id(custodian_id)
    # 分页获取一级供应商列表
    custodian.getpageList('custodian', '测试一级供应商')
    # 获取可用的一级供应商
    custodian.getAvailableCustodians()
    # 设置一级供应商账期
    custodian.setAccountPeriod(custodian_id)
    yield custodian_id


# 成本——进销存
@pytest.fixture(scope='class')
def cost_invoicing():
    # 成本
    # 分页查询
    finance.cost().pageList()
    # 查询成本明细
    finance.cost().getDetail()
    # 导出
    finance.cost().export()

    # 进销存
    # 列表查询
    finance.invoicing().pageList()
    # 导出
    finance.invoicing().export()


# 成本——进销存
@pytest.fixture(scope='class')
def globalSearch():
    # 获取查询类型列表
    typeList = systemData.globalSearch().searchTypeList()
    # 全局搜索
    systemData.globalSearch().search()
    # 根据条码查询商品生命周期
    systemData.globalSearch().goodsLife()
    # 根据条码查询商品生命周期
    systemData.globalSearch().goodsItemLife()
    # 根据GS1查询商品信息
    systemData.globalSearch().gs1Decoding()

    # 无权限token
    headers = systemData.Login().login('spw_2', '123456')

    yield typeList, headers


# 首页GSP提醒接口，历史库存
@pytest.fixture(scope='class')
def gsp_history():
    # 产品注册证提醒
    systemData.gsp().goodsRegisterRemindList()
    # 企业证照提醒
    systemData.gsp().companyLicenseRemindList()
    # 获取商品历史库存列表
    systemData.history().list()
    # 获取定数包历史库存列表
    systemData.history().listByPackageBulk()
    # 获取手术套包历史库存列表
    systemData.history().listByPackageSurgical()


# 保存alias
@pytest.fixture(scope='class')
def jpush():
    # 保存alias
    systemData.jpush().save()


@pytest.fixture(scope='function')
def creatRole(createManufacturer):
    a = role.role().addRole(name['rolename'])
    print(a)
