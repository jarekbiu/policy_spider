# -*- coding: UTF-8 -*-
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib

file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_江西_public.txt', 'a', encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_江西_publicfail.txt', 'a', encoding='utf-8')
get_person = "赵睿"
check_person = ''
source_name = '江西省政府'
policy_num = 0
policy_success_num = 0
policy_fail_num = 0
row = ['null', 'null', 'null', 'null', 'null'
    , 'null', 'null', 'null', 'null', 'null'
    , 'null', 'null', 'null', 'null', 'null'
    , 'null', 'null', 'null', 'null', 'null'
    , 'null', 'null', 'null', 'null', 'null'
    , 'null', 'null', 'null', 'null', 'null'
    , 'null', 'null', 'null', 'null', 'null'
    , 'null', 'null']
row[6] = get_person
row[7] = check_person
row[2] = source_name

#4400
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}
#江西省公报
mainUrl='http://www.jxgb.gov.cn'
datas = requests.get(mainUrl,timeout=20)
datas.encoding = 'gb2312'
datas = datas.text
soup = BeautifulSoup(datas)

journal_lists=[]
m = hashlib.md5()
options=soup.find_all('option')
options=options[2:]
for option in options:
    journal_lists.append(option.string)

url='http://www.jxgb.gov.cn/searchqk.asp'
for journal in journal_lists:
    try:
        data={'classid':journal}
        datas = requests.post(url,data,timeout=20)
        datas.encoding = 'gb2312'
        datas = datas.text
        soup1 = BeautifulSoup(datas)
        li_contents=soup1.find_all('li')
        row[12]=journal
        for li_content in li_contents:
            try:
                policy_num+=1
                temp_url=li_content.a['href']
                temp_url='http://www.jxgb.gov.cn'+temp_url[1:]
                print('正在抓取第'+str(policy_num)+'条数据... '+str(journal)+' URL： '+temp_url)
                row[0]=temp_url
                m.update(temp_url.encode("utf8"))
                # md5 for url
                md5 = m.hexdigest()
                row[1] = md5

                contents = requests.get(temp_url,timeout=20)
                contents.encoding = 'gb2312'
                contents = contents.text
                soup2 = BeautifulSoup(contents)
                titletag=soup2.find('title')
                title=titletag.string
                row[9]=title
                infos=''
                info=soup2.find(class_='c')
                for string in info.stripped_strings:
                    infos+=string
                row[10]=infos
                print('success')
                policy_success_num+=1
                for i in range(37):
                    file_db.write(row[i])
                    file_db.write('$policy$')
                file_db.write('\n')
            except Exception as err:
                policy_fail_num+=1
                print('fail one content')
        file_db.flush()
    except Exception as err:
        print('fail on journal')

print("一共访问" + str(policy_num) + '条数据')
print('成功' + str(policy_success_num) + '条')
print('失败' + str(policy_fail_num) + '条')