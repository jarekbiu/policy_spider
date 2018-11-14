# -*- coding: UTF-8 -*- 
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib
#福建省政府文件

file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_fujian1.txt','a',encoding='utf-8')
get_person="zhaorui"
check_person=''
source_name='福建省人民政府'
policy_num=0

list_url=['http://www.fujian.gov.cn/zc/zxwj/szfwj/'
         ,'http://www.fujian.gov.cn/zc/zxwj/szfbgtwj/'
         ,'http://www.fujian.gov.cn/zc/zxwj/bmwj/'
         ,'http://www.fujian.gov.cn/zc/zxwj/sqswj/']
row=['null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null']

for i in range(1):
	url='http://www.zj.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=163&endrecord=216&perpage=18'
	header = {
	'Accept':'text/javascript, application/javascript, */*',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Content-Length':'159',
	'Content-Type':'application/x-www-form-urlencoded',
	'Cookie':'JSESSIONID=36AE9CA2C4CFFC13F3EC2F9C3F2A9EF1; acw_tc=AQAAAJvcUWxP/QoACWVvpiWUV0FaxrKm; _gscu_2069726388=03276579o6txcd35; _gscs_2069726388=03276579x6usmm35|pv:46; _gscbrs_2069726388=1; SERVERID=67f6e0372c2e2c36c861c4461791451e|1503280331|1503276579',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Host':'www.zj.gov.cn',
	'Origin':'http://www.zj.gov.cn',
	'Referer':'http://www.zj.gov.cn/col/col818/index.html',
	'X-Requested-With':'XMLHttpRequest'
	}
	datas=requests.get(url,headers=header)
	datas.encoding = 'utf-8'
	datas=datas.text
	#print(datas)
	soup = BeautifulSoup(datas)
	#content=soup.findAll()
	print(datas)
	#for divcontent in content:
	#	licontents=divcontent.findAll('li')
		#print(licontents[0])
	#print(content)