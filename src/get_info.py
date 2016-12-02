# coding=utf-8
"""
Created on 2016.11.24
@author: 张晓君
"""

import re

import login_cqut as lc


def get_schedule(opener):  # 获取课程表
    rep = opener.open('http://i.cqut.edu.cn/zfca?yhlx=student&login=0122579031373493728&url=xskbcx.aspx')
    read = rep.read().decode('gb2312')
    # print(read)  # 显示网页内容

    # 行课信息
    xk_data = []
    xk_item = []
    xk_info = re.findall(r'<tr>(.*?)</tr>', read, re.S | re.M)
    for line in xk_info:
        # print(line)
        xk_td_0 = re.findall(r'<td align="Center" rowspan="2" width="7%">(.*?)</td>', line, re.S | re.M)
        xk_td_1 = re.findall(r'<td align="Center" rowspan="2">(.*?)</td>', line, re.S | re.M)
        xk_item.extend(xk_td_0)
        xk_item.extend(xk_td_1)
    for line in xk_item:
        xk_line = re.split(r"<br><br>", line)
        for k in xk_line:
            if k[0] != '<':
                xk_data.append(k)
    # print("xk_data = ")
    # print(xk_data)

    # 调课信息
    tk_data = []
    tk_table = re.findall(
        r'<table class="datelist noprint" cellspacing="0" cellpadding="3" border="0" id="DBGrid" width="100%">(.*?)</table>',
        read, re.S | re.M)
    tk_tr_0 = re.findall(r'<tr>\r\n\t\t<td>(.*?)\r\n\t</tr>', tk_table[0], re.S | re.M)
    tk_tr_1 = re.findall(r'<tr class="alt">\r\n\t\t<td>(.*?)\r\n\t</tr>', tk_table[0], re.S | re.M)
    tk_data.extend(tk_tr_0)
    tk_data.extend(tk_tr_1)
    # print("tk_data = ")
    # print(tk_data)

    # 数据规整
    result = []
    for line in xk_data:
        xk_line = re.split(r"<br>", line)
        xk_line[1] = xk_line[1].rstrip('}')
        xk_line_date = xk_line[1].split('{')
        xk_line.append(xk_line[2])
        xk_line[1] = xk_line_date[0]
        xk_line[2] = xk_line_date[1]
        result.append(xk_line)

    for line in tk_data:
        tk_line = re.split(r"</td><td>", line)

    return result


def main():
    opener = lc.LoginCQUTCookie().login()
    class_table = get_schedule(opener=opener)
    print(class_table)
    # print(len(class_table))


