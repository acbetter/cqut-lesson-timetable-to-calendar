# CQUT Student Schedule To ICS

将重庆理工大学教务网课程导出为 iCalendar 文件（可用于 iCal、Google Calendar 等）

![demo](https://i.loli.net/2018/04/27/5ae2e14a9deea.png)

## INSTALLATION

You need to install python 3 first.

```Shell
brew install python3
```

Second, you need install beautifulsoup4 and icalendar by pip (pip3).

```shell
pip/pip3 install beautifulsoup4
pip/pip3 install icalendar
```

## USAGE

使用前需修改 `cqut.py` 第 192 行的日期，需要改成开学第一周星期一的日期。

```shell
python3 cqut.py -u <username> -p <password>
```

## DESCRIPTION

```shell
-u, --username    你的学号
-p, --password    你的密码
```

## TODO

- [ ] 从本地配置文件读取账号和密码
- [ ] 从 http://cale.dc.cqut.edu.cn/Index.aspx?term=201x-201x 抓取开学时间
- [ ] 部署到 GAE

# LICENSE 

GPL-3.0

