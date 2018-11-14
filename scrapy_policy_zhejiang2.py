# -*- coding: UTF-8 -*-
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib
#浙江省政府公报
file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_public.txt','a',encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_publicfail.txt','a',encoding='utf-8')
get_person="zhaorui"
check_person=''
province='浙江省'
source_name='浙江省政府'
get_one_page()：
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
    url='http://www.zj.gov.cn/col/col41314/index.html'
    try:
        response=requests.get(url,header,timeout=20)
        response.encoding = 'utf-8'
        response=response.text
        soup = BeautifulSoup(response)
        options=soup.find_all('option')
        option1=options[1:11]#第一部分 以年份为单位
        option2=options[11:]#第二部分 以期刊为单位
        #print(option1)
        m = hashlib.md5()

        for option in option1:
            info=[]
            info.append(province)
            info.append(source_name)
            gongbaoUrl='http://www.zj.gov.cn'+option['value']
            #m.update(gongbaoUrl.encode("utf8"))
            # md5 for url
            #md5 = m.hexdigest()
            row[1] = md5
            row[0] = gongbaoUrl
            #print(gongbaoUrl)
            try:
                datas=requests.get(gongbaoUrl,header,timeout=5)
                datas.encoding='utf-8'
                datas=datas.text
                soup1=BeautifulSoup(datas)
                gongbao_as=soup1.find_all(class_='bt_link')
                gongbao_as=gongbao_as[4:]
                gongbao_source = soup1.find('title')
                row[12] = gongbao_source.string
                #info.append(gongbao_source.string)#title
                print(row[12])
                for gongbao_a in gongbao_as:
                    policy_num+=1
                    print('正在抓取第'+str(policy_num)+'条数据...')
                    gongbao_content_url=gongbao_a['href']
                    #print(gongbao_content_url)
                    if gongbao_content_url[0:4]!='http':
                        gongbao_content_url='http://www.zj.gov.cn'+gongbao_content_url
                    row[10]=gongbao_content_url
                    gongbao_title=gongbao_a['title']
                    row[9]=gongbao_title
                    info.append(gongbao_content_url)
                    m.update(gongbao_content_url.encode("utf8"))
                    # md5 for url
                    md5 = m.hexdigest()
                    info.append(md5)
                    info.append(gongbao_source.string)#title
                    info.append(gongbao_content_url)#公报内容是一个链接
                    info.append(get_person)
                    info.append('1')
                    policy_success_num+=1
            except Exception as err:
                print('scrapy fail in option1')
                policy_fail_num+=1
        for option in option2:
            info=[]
            gongbaoUrl='http://www.zj.gov.cn'+option['value']#每一期
            info.append(province)
            info.append(source_name)
            #m.update(gongbaoUrl.encode("utf8"))
            try:
                datas=requests.get(gongbaoUrl,header,timeout=5)
                datas.encoding='utf-8'
                datas=datas.text
                soup3=BeautifulSoup(datas)
                gongbao_as=soup3.select('a')
                gongbao_source=soup3.find('title')
                row[12]=gongbao_source.string#title
                #print(row[12])
                gongbao_as=gongbao_as[4:-1]#公告每一条
                content = ''
                for gongbao_a in gongbao_as:
                    policy_num+=1
                    print('正在抓取第'+str(policy_num)+'条数据...')
                    gongbao_content_url=gongbao_a['href']
                    if gongbao_content_url[0:4] != 'http':
                        gongbao_content_url='http://www.zj.gov.cn'+gongbao_content_url
                    row[10] = gongbao_content_url#每条具体内容
                    #print(row[10])
                    m.update(gongbao_content_url.encode("utf8"))
                    # md5 for url
                    md5 = m.hexdigest()
                    info.append(gongbao_content_url)
                    info.append(md5)
                    contents=requests.get(gongbao_content_url,header,timeout=5)
                    contents.encoding = 'utf-8'
                    contents = contents.text
                    soup2 = BeautifulSoup(contents)
                    div_contents=soup2.find_all(id='zoom')
                    #for div_content in div_contents:
                    #    p_contents=div_content.findAll('p')
                    #    for p_content in p_contents:
                    #        for s in p_content.stripped_strings:
                    #            content+=s

                    policy_success_num+=1
                    gongbao_title = gongbao_a['title']
                    info.append(gongbao_title)
                    info.append(str(div_contents))
                    info.append(get_person)
                    info.append('1')
                    #print(gongbao_a['title'])
                    #print(content)
                    #print(gongbao_as)
            except Exception as err:
                print('scrapy fail in option2')
                policy_fail_num+=1
    except Exception as err:
        print('scrapy fail in first level')


def main(i):
    get_one_page(i)

def post_info(url, info):
    data = {"province":'',"sitename":'',"url":'',"url_md5":'',"title":'',"content":'',"get_person":'',"status":''}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }
    for one_info ,one_key in zip(info,data.keys()):
        data[one_key] = one_info
    print(data)
    push_data = {
        'table': 'ipolicy',
        'data': str(data),
        'override':0
    }
    result = requests.post(url, headers=header, data=push_data)
    print(result.text)

if __name__ == '__main__':
    get_one_page()

