# # -*- coding: utf-8 -*-
# # @Time : 2021/1/28 2:17 下午
# # @Author : lsj
# # @File : all_deliveryOrder.py
#
# # 已经整理到了centralLibrary.py，该文件暂不更新
# import request
#
#
# # 中心库 推送
# class Delivery:
#
#
#     # 查出推送单ID
#     def get_deliveryId(self, departmentId):
#         """
#         :param departmentId: 科室ID
#         :param warehouseId: 仓库ID
#         """
#         deliveryId = []
#         codeList = []
#         for i in departmentId:
#             params = {
#                 'pageNum': 0,
#                 'pageSize': 20,
#                 'departmentIds': i
#                 # 'status': status, #订单状态
#             }
#             response = request.get_params('/api/admin/deliveryOrder/1.0/list', params=params)
#
#             # 这里如果 定数包和商品都有的话 接口返回的格式不一样了，ID code 需要重新取一次
#             for i in response['data']['rows']:
#                 deliveryId.append(i['id'])
#                 codeList.append(i['code'])
#             # 拣货单code
#             codeList.append(response['data']['rows'][0]['code'])
#             # print('推送单ID：--%s' % deliveryId)
#             print(deliveryId)
#         return deliveryId, codeList
#
#     # 查出itemsID
#     def get_itemsId(self, deliveryId):
#         """
#         :param deliveryId: 推送单id
#         :return:
#         """
#         itemsIds = []
#         for i in deliveryId:
#             params = {
#                 'deliveryId': i
#             }
#             response = request.get_params('/api/admin/deliveryOrder/1.0/detail', params=params)
#             itemId = []
#             for j in response['data']['detail']:
#                 itemId.append(j['id'])
#             itemsIds.append(itemId)
#             # print('itemsId:%s' % itemsIds)
#         return itemsIds
#
#     # 批量复核
#     def batch_check(self, deliveryId, itemsIds):
#         """
#         :param deliveryId: 推送单id
#         :param itemsIds: items id
#         :return:
#         """
#         for i, j in zip(deliveryId, itemsIds):
#             body = {
#                 "deliveryOrderId": i,
#                 "status": "pass",
#                 "itemsIds": j
#             }
#             response = request.post_body('/api/admin/deliveryOrder/1.0/batchCheck', body=body)
#             try:
#                 response['msg'] == '操作成功'
#             except:
#                 raise Exception(response)
#
#     # 复核推送单
#     def set_pusher(self, deliveryId):
#         for i in deliveryId:
#             body = {
#                 "pusherId": 15,
#                 "deliveryOrderId": i
#             }
#             response = request.post_body('/api/admin/deliveryOrder/1.0/setPusher', body=body)
#             try:
#                 response['msg'] == '操作成功'
#             except:
#                 raise Exception(response)
#
#     def all(self, departmentId):
#         """
#         :param departmentId: 科室ID
#         :return:
#         """
#         allList = self.get_deliveryId(departmentId)
#         # 获取 推送单ID
#         deliveryId = allList[0]
#         # 获取 推送单 code
#         codeList = allList[1]
#         # 获取 itemsId
#         itemsIds = self.get_itemsId(deliveryId)
#         # 批量 复核商品
#         self.batch_check(deliveryId, itemsIds)
#         # 复核 推送单
#         self.set_pusher(deliveryId)
#         return codeList
#
#
# if __name__ == '__main__':
#     a = Delivery()
#     # a.get_deliveryId([268, 269, 270, 271])
#     # a.get_itemsId([2959, 2958, 2957, 2956])
#     # a.batch_check([2959, 2958, 2957, 2956],[[16790, 16791, 16789], [16787, 16788, 16786], [16784, 16785, 16783], [16781, 16782, 16780]])
#     # a.set_pusher([2959, 2958, 2957, 2956])
#     result = a.all([584, 585, 586, 587])
#     print(result)
