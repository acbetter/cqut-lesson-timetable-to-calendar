# CQUT Student Schedule To ICS

将重庆理工大学教务网课程导出为 iCalendar 文件（可用于 iCal、Google Calendar 等）

## INSTALLATION

You need to install python 3 first.

```Shell
brew install python3
```

Second, you need install beautifulsoup4 and icalendar by pip (pip3).

```shell
pip install beautifulsoup4
pip install icalendar
```

## USAGE

```shell
cqut.py -u <username> -p <password>
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

