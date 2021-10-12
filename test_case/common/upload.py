#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/16 10:16
# @File     : upload.py
# @Project  : integration-tests-insight

import request


def uploadSupplier(file_name):
    """
    导入供应商信息
    :return:
    """
    upload_res = request.post_file('/api/admin/uploadSupplier/1.0/upload', file_name=file_name)


if __name__ == '__main__':
    uploadSupplier('供应商_正确.zip')
