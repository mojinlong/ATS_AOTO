#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Spw
# @Time     : 2021/6/10 16:58
# @File     : sql.py
# @Project  : integration-tests-insight

import postgresql


class sql_199:

    def delete_fin_statement(self):
        """
        删除结算单信息
        :return:
        """
        sql = """
        DELETE FROM fin_statement_detail WHERE parent_id IN (SELECT id FROM fin_statement WHERE "name" = 'Phmedtech医院2021年05月结算单');

        DELETE FROM fin_statement_period WHERE period_name = '2021年05月';
        
        DELETE FROM fin_invoice_detail WHERE fin_statement_id IN (SELECT id FROM fin_statement WHERE "name" = 'Phmedtech医院2021年05月结算单');

        DELETE FROM fin_statement WHERE "name" = 'Phmedtech医院2021年05月结算单';

        """
        postgresql.PostgresSql().execute(sql)


if __name__ == '__main__':
    sql_199().delete_fin_statement()
