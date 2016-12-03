# coding=utf-8
"""
Created on 2016.11.24
@author: 张晓君
"""

import http.cookiejar
import urllib.request
import urllib.parse
import re


class LoginCQUTCookie:
    # URL
    login_page_url = 'http://i.cqut.edu.cn/zfca/login?service=http%3A%2F%2Fi.cqut.edu.cn%2Fportal.do'
    login_url = 'http://i.cqut.edu.cn/zfca/login?service=http%3A%2F%2Fi.cqut.edu.cn%2Fportal.do'
    # 个人信息
    username = ''
    password = ''

    def __init__(self):
        if self.username == '':
            self.username = str(input('please enter your id: '))
        if self.password == '':
            self.password = str(input('please enter your password: '))

    def login(self):
        cookie = http.cookiejar.MozillaCookieJar()  # 使用 Cookie
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        # 开始获取请求地址
        rep = opener.open(self.login_page_url)
        html = rep.read()
        # print(html.decode("GBK"))
        lt = re.findall(b'lt" value="(.*)"', html)  # 提取 lt 的 value
        post_data = urllib.parse.urlencode({
            'useValidateCode': '0',
            'isremenberme': '0',
            'ip': '',
            'username': self.username,
            'password': self.password,
            'losetime': '30',
            'lt': lt[0],
            '_eventId': 'submit',
            'submit1': ''
        }).encode('utf-8')
        rep = opener.open(self.login_url, post_data)  # 模拟登陆
        return opener
