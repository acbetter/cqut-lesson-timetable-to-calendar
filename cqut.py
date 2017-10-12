#  -*- coding: utf-8 -*-

#            __     __     __   _____  _____   __    ___
#    /\     /      |  )   |       |      |    |     |   \
#   /__\   |       |--    |--     |      |    |--   |___/
#  /    \   \__)   |__)   |__     |      |    |__   |   \_


__title__ = 'class-schedule2ics for cqut'
__description__ = 'Spider Class Schedule of CQUT and Save to iCalendar file for Calendar App.'
__url__ = 'https://acbetter.com'
__version__ = '0.1'
__author__ = 'AC Better'
__author_email__ = 'acbetter@foxmail.com'
__license__ = 'GPL-3.0'
__copyright__ = 'Copyright 2017 AC Better'

"""
class-schedule2ics
~~~~~~~~~~~~~~~~~~~~~


"""
import os
import re
import sys
import getopt
import logging
from uuid import uuid1
from pprint import pprint
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, time, timedelta, timezone

import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event


class CssGetter(object):
    Headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.95 Safari/537.36'}
    URL = {
        'login': 'http://i.cqut.edu.cn/zfca/login?service=http%3A%2F%2Fi.cqut.edu.cn%2Fportal.do',
        'schedule': 'http://i.cqut.edu.cn/zfca?yhlx=student&login=0122579031373493728&url=xskbcx.aspx'
    }

    def __init__(self):
        self.argv = sys.argv
        os.chdir(str(self.argv[0]).rsplit('/', maxsplit=1)[0])
        self.logger = self.logger_creator()

        self.username, self.password = '', ''
        self.session = requests.Session()
        self.lt = None
        self.schedule = []
        self.date_start = None

    @staticmethod
    def logger_creator():
        """脚本日志处理"""
        logger_ = logging.getLogger('cqut.py')
        logger_.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('cqut.log', 'w', 'utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
        logger_.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
        logger_.addHandler(console_handler)

        logger_.info('正在执行脚本...')
        return logger_

    def get_username_password(self):
        """解析命令行参数 得到用户名和密码"""
        try:
            opts, args = getopt.getopt(self.argv[1:], 'hu:p:', ['username=', 'password='])
        except getopt.GetoptError:
            self.logger.info('你的打开方式不对！请重新输入命令')
            self.logger.info('cqut.py -u <username> -p <password>')
            sys.exit(-1)
        for opt, arg in opts:
            if opt in ('-u', '--username'):
                self.username = arg
            elif opt in ('-p', '--password'):
                self.password = arg
        if self.username is None:
            self.username = input('请输入你的学号: ')
        if self.password is None:
            self.password = input('请输入你的密码: ')

    def user_login(self):
        """模拟登录数字化校园"""
        r = self.session.get('http://ip.cn')
        soup = BeautifulSoup(r.text, 'html5lib')
        self.logger.debug(r.text.replace('\n', ''))
        self.logger.debug(' '.join(re.split('[	 \n]+', soup.text)).strip())
        self.logger.info('正在准备登录数字化校园...')
        try:
            self.logger.info('正在尝试打开数字化校园...')
            self.session.headers = CssGetter.Headers
            r = self.session.get(url=CssGetter.URL['login'])
            value_lt = re.findall(r'name="lt" value="(.*?)"', r.text)[0]
            self.lt = value_lt
            data = {'useValidateCode': '0',
                    'isremenberme': '0',
                    'ip': '',
                    'username': self.username,
                    'password': self.password,
                    'losetime': '30',
                    'lt': value_lt,
                    '_eventId': 'submit',
                    'submit1': ''}
            r = self.session.post(url=CssGetter.URL['login'], data=data)
            soup = BeautifulSoup(r.text, 'html5lib')
            self.logger.info('正在获取用户信息...')
            name = soup.select('div > em')[0].text
            self.logger.info('登录成功！' + name)
        except IndexError:
            self.logger.error('登录失败！请检查账号密码是否有误，网络连接及代理配置是否正常。')
            self.logger.debug('下面是登录页信息:')
            self.logger.debug(r.text.replace('\n', ''))

    def get_schedule(self):
        """爬取课程表信息"""
        self.logger.info('正在准备爬取课程表信息...')
        r = self.session.get(url=CssGetter.URL['schedule'])
        soup = BeautifulSoup(r.text, 'html5lib')
        self.logger.debug(' '.join(re.split('[	 \n]+', soup.text)).strip())
        i = soup.find_all('td', {'align': 'Center', 'rowspan': re.compile('\d+')})
        """
        i = [
            '<td align="Center" rowspan="2" width="7%">算法分析与设计<br/>周五第1,2节{第13-17周}<br/>刘万平(刘万平)<br/>5教0402<br/><br/>算法分析与设计<br/>周五第1,2节{第9-11周}<br/>刘万平(刘万平)<br/>5教0402</td>',
            '<td align="Center" class="noprint" rowspan="2" width="7%">数字图像处理技术<br/>周六第1,2节{第3-10周}<br/>傅由甲(傅由甲)<br/>4教0207(0208)</td>',
            '<td align="Center" rowspan="2">数据库原理及应用<br/>周一第3,4节{第6-11周}<br/>刘加伶(刘加伶)<br/>4教0303(0305)<br/><br/>大学体育[5]<br/>周一第3,4节{第2-5周}<br/>赵晋忠<br/>操场1</td>',
            '<td align="Center" rowspan="2">操作系统原理及应用<br/>周二第3,4节{第10-11周}<br/>杨宏雨(杨宏雨)<br/>4教0303(0305)<br/><br/>操作系统原理及应用<br/>周二第3,4节{第13-17周}<br/>杨宏雨(杨宏雨)<br/>4教0303(0305)<br/><br/>计算机网络【计算机】<br/>周二第3,4节{第2-9周}<br/>李波<br/>6教0411</td>',
            '<td align="Center" rowspan="2">操作系统原理及应用<br/>周三第3,4节{第17-17周|单周}<br/>杨宏雨(杨宏雨)<br/>4教0303(0305)<br/><br/>数据库原理及应用<br/>周三第3,4节{第6-11周}<br/>刘加伶(刘加伶)<br/>4教0303(0305)</td>',
            '<td align="Center" rowspan="2">操作系统原理及应用<br/>周四第3,4节{第11-11周|单周}<br/>杨宏雨(杨宏雨)<br/>3教0307<br/><br/>操作系统原理及应用<br/>周四第3,4节{第13-17周}<br/>杨宏雨(杨宏雨)<br/>3教0307</td>',
            '<td align="Center" rowspan="2">算法分析与设计<br/>周五第3,4节{第13-17周}<br/>刘万平(刘万平)<br/>4教0313<br/><br/>算法分析与设计<br/>周五第3,4节{第9-11周}<br/>刘万平(刘万平)<br/>4教0313</td>',
            '<td align="Center" class="noprint" rowspan="2">操作系统原理及应用<br/>周六第3,4节{第10-11周}<br/>杨宏雨(杨宏雨)<br/>3教0307<br/><br/>操作系统原理及应用<br/>周六第3,4节{第13-16周}<br/>杨宏雨(杨宏雨)<br/>3教0307</td>',
            '<td align="Center" rowspan="4">经济学原理<br/>周一第5,6,7,8节{第13-20周}<br/>霍灵知<br/>5教0309<br/><br/>数据库原理及应用<br/>周一第5,6节{第2-11周}<br/>刘加伶(刘加伶)<br/>6教0411</td>',
            '<td align="Center" rowspan="2">算法分析与设计<br/>周二第5,6节{第13-17周}<br/>刘万平(刘万平)<br/>5教0402<br/><br/>算法分析与设计<br/>周二第5,6节{第9-11周}<br/>刘万平(刘万平)<br/>5教0402</td>',
            '<td align="Center" rowspan="2">数据库原理及应用<br/>周三第5,6节{第2-11周}<br/>刘加伶(刘加伶)<br/>6教0411</td>',
            '<td align="Center" rowspan="2">计算机网络【计算机】<br/>周四第5,6节{第2-9周}<br/>李波<br/>6教0411</td>',
            '<td align="Center" rowspan="2">管理学概论<br/>周五第5,6节{第2-9周}<br/>崔骅<br/>5教0102</td>',
            '<td align="Center" rowspan="2">操作系统原理及应用<br/>周二第7,8节{第9-11周}<br/>杨宏雨(杨宏雨)<br/>3教0307<br/><br/>操作系统原理及应用<br/>周二第7,8节{第13-17周}<br/>杨宏雨(杨宏雨)<br/>3教0307</td>',
            '<td align="Center" rowspan="2">管理学概论<br/>周三第7,8节{第2-9周}<br/>崔骅<br/>5教0102</td>',
            '<td align="Center" rowspan="2">计算机网络实验【独立实验】<br/>周四第7,8节{第3-10周}<br/>邹航/崔贯勋<br/>4教0304</td>',
            '<td align="Center" rowspan="2">数字图像处理技术<br/>周四第9,10节{第2-9周}<br/>傅由甲(傅由甲)<br/>6教0105</td>',
            '<td align="Center" rowspan="2">数字图像处理技术<br/>周五第9,10节{第2-9周}<br/>傅由甲(傅由甲)<br/>6教0105</td>']
        """
        j = []
        for x in i:
            j.extend(re.sub(r'<td(.*?)>', r'', x).replace('</td>', '').split('<br/><br/>'))
        for x in j:
            this = {
                '课程名': re.sub(r'【(.*?)】', r'', x.split('<br/>')[0]),
                '星期几': re.findall(r'周(.?)第', x)[0],
                '第几节': re.findall(r'第(.?)', x)[0],
                '起始周': re.findall(r'{第(.*?)周', x)[0].split('-')[0],
                '结课周': re.findall(r'{第(.*?)周', x)[0].split('-')[1],
                '单周?': True if '单' in x.split('<br/>')[1] else False,
                '双周?': True if '双' in x.split('<br/>')[1] else False,
                '教师名': re.sub(r'\((.*?)\)', r'', x.split('<br/>')[2]),
                '教室': x.split('<br/>')[3]
            }
            self.logger.info(this)
            self.schedule.extend([this])
            '''拆课 - 我们对连续的两节大课进行拆分'''
            t = re.findall(r'第(.*?)节', x)[0].split(',')
            if len(t) > 2:
                that = dict(this)
                that['第几节'] = t[2]
                self.logger.warning(that)
                self.schedule.extend([that])

    def get_date_start(self):
        pass

    def to_ics(self):
        self.logger.warning('拆分后的课程总数：' + str(len(self.schedule)))
        cal = Calendar()
        cal['version'] = '2.0'
        cal['prodid'] = '-//CQUT//Syllabus//CN'  # *mandatory elements* where the prodid can be changed, see RFC 5445
        self.date_start = date(2017, 8, 28)  # 开学第一周星期一的时间
        # datetime.now()
        # TODO: 从 http://cale.dc.cqut.edu.cn/Index.aspx?term=201x-201x 抓取开学时间
        dict_week = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6}
        # dict_time = {1: relativedelta(hours=8, minutes=20), 3: relativedelta(hours=10, minutes=20),
        #              5: relativedelta(hours=14, minutes=0), 7: relativedelta(hours=16, minutes=0),
        #              9: relativedelta(hours=19, minutes=0)}
        dict_time = {1: time(8, 20), 3: time(10, 20), 5: time(14, 0), 7: time(16, 0), 9: time(19, 0)}

        for i in self.schedule:
            print(i)
            event = Event()
            ev_start_date = self.date_start + relativedelta(weeks=int(i['起始周']) - 1, weekday=dict_week[i['星期几']])
            ev_start_datetime = datetime.combine(ev_start_date, dict_time[int(i['第几节'])])  # 上课时间
            # 我们的课持续一小时四十分钟（中间有十分钟课间时间）
            ev_last_relative_delta = relativedelta(hours=1, minutes=40) \
                if int(i['第几节']) != 9 else relativedelta(hours=1, minutes=35)  # 我们晚上的课要少五分钟课间时间
            ev_end_datetime = ev_start_datetime + ev_last_relative_delta  # 下课时间
            ev_interval = 1 if not i['单周?'] | i['双周?'] else 2  # 如果有单双周的课 那么这些课隔一周上一次
            ev_count = int(i['结课周']) - int(i['起始周']) + 1 \
                if not i['单周?'] | i['双周?'] else (int(i['结课周']) - int(i['起始周'])) // 2 + 1

            # 添加事件
            event.add('uid', str(uuid1()) + '@CQUT')
            event.add('summary', i['课程名'])
            event.add('dtstamp', datetime.now())
            event.add('dtstart', ev_start_datetime)
            event.add('dtend', ev_end_datetime)
            event.add('location', i['教师名'] + '@' + i['教室'])
            event.add('rrule', {'freq': 'weekly', 'interval': ev_interval, 'count': ev_count})
            cal.add_component(event)
        with open('output.ics', 'w+', encoding='utf-8') as file:
            file.write(cal.to_ical().decode('utf-8'.replace('\r\n', '\n').strip()))


if __name__ == '__main__':
    cg = CssGetter()
    cg.get_username_password()
    cg.user_login()
    # cg.get_date_start()
    cg.get_schedule()
    cg.to_ics()
