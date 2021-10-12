# __author:"zonglr"
# date:2020/6/17
# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import os, configparser, psycopg2, pprint
from psycopg2 import pool
import threading

# 调用配置文件方法，读取配置文件
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
file = root_dir + '/test_config/' + 'config-200.ini'
config = configparser.ConfigParser()
config.read(file, encoding='UTF-8')
# 数据库
host = config.get('database', 'host')
port = config.get('database', 'port')
user = config.get('database', 'user')
password = config.get('database', 'password')
database = config.get('database', 'database')
schema = config.get('database', 'schema')
db = psycopg2.connect(host=host, port=int(port), user=user, password=password, database=database,
                      options='-c search_path={schema}'.format(schema=schema))


class PostgresSql:
    # 加锁
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with PostgresSql._instance_lock:
                PostgresSql._instance = super().__new__(cls)
                try:
                    PostgresSql._instance.connectPool = pool.SimpleConnectionPool(2, 10, host=host, port=port,
                                                                                  user=user, password=password,
                                                                                  database=database,
                                                                                  options='-c search_path={schema}'.format(
                                                                                      schema=schema),
                                                                                  keepalives=1, keepalives_idle=30,
                                                                                  keepalives_interval=10,
                                                                                  keepalives_count=5)
                except Exception as e:
                    print(e)
        return PostgresSql._instance

    def getConnect(self):
        conn = self.connectPool.getconn()
        cursor = conn.cursor()
        return conn, cursor

    def closeConnect(self, conn, cursor):
        cursor.close()
        self.connectPool.putconn(conn)

    def closeAll(self):
        self.connectPool.closeall()

    # 执行增删改
    def execute(self, sql, vars=None):
        conn, cursor = self.getConnect()
        try:
            cursor.execute(sql, vars)
            conn.commit()
            self.closeConnect(conn, cursor)
        except Exception as e:
            conn.rollock()
            raise e

    def selectOne(self, sql):
        conn, cursor = self.getConnect()
        cursor.execute(sql)
        result = cursor.fetchone()
        self.closeConnect(conn, cursor)
        return result

    def selectAll(self, sql):
        conn, cursor = self.getConnect()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeConnect(conn, cursor)
        return result


if __name__ == '__main__':
    a = PostgresSql().selectAll('select  permission_id from md_role_permission')
    list(a)
    # print(type(a))
    # for i in a:
    #     print(i)

