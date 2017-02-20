# -*- coding: utf-8 -*-
"""
Created on 2016.11.24
@author: 张晓君
"""

import re
from uuid import uuid1
from icalendar import Calendar, Event
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import get_info as gi
import login_cqut as lc


def display(cal):
    return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()


def get_ics(schedule):
    cal = Calendar()
    cal['version'] = '2.0'
    cal['prodid'] = '-//CQUT//Syllabus//CN'  # *mandatory elements* where the prodid can be changed, see RFC 5445
    start_monday = date(2017, 2, 20)  # 开学第一周星期一的时间 TODO: 从 http://cale.dc.cqut.edu.cn/Index.aspx?term=2016-2017 抓取开学时间
    dict_week = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6}
    dict_day = {1: relativedelta(hours=8, minutes=20), 3: relativedelta(hours=10, minutes=20),
                5: relativedelta(hours=14, minutes=0), 7: relativedelta(hours=16, minutes=0),
                9: relativedelta(hours=19, minutes=0)}
    for line in schedule:
        event = Event()
        print(line)
        # line should be like this: ['汇编语言程序设计', '周三第7,8节', '第10-10周|双周', '第1实验楼B403-A', '刘小洋(刘小洋)']

        info_day = re.findall(r'周(.*?)第(\d+),(\d+)节', line[1], re.S | re.M)
        info_day = info_day[0]
        print(info_day)
        # info_day should be like this: ('三', '7', '8')

        info_week = re.findall(r'第(\d+)-(\d+)周', line[2], re.S | re.M)
        info_week = info_week[0]
        print(info_week)
        # info_week should be like this: ('10', '10')

        dtstart_date = start_monday + relativedelta(weeks=(int(info_week[0]) - 1)) + relativedelta(
            days=int(dict_week[info_day[0]]))
        dtstart_datetime = datetime.combine(dtstart_date, datetime.min.time())
        dtstart = dtstart_datetime + dict_day[int(info_day[1])]
        dtend = dtstart + relativedelta(hours=1, minutes=40)
        # 我们的课持续一小时四十分钟（中间有十分钟课间时间）
        if int(info_day[1]) == 9:
            dtend = dtend - relativedelta(minutes=5)
        # 我们晚上的课要少五分钟课间时间

        event.add('uid', str(uuid1()) + '@CQUT')
        event.add('summary', line[0])
        event.add('dtstamp', datetime.now())
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)

        if line[2].find('|') == -1:
            interval = 1
            count = int(info_week[1]) - int(info_week[0]) + 1
        else:
            interval = 2
            count = int(info_week[1]) - int(info_week[0]) / 2 + 1
        # 如果有单双周的课 那么这些课隔一周上一次

        event.add('rrule',
                  {'freq': 'weekly', 'interval': interval,
                   'count': count})
        # 设定重复次数

        event.add('location', line[3])
        # 设定重复地点

        cal.add_component(event)
    return cal


def main():
    print("正在获取课程表...")
    schedule = gi.get_schedule(opener=lc.LoginCQUTCookie().login())
    """
    schedule should be like this:
                [['大学物理学【Ⅱ（2）】', '周一第1,2节', '第1-10周', '1教0516', '韦建卫'],
                ['Linux基础与应用', '周二第1,2节', '第1-10周', '4教0209', '周敏'],
                ['大学英语【III】', '周三第1,2节', '第4-18周|双周', '4教0402', '杜云飞'],
                ['Linux基础与应用', '周五第1,2节', '第1-10周', '4教0209', '周敏'],
                ['中国近现代史纲要', '周一第3,4节', '第1-10周', '3教0409', '柯芳'],
                ['汇编语言程序设计', '周二第3,4节', '第8-10周', '3教0406', '刘小洋(刘小洋)'],
                ['汇编语言程序设计', '周二第3,4节', '第12-16周', '3教0406', '刘小洋(刘小洋)'],
                ['大学物理学【Ⅱ（2）】', '周三第3,4节', '第1-10周', '1教0516', '韦建卫'],
                ['大学英语【III】', '周四第3,4节', '第13-18周', '1教0706', '杜云飞'],
                ['大学英语【III】', '周四第3,4节', '第2-10周', '1教0706', '杜云飞'],
                ['大学物理学【Ⅱ（2）】', '周五第3,4节', '第1-4周', '1教0516', '韦建卫'],
                ['线性代数【理工】', '周二第5,6节', '第12-13周', '5教0306', '唐朝君'],
                ['线性代数【理工】', '周二第5,6节', '第1-10周', '5教0306', '唐朝君'],
                ['汇编语言程序设计', '周三第5,6节', '第8-10周', '3教0406', '刘小洋(刘小洋)'],
                ['汇编语言程序设计', '周三第5,6节', '第12-16周', '3教0406', '刘小洋(刘小洋)'],
                ['中国近现代史纲要', '周三第5,6节', '第1-5周', '3教0409', '柯芳'],
                ['大学体育【网球】', '周四第5,6节', '第1-17周', '操场', '胡洪波'],
                ['线性代数【理工】', '周五第5,6节', '第1-1周|单周', '5教0306', '唐朝君'],
                ['线性代数【理工】', '周五第5,6节', '第12-13周', '5教0306', '唐朝君'],
                ['线性代数【理工】', '周五第5,6节', '第3-10周', '5教0306', '唐朝君'],
                ['汇编语言程序设计', '周二第7,8节', '第10-10周|双周', '第1实验楼B403-A', '刘小洋(刘小洋)'],
                ['汇编语言程序设计', '周二第7,8节', '第12-16周', '第1实验楼B403-A', '刘小洋(刘小洋)'],
                ['汇编语言程序设计', '周三第7,8节', '第10-10周|双周', '第1实验楼B403-A', '刘小洋(刘小洋)'],
                ['汇编语言程序设计', '周三第7,8节', '第12-16周', '第1实验楼B403-A', '刘小洋(刘小洋)'],
                ['日语入门', '周二第9,10节', '第9-9周|单周', '1教0406', '张伶俐'],
                ['日语入门', '周二第9,10节', '第6-8周', '1教0406', '张伶俐'],
                ['日语入门', '周二第9,10节', '第1-4周', '1教0406', '张伶俐'],
                ['日语入门', '周四第9,10节', '第1-8周', '1教0410', '张伶俐']]
                """
    print("获取成功!")
    print("\n课表是...")
    for line in schedule:
        print(line)
    print("\n正在生成 ics 文件...")
    ics = get_ics(schedule)
    print(display(ics))
    print("生成成功!")

    file_name = 'output.ics'
    print("\n正在保存到..." + file_name)
    with open(file_name, 'wb') as f:
        f.write(ics.to_ical())
        if f:
            print('保存成功!')
        else:
            print('保存失败!')


if __name__ == '__main__':
    main()
