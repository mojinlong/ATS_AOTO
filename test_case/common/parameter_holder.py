# _*_ coding: utf-8 _*_
# __author:"scott"
# date:2020/06/26


class ParameterHolder(object):
    """
    define parameters used for those test cases.
    """

    def __init__(self):
        self.hospital_id = None
        # 登录用户名
        self.login_phone = None
        # 请领商品参数
        self.goods_id = None
        # 商品物资编号
        self.goods_code = None
        # 测试科室库id
        self.warehouse_id = None
        # 测试科室id
        self.department_id = None
        # 采购商品参数
        self.purchase_goods_id = None
        # 定数包id
        self.package_bulk_id = None
        # 定数包物资编号
        self.package_bulk_code = None
        # 定数包中商品id
        self.bulk_goods_id = None
        # 定数包物资编号
        self.bulk_goods_code = None
        # 手术套包id
        self.surgical_package_id = None
        # 手术套包编号
        self.surgical_package_code = None
        # 中心库id
        self.central_warehouseId = None
        # 合格区id
        self.standard_area = None
        # 订单号
        self.order_id = None

    def set_hospital_id(self, hospital_id):
        self.hospital_id = hospital_id
