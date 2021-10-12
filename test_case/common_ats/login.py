#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2021/9/22 15:56 
# @Author   : 蓦然
# @File     : login.py
# Project   : ATS
import requests
from selenium.webdriver.chrome import webdriver
import logging


def login_configure():
    url = "https://" + "ats-test" + ".51zhaopin.cn/pic/api/login/wework/third/code?code=110120&suiteId=wwbddcd1884a9dc2c5&state=wwbddcd1884a9dc2c5"
    res = requests.get(url).json()
    token = res.get("data").get("token")
    logging.info("获取token为", token)
    return token


def configure():
    option = webdriver.ChromeOptions()
    option.add_argument('user-agent=wxwork')
    driver = webdriver.Chrome(options=option)
    driver.get("https://" + "ats-test" + ".51zhaopin.cn/favicon.ico")
    accessToke = driver.execute_script("window.localStorage.setItem('qw_token',"
                                       "'cookie')".replace('cookie', login_configure()))
    accessToken = driver.execute_script("return localStorage.getItem('qw_token')")
    status = driver.add_cookie({'name': 'p', 'value': 'true'})
    return driver


if __name__ == '__main__':
    login_configure