def test():
    xk_data = [
        '大学物理学【Ⅱ（2）】<br>周一第1,2节{第1-10周}<br>韦建卫<br>1教0516',
        'Linux基础与应用<br>周二第1,2节{第1-10周}<br>周敏<br>4教0209',
        '大学英语【III】<br>周三第1,2节{第4-18周|双周}<br>杜云飞<br>4教0402',
        'Linux基础与应用<br>周五第1,2节{第1-10周}<br>周敏<br>4教0209',
        '中国近现代史纲要<br>周一第3,4节{第1-10周}<br>柯芳<br>3教0409',
        '汇编语言程序设计<br>周二第3,4节{第8-10周}<br>刘小洋(刘小洋)<br>3教0406',
        '汇编语言程序设计<br>周二第3,4节{第12-16周}<br>刘小洋(刘小洋)<br>3教0406',
        '大学物理学【Ⅱ（2）】<br>周三第3,4节{第1-10周}<br>韦建卫<br>1教0516',
        '大学英语【III】<br>周四第3,4节{第13-18周}<br>杜云飞<br>1教0706',
        '大学英语【III】<br>周四第3,4节{第2-10周}<br>杜云飞<br>1教0706',
        '大学物理学【Ⅱ（2）】<br>周五第3,4节{第1-4周}<br>韦建卫<br>1教0516',
        '线性代数【理工】<br>周二第5,6节{第12-13周}<br>唐朝君<br>5教0306',
        '线性代数【理工】<br>周二第5,6节{第1-10周}<br>唐朝君<br>5教0306',
        '汇编语言程序设计<br>周三第5,6节{第8-10周}<br>刘小洋(刘小洋)<br>3教0406',
        '汇编语言程序设计<br>周三第5,6节{第12-16周}<br>刘小洋(刘小洋)<br>3教0406',
        '中国近现代史纲要<br>周三第5,6节{第1-5周}<br>柯芳<br>3教0409',
        '大学体育【网球】<br>周四第5,6节{第1-17周}<br>胡洪波<br>操场',
        '线性代数【理工】<br>周五第5,6节{第1-1周|单周}<br>唐朝君<br>5教0306',
        '线性代数【理工】<br>周五第5,6节{第12-13周}<br>唐朝君<br>5教0306',
        '线性代数【理工】<br>周五第5,6节{第3-10周}<br>唐朝君<br>5教0306',
        '汇编语言程序设计<br>周二第7,8节{第10-10周|双周}<br>刘小洋(刘小洋)<br>第1实验楼B403-A',
        '汇编语言程序设计<br>周二第7,8节{第12-16周}<br>刘小洋(刘小洋)<br>第1实验楼B403-A',
        '汇编语言程序设计<br>周三第7,8节{第10-10周|双周}<br>刘小洋(刘小洋)<br>第1实验楼B403-A',
        '汇编语言程序设计<br>周三第7,8节{第12-16周}<br>刘小洋(刘小洋)<br>第1实验楼B403-A',
        '日语入门<br>周二第9,10节{第9-9周|单周}<br>张伶俐<br>1教0406',
        '日语入门<br>周二第9,10节{第6-8周}<br>张伶俐<br>1教0406',
        '日语入门<br>周二第9,10节{第1-4周}<br>张伶俐<br>1教0406',
        '日语入门<br>周四第9,10节{第1-8周}<br>张伶俐<br>1教0410']
    tk_data = [
        '调0097</td><td>日语入门</td><td>周2第9节连续2节{第5-5周}/1教0406/张伶俐</td><td>周2第9节连续2节{第9-9周单周}/1教0406/张伶俐</td><td>2016-09-23-15-26</td>',
        '换0003</td><td>汇编语言程序设计</td><td>周2第7节连续2节{第12-16周}/4教0312/刘小洋</td><td>周2第7节连续2节{第12-16周}/第1实验楼B403-A/刘小洋</td><td>2016-08-26-16-06</td>',
        '换0005</td><td>汇编语言程序设计</td><td>周3第7节连续2节{第12-16周}/4教0312/刘小洋</td><td>周3第7节连续2节{第12-16周}/第1实验楼B403-A/刘小洋</td><td>2016-08-26-16-17</td>',
        '停0077</td><td>大学英语【III】</td><td>周4第3节连续2节{第12-12周}/1教0706/杜云飞</td><td>&nbsp;</td><td>2016-11-16-10-48</td>',
        '换0002</td><td>汇编语言程序设计</td><td>周2第7节连续2节{第10-10周双周}/4教0312/刘小洋</td><td>周2第7节连续2节{第10-10周双周}/第1实验楼B403-A/刘小洋</td><td>2016-08-26-16-05</td>',
        '换0004</td><td>汇编语言程序设计</td><td>周3第7节连续2节{第10-10周双周}/4教0312/刘小洋</td><td>周3第7节连续2节{第10-10周双周}/第1实验楼B403-A/刘小洋</td><td>2016-08-26-16-16</td>',
        '停0009</td><td>线性代数【理工】</td><td>周5第5节连续2节{第2-2周}/5教0306/唐朝君</td><td>&nbsp;</td><td>2016-09-08-14-57</td>']

    for line in xk_data:
        xk_line = re.split(r"<br>", line)
        xk_line[1] = xk_line[1].rstrip('}')
        xk_line_date = xk_line[1].split('{')
        xk_line.append(xk_line[2])
        xk_line[1] = xk_line_date[0]
        xk_line[2] = xk_line_date[1]
        print(xk_line)

    for line in tk_data:
        tk_line = re.split(r"</td><td>", line)
        print(tk_line)


if __name__ == '__main__':
    # main()
    test()
