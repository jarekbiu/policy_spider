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
get_person="zhaorui"
province='浙江省'
source_name='浙江省政府'
post_url="http://139.196.165.207:8002/ee_app/push_data/"
document_type='政府公报'
def get_one_page():
    policy_num=0
    policy_success_num=0
    policy_fail_num=0

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
            gongbaoUrl='http://www.zj.gov.cn'+option['value']
            #print(gongbaoUrl)
            try:
                datas=requests.get(gongbaoUrl,header,timeout=5)
                datas.encoding='utf-8'
                datas=datas.text
                soup1=BeautifulSoup(datas)
                gongbao_as=soup1.find_all(class_='bt_link')
                gongbao_as=gongbao_as[4:]
                gongbao_source = soup1.find('title')
                for gongbao_a in gongbao_as:
                    info = []
                    info.append(province)
                    info.append(source_name)
                    policy_num+=1
                    print('正在抓取第'+str(policy_num)+'条数据...')
                    gongbao_content_url=gongbao_a['href']
                    #print(gongbao_content_url)
                    if gongbao_content_url[0:4]!='http':
                        gongbao_content_url='http://www.zj.gov.cn'+gongbao_content_url
                    gongbao_title=gongbao_a['title']
                    info.append(gongbao_content_url)
                    m.update(gongbao_content_url.encode("utf8"))
                    # md5 for url
                    md5 = m.hexdigest()
                    info.append(md5)
                    info.append(gongbao_source.string)#title
                    info.append(gongbao_content_url)#公报内容是一个链接
                    info.append(get_person)
                    info.append('1')
                    info.append(document_type)
                    post_info(post_url,info)
                    policy_success_num+=1
            except Exception as err:
                print('scrapy fail in option1')
                policy_fail_num+=1
        for option in option2:
            gongbaoUrl='http://www.zj.gov.cn'+option['value']#每一期
            #m.update(gongbaoUrl.encode("utf8"))
            try:
                datas=requests.get(gongbaoUrl,header,timeout=5)
                datas.encoding='utf-8'
                datas=datas.text
                soup3=BeautifulSoup(datas)
                gongbao_as=soup3.select('a')
                gongbao_source=soup3.find('title')
                gongbao_as=gongbao_as[4:-1]#公告每一条
                for gongbao_a in gongbao_as:
                    info = []
                    info.append(province)
                    info.append(source_name)
                    policy_num+=1
                    print('正在抓取第'+str(policy_num)+'条数据...')
                    gongbao_content_url=gongbao_a['href']
                    if gongbao_content_url[0:4] != 'http':
                        gongbao_content_url='http://www.zj.gov.cn'+gongbao_content_url
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
                    policy_success_num+=1
                    gongbao_title = gongbao_a['title']
                    info.append(gongbao_title)
                    info.append(str(div_contents))
                    info.append(get_person)
                    info.append('1')
                    post_info(post_url, info)
            except Exception as err:
                print('scrapy fail in option2')
                policy_fail_num+=1
    except Exception as err:
        print('scrapy fail in first level')


def main(i):
    get_one_page(i)

def post_info(url, info):
    data = {"province":'',"sitename":'',"url":'',"url_md5":'',"title":'',"content":'',"get_person":'',"status":'',"document_type":''}
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

if __name__ == '__main__':
    get_one_page()

