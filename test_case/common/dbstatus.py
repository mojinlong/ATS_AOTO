# __author:"zonglr"
# date:2020/5/28
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
from test_config import param_config
from common import postgresql

db = postgresql.PostgresSql()
hospital_id = param_config.hospital_id
"""
通过修改数据库修改商品、商品实例、单据等状态
is_enabled、is_delete
"""


# 不可以修改数据库内容
# 删除定数包
def delete_package_bulk(id):
    sql = "update md_goods set is_deleted = true " \
          "where id = {id} and hospital_id = {hospital_id};".format(id=id, hospital_id=hospital_id)
    db.execute(sql)


# 恢复删除定数包
def cancel_delete_package_bulk(id):
    sql = "update md_goods set is_deleted = false " \
          "where id = {id} and hospital_id = {hospital_id};".format(id=id, hospital_id=hospital_id)
    db.execute(sql)


# 不可以修改数据库内容
# 禁用手术套包
def disable_surgical_package(id):
    sql = "update md_package_surgical set is_enabled = false " \
          "where id = {id} and hospital_id = {hospital_id};".format(id=id, hospital_id=hospital_id)
    db.execute(sql)


# 启用手术套包
def enable_surgical_package(id):
    sql = "update md_package_surgical set is_enabled = true " \
          "where id = {id} and hospital_id = {hospital_id};".format(id=id, hospital_id=hospital_id)
    db.execute(sql)


# 不可以修改数据库内容
# 删除手术套包
def delete_surgical_package(id):
    sql = "update md_goods set is_deleted = true " \
          "where id = {id} and hospital_id = {hospital_id};".format(id=id, hospital_id=hospital_id)
    db.execute(sql)


# 恢复删除手术套包
def cancel_delete_surgical_package(id):
    sql = "update md_goods set is_deleted = false " \
          "where id = {id} and hospital_id = {hospital_id};".format(id=id, hospital_id=hospital_id)
    db.execute(sql)


# 删除采购计划
def delete_plan(planId):
    sql = "update oms_purchase_plan set is_deleted = true " \
          "where id = {planId} and hospital_id = {hospital_id};".format(planId=planId, hospital_id=hospital_id)
    db.execute(sql)


# 恢复删除采购计划
def cancel_delete_plan(planId):
    sql = "update oms_purchase_plan set is_deleted = false " \
          "where id = {planId} and hospital_id = {hospital_id};".format(planId=planId, hospital_id=hospital_id)
    db.execute(sql)


# 删除验收单
def delete_receiving_order(receivingId):
    sql = "update oms_receiving_report set is_deleted = true " \
          "where id = {receivingId} and hospital_id = {hospital_id};".format(receivingId=receivingId,
                                                                             hospital_id=hospital_id)
    db.execute(sql)


# 恢复删除验收单
def cancel_delete_receiving_order(receivingId):
    sql = "update oms_receiving_report set is_deleted = false " \
          "where id = {receivingId} and hospital_id = {hospital_id};".format(receivingId=receivingId,
                                                                             hospital_id=hospital_id)
    db.execute(sql)


# 删除验收单中的仓库

warehouse_id = ''


def delete_receiving_order_warehouse(receivingId):
    global warehouse_id
    # 查询仓库id
    sql = "select warehouse_id from oms_receiving_report " \
          "where id = {receivingId} and hospital_id ={hospital_id};".format(receivingId=receivingId,
                                                                            hospital_id=hospital_id)
    result = db.selectOne(sql)
    warehouse_id = result[0]
    # 删除验收单中的仓库id
    sql2 = "update oms_receiving_report set warehouse_id = {warehouse_id} " \
           "where id = {receivingId} and hospital_id ={hospital_id};".format(warehouse_id=warehouse_id,
                                                                             receivingId=receivingId,
                                                                             hospital_id=hospital_id)
    db.execute(sql2)
    return warehouse_id


# 删除推送单
def delete_delivery_order(deliveryId):
    sql = "update wms_delivery_order set is_deleted = true " \
          "where id = {deliveryId} and hospital_id = {hospital_id};".format(deliveryId=deliveryId,
                                                                            hospital_id=hospital_id)
    db.execute(sql)


# 取消删除推送单
def cancel_delete_delivery_order(deliveryId):
    sql = "update wms_delivery_order set is_deleted = false " \
          "where id = {deliveryId} and hospital_id = {hospital_id};".format(deliveryId=deliveryId,
                                                                            hospital_id=hospital_id)
    db.execute(sql)


# 删除商品实例
def delete_goods_item(operator_barcode):
    if 'ID' in operator_barcode:
        sql = "update md_goods_item set is_deleted = true " \
              "where operator_barcode = '{operator_barcode}' and hospital_id ={hospital_id};".format(
            operator_barcode=operator_barcode, hospital_id=hospital_id)
        db.execute(sql)
    elif 'PS' in operator_barcode:
        sql2 = "update md_package_surgical_item set is_deleted = true " \
               "where operator_barcode = '{operator_barcode}' and hospital_id ={hospital_id};".format(
            operator_barcode=operator_barcode, hospital_id=hospital_id)
        db.execute(sql2)
    elif 'PB' in operator_barcode:
        sql3 = "update md_package_bulk_item set is_deleted = true " \
               "where operator_barcode = '{operator_barcode}' and hospital_id ={hospital_id};".format(
            operator_barcode=operator_barcode, hospital_id=hospital_id)
        db.execute(sql3)
    else:
        raise Exception('传入的条码不正确')


# 取消删除商品实例
def cancel_delete_goods_item(operator_barcode):
    if 'ID' in operator_barcode:
        sql = "update md_goods_item set is_deleted = false " \
              "where operator_barcode = '{operator_barcode}' and hospital_id ={hospital_id};".format(
            operator_barcode=operator_barcode, hospital_id=hospital_id)
        db.execute(sql)
    elif 'PS' in operator_barcode:
        sql2 = "update md_package_surgical_item set is_deleted = false " \
               "where operator_barcode = '{operator_barcode}' and hospital_id ={hospital_id};".format(
            operator_barcode=operator_barcode, hospital_id=hospital_id)
        db.execute(sql2)
    elif 'PB' in operator_barcode:
        sql3 = "update md_package_bulk_item set is_deleted = false " \
               "where operator_barcode = '{operator_barcode}' and hospital_id ={hospital_id};".format(
            operator_barcode=operator_barcode, hospital_id=hospital_id)
        db.execute(sql3)
    else:
        raise Exception('传入的条码不正确')


# 删除仓库
def delete_warehouse(warehouse_id):
    sql = "update md_warehouse set is_deleted = true where id = {id};".format(id=warehouse_id)
    db.execute(sql)


# 取消删除仓库
def cancel_delete_warehouse(warehouse_id):
    sql = "update md_warehouse set is_deleted = false where id = {id};".format(id=warehouse_id)
    db.execute(sql)
