# -*- coding: UTF-8 -*-
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib
#湖北政府公报
file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_湖北_public.txt','a',encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_湖北_publicfail.txt','a',encoding='utf-8')
get_person="赵睿"
check_person=''
source_name='湖北政府'
policy_num=0
policy_success_num=0
policy_fail_num=0

row=['null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null']
row[6]=get_person
row[7]=check_person
row[2]=source_name
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
    }
#url='http://gkml.hubei.gov.cn/auto5472/auto5473/?id=2130'
url='http://gkml.hubei.gov.cn/auto5472/auto5473/2038/2109/2135/2136/'

response=requests.get(url,header,timeout=20)
response.encoding = 'utf-8'
response=response.text
soup = BeautifulSoup(response)

tr_tags=soup.find_all('tr')
tr_tags=tr_tags[1:]
for tr_tag in tr_tags:
    a_tag=tr_tag.a
    content_url=a_tag['href']
    content_url='http://gkml.hubei.gov.cn/auto5472/auto5473'+content_url[11:]
    content_title=a_tag['title']
    print(content_url)

    datas = requests.get(content_url, header, timeout=20)
    datas.encoding = 'utf-8'
    datas = datas.text
    soup1 = BeautifulSoup(datas)

    table_content=soup1.find('wzy_sy_1')
    li_contents=table_content.find_all('li')
    for li in li_contents:
        index=0
        string_list=[]
        for string in li.strings:
            string_list.append(string)
        if(string_list[0]=='索 引 号：'):
            row[22]=string_list[1]
        if (string_list[0] == '分&nbsp;&nbsp;&nbsp; 类：'):
            row[26] = string_list[1]
        if (string_list[0] == '发布机构：'):
            row[11] = string_list[1]
        if (string_list[0] == '发文日期：'):
            row[15] = string_list[1]
        if (string_list[0] == '名&nbsp;&nbsp;&nbsp; 称：'):
            row[9] = string_list[1]
        if (string_list[0] == '文&nbsp;&nbsp;&nbsp; 号：'):
            row[12] = string_list[1]
        if (string_list[0] == '主 题 词：'):
            row[15] = string_list[1]
    content_info=soup1.find(class_='normal_block_border channel_block')
    print(content_info)

print("一共访问"+str(policy_num)+'条数据')
print('成功'+str(policy_success_num)+'条')
print('失败'+str(policy_fail_num)+'条')






