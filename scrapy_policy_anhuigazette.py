# -*- coding: UTF-8 -*-
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib
#安徽省公报
file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_安徽_public.txt','a',encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_安徽_publicfail.txt','a',encoding='utf-8')
get_person="zhaorui"
check_person=''
source_name='安徽省政府'
policy_num=0
policy_success_num=0
policy_fail_num=0
document_type='公报公示'
post_url="http://139.196.165.207:8002/ee_app/push_data/"
row=['null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null','null','null','null'
    ,'null','null']
province='安徽'
sitename='安徽政府网'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
    }

def has_title(tag):
    return tag.has_attr('title')
m = hashlib.md5()
def get_page():
    for year in range(2015,2018):
        for halfmonth in range(1,25):
            url='http://www.ah.gov.cn/tmp/Nav_zfgblm.shtml?n='+str(year)+'&q='+str(halfmonth)#每一期
            response=requests.get(url)
            print(url)
            response.encoding = 'gb2312'
            response=response.text
            soup = BeautifulSoup(response)

            a_tags=soup.find_all(class_="newslink")
            m = hashlib.md5()
            try:
                for a_tag in a_tags:
                    visited_lists=[]#已经查找过的，确定是需要访问的URL
                    visit_lists=[]#新发现但还没有搜索的URL
                    a_url='http://www.ah.gov.cn'+a_tag['href']#每期期刊的每一个栏目
                    visit_lists.append(a_url)
                    print('searcing...')
                    while len(visit_lists)>0:
                        visit_url=visit_lists[0]
                        visited_lists.append(visit_url)#将URL加到visited中
                        urldata = requests.get(visit_url)
                        urldata.encoding = 'gb2312'
                        urldata = urldata.text
                        soup1 = BeautifulSoup(urldata)

                        temp_a_tag = soup1.find(has_title)
                        temp_url = temp_a_tag.find_next('table')
                        candidate_a = temp_url.find_all('a')
                        for c_a in candidate_a:
                            newUrl = 'http://www.ah.gov.cn' + c_a['href']
                            if newUrl not in visited_lists and newUrl not in visit_lists:
                                visit_lists.append(newUrl)
                        visit_lists.remove(visit_url)
                    visited_lists.remove(a_url)
                    print('scrapying')
                    for visited_url in visited_lists:
                        try:
                            datas = requests.get(visited_url)
                            datas.encoding = 'gb2312'
                            datas = datas.text
                            soup2 = BeautifulSoup(datas)

                            item_as=soup2.find_all(has_title)

                            for item_a in item_as:
                                info = []
                                try:
                                    #policy_num+=1
                                    item_url=item_a['href']#最终页面
                                    row[0] = item_url
                                    info.append(province)
                                    info.append(sitename)
                                    info.append(item_url)
                                    m.update(item_url.encode("gb2312"))
                                    # md5 for url
                                    md5 = m.hexdigest()
                                    row[1] = md5
                                    info.append(md5)
                                    item_name=item_a.string
                                    row[9]=item_name
                                    info.append(item_name)
                                    #print('正在抓取第'+str(policy_num)+'条数据...URL： '+item_url)

                                    doclists = requests.get(item_url)
                                    doclists.encoding = 'gb2312'
                                    doclists = doclists.text
                                    soup2 = BeautifulSoup(doclists)

                                    content=''
                                    div=soup2.find(id="zoom")
                                    info.append(str(div))
                                    info.append(get_person)
                                    status='1'
                                    info.append(status)
                                    info.append(document_type)
                                    print('scrapy success')
                                except Exception as err:
                                    print('fail in one content')
                                post_info(post_url, info)
                        except Exception as err:
                            print('fail in page chose')
                    file_db.flush()
            except Exception as err:
                print('fail in department')

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
    get_page()





