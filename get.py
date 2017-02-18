#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import http.cookiejar
import urllib.request
import urllib.parse

import sys

login_page_url = 'http://i.cqut.edu.cn/zfca/login?service=http%3A%2F%2Fi.cqut.edu.cn%2Fportal.do'
login_url = 'http://i.cqut.edu.cn/zfca/login?service=http%3A%2F%2Fi.cqut.edu.cn%2Fportal.do'
username = sys.argv[0]
password = sys.argv[1]


def login():
    cookie = http.cookiejar.MozillaCookieJar()  # 使用 Cookie
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    # 开始获取请求地址
    rep = opener.open(login_page_url)
    html = rep.read()
    # print(html.decode("GBK"))
    lt = re.findall(b'lt" value="(.*)"', html)  # 提取 lt 的 value
    post_data = urllib.parse.urlencode({
        'useValidateCode': '0',
        'isremenberme': '0',
        'ip': '',
        'username': username,
        'password': password,
        'losetime': '30',
        'lt': lt[0],
        '_eventId': 'submit',
        'submit1': ''
    }).encode('utf-8')
    rep = opener.open(login_url, post_data)  # 模拟登陆
    return opener


def main():
    print('')

if __name__ == '__main__':
    main()
