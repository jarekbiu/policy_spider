# -*- coding: UTF-8 -*-
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib
#内蒙古政府公报
file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_neimenggu_public.txt','a',encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_neimenggu_publicfail.txt','a',encoding='utf-8')
get_person="zhaorui"
check_person=''
province="内蒙古"
source_name='内蒙古政府'
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

def get_page_content():
    policy_num = 0
    policy_success_num = 0
    policy_fail_num = 0
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
        }
    url='http://www.nmgzfgb.gov.cn/information/nmgzb22/msg6730113575.html'

    response=requests.get(url,header,timeout=20)
    response.encoding = 'gbk'
    response=response.text
    soup = BeautifulSoup(response)
    div_tags=soup.find(class_="zbtree")
    a_tags=div_tags.findAll('a')
    list_urls=[]
    for a_tag in a_tags:
        #print(a_tag['href'])
        list_urls.append('http://www.nmgzfgb.gov.cn'+a_tag['href'])
        #print('http://www.nmgzfgb.gov.cn'+a_tag['href'])
    #print('1')
    m = hashlib.md5()
    for list_url in list_urls:
        try:
            datas = requests.get(list_url, header, timeout=20)
            datas.encoding = 'gbk'
            datas = datas.text
            soup1 = BeautifulSoup(datas)
            a_contents=soup1.find_all(class_='zblink')#找到每一期中具体的每个条目的URL
            title=soup1.find('title')#期刊标题
            #print(title.string)
            #print('2')
            for  a_content in a_contents:
                info=[]
                #print(a_content['href'])
                policy_num+=1

                content_url='http://www.nmgzfgb.gov.cn'+a_content['href']
                #print(content_url)#每一条的URL
                row[0]=content_url
                info.append(province)
                info.append(source_name)
                info.append(content_url)
                aim_name=a_content.string
                row[9]=aim_name

                m.update(content_url.encode("utf8"))
                # md5 for url
                md5 = m.hexdigest()
                row[1] = md5
                info.append(md5)
                info.append(aim_name)
                #print(a_content.string)#每一条的标题
                #print('3')
                print('正在抓取第' + str(policy_num) + '条数据...' + aim_name + ' URL:' + content_url)
                try:
                    contents = requests.get(content_url, header, timeout=20)
                    contents.encoding = 'gbk'
                    contents = contents.text
                    soup2 = BeautifulSoup(contents)
                    #print('4')
                    # keywords
                    meta_keywords = soup2.find(attrs={"name": "Keywords"})['content']
                    row[24] = meta_keywords
                    info.append(meta_keywords)
                    p_contents=soup2.find_all('p')
                    info.append(str(p_contents))
                    #gongbao_content=''
                    #for p_content in p_contents:
                    #    for string in p_content.stripped_strings:
                    #        gongbao_content+=string
                    #row[10]=gongbao_content
                    #row[3]='1'

                    #for i in range(37):
                    #    file_db.write(row[i])
                    #    file_db.write('$policy$')
                    #file_db.write('\n')
                    print('scrapy success')
                    info.append(get_person)
                    status='1'
                    info.append(status)
                    info.append(document_type)
                except Exception as err:
                    print('scrapy fail in inner')
                post_info(post_url,info)
            #file_db.flush()
        except Exception as err:
            print('scrapy fail in outer')


def post_info(url, info):
    data = {"province":'',"sitename":'',"url":'',"url_md5":'',"title":'',"keywords":'',"content":'',"get_person":'',"status":'',"document_type":''}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }
    for one_info ,one_key in zip(info,data.keys()):
        data[one_key] = one_info
    #print(data)
    push_data = {
        'table': 'ipolicy',
        'data': str(data),
        'override':1
    }
    result = requests.post(url, headers=header, data=push_data)
    print(result.text)



if __name__ == '__main__':
    get_page_content()






