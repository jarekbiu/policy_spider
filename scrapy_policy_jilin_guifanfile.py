# -*- coding: UTF-8 -*-
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib
from multiprocessing import Pool
#吉林政府公报
file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_jilin_public.txt','a',encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_jilin_publicfail.txt','a',encoding='utf-8')
get_person="zhaorui"
check_person=''
province='吉林'
source_name='吉林省政府'
document_type='政府公报'

post_url="http://139.196.165.207:8002/ee_app/push_data/"
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
def get_one_page(i):
    policy_num = 0
    policy_success_num = 0
    policy_fail_num = 0
    if i==0:
        url='http://xxgk.jl.gov.cn/gfxwj/index.html'
    else:
        url='http://xxgk.jl.gov.cn/gfxwj/index_'+str(i)+'.html'
    try:
        response=requests.get(url,header,timeout=20)
        response.encoding = 'utf-8'
        response=response.text
        soup = BeautifulSoup(response)

        #print(url)

        a_tags=soup.find_all(target="_blank")
        m = hashlib.md5()

        #print('2')

        for a_tag in a_tags:
            info=[]
            a_url=a_tag['href']

            a_url='http://xxgk.jl.gov.cn'+a_url[2:]

            a_title=a_tag.string
            info.append(province)
            info.append(source_name)
            info.append(a_url)
            m.update(a_url.encode("utf8"))
            # md5 for url
            md5 = m.hexdigest()
            info.append(md5)
            info.append(a_title)
            policy_num += 1
            print('正在抓取第' + str(policy_num) + '条数据...' + a_title + ' URL:' + a_url)
            '''
            #next_table=a_tag.find_next('div')
            #td_tags=next_table.findAll('td')
            #td_index=0
            #for td_tag in td_tags:
            #    temp_content=''
            #    for string in td_tag.stripped_strings:
            #        temp_content+=string
            #    info.append(temp_content)
        
                if td_index==0:
                    index_number=temp_content
                    info.append(index_number)
                if td_index==1:
                    category=temp_content
                    info.append(category)
                if td_index==2:
                    written_date=temp_content
                    info.append(written_date)
                if td_index==3:
                    department=temp_content
                    info.append(department)
                if td_index==4:
                    row[9]=temp_content
                if td_index==5:
                    row[24]=temp_content
                    keywords=temp_content
                    info.append(keywords)
                if td_index==6:
                    row[23]=temp_content
                    registration_number=temp_content
                    info.append(registration_number)
                td_index+=1
            '''

            try:
                datas = requests.get(a_url, header, timeout=20)
                datas.encoding = 'utf-8'
                datas = datas.text
                soup1 = BeautifulSoup(datas)

                td_tags = soup1.findAll(class_='zly_xxgk_20170120l2')
                for td_tag in td_tags:
                    info.append(td_tag.string)
                #print(td_tags)

                table_contents=soup1.find(id='zoom')
                info.append(str(table_contents))
                info.append(get_person)
                info.append('1')
                post_info(post_url, info)
                print('scrapy success')
            except Exception as err:
                print('scapy fail in inner')
    except Exception as err:
        print('scrapy fail in outer')


def post_info(url, info):
    data = {"province":'',"sitename":'',"url":'',"url_md5":'',"title":'',"index_number":'',"document_type":'',"department":'',"written_date":'',"issued_number":'',"release_date":'',"content":'',"get_person":'',"status":''}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }
    for one_info ,one_key in zip(info,data.keys()):
        data[one_key] = one_info
    print(data)
    push_data = {
        'table': 'ipolicy',
        'data': str(data),
        'override':1
    }
    result = requests.post(url, headers=header, data=push_data)
    print(result.text)
def main(i):
    get_one_page(i)


if __name__ == '__main__':
    pool = Pool(2)
    pool.map(main, range(183))

