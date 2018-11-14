# -*- coding: UTF-8 -*- 
#中国政府网-文件
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib
from multiprocessing import Pool

policy_num=0
post_url="http://139.196.165.207:8002/ee_app/push_data/"
def get_one_page(url):
    sitename = '中国政府网'
    province = '国务院'
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
    }
    datas=requests.get(url,headers=header)
    datas.encoding = 'utf-8'
    datas=datas.text
    soup = BeautifulSoup(datas)
    div_content=soup.findAll(class_="dataBox")
    tr_content=div_content[0].findAll('tr')
    m = hashlib.md5()
    for i in range(1,len(tr_content)):
        info=[]
        file_info=tr_content[i]
        temp_title=file_info.findAll(class_="info")
        file_url=temp_title[0].a['href']
        info.append(province)
        info.append(sitename)
        info.append(file_url)
        m.update(file_url.encode("utf8"))
        # md5 for url
        policy_url_hash = m.hexdigest()
        info.append(policy_url_hash)
        file_title=temp_title[0].a.string
        info.append(file_title)
        li_content=file_info.findAll("li")
        for li in li_content:
            #policy_num+=1
            list_temp=[]
            for string in li.stripped_strings:
                list_temp.append(string)
            if len(list_temp)>1:
                if list_temp[0]=='索  引 号：':
                    info.append(list_temp[1])
                if list_temp[0]=='主题分类：':
                    info.append(list_temp[1])
                if list_temp[0]=='发文机关：':
                    info.append(list_temp[1])
                if list_temp[0]=='成文日期：':
                    info.append(list_temp[1])
                if list_temp[0]=='发文字号：':
                    info.append(list_temp[1])
                if list_temp[0]=='发布日期：':
                    info.append(list_temp[1])
        flag=False

        try:
            file_content=requests.get(file_url,headers=header)
        except Exception as err:
            flag=True

        if flag==False:
            file_content.encoding='utf-8'
            file_content=file_content.text
            soup1 = BeautifulSoup(file_content)
            fileinfo_td_content=soup1.findAll(class_="b12c")
            info.append(str(fileinfo_td_content))
            get_person="zhaorui"
            info.append(get_person)
            status='1'
            info.append(status)
            info.append('政府文件')

        post_info(post_url,info)
print('policy num is '+str(policy_num))


def post_info(url, info):
    data = {"province":'',"sitename":'',"url":'',"url_md5":'',"title":'',"index_number":'',"category":'',"department":'',"written_date":'',"issued_number":'',"release_date":'',"content":'',"get_person":'',"status":'',"document_type":''}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }
    for one_info ,one_key in zip(info,data.keys()):
        data[one_key] = one_info
    print(data)
    push_data = {
        'table': 'ipolicy',
        'data': str(data),
        'override': 1
    }
    result = requests.post(url, headers=header, data=push_data)
    print(result.text)


def main(i):
    url = 'http://sousuo.gov.cn/list.htm?q=&n=15&p=' + str(i) + '&t=paper&sort=pubtime&childtype=&subchildtype=&pcodeJiguan=&pcodeYear=&pcodeNum=&location=&searchfield=&title=&content=&pcode=&puborg=&timetype=timeqb&mintime=&maxtime='
    get_one_page(url)


if __name__ == '__main__':
    pool = Pool(2)
    pool.map(main, range(321))