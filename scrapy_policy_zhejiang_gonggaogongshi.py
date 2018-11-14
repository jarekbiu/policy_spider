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
#浙江省公告公示
file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_zhejiang_gonggao.txt','a',encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_zhejiangfail_gonggao.txt','a',encoding='utf-8')
get_person="zhaorui"
check_person=''
province='浙江省'
source_name='浙江省政府'
aim_name=''
document_type='公报公示'


post_url="http://139.196.165.207:8002/ee_app/push_data/"
#url='http://www.zj.gov.cn/col/col818/index.html'
def get_one_page(i):
    policy_num=0
    policy_success_num=0
    policy_fail_num=0
#for i in range(145154):
    start=54*i+1
    if start==145153:
        end =start+13
    else:
        end=start+53
    url='http://www.zj.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord='+str(start)+'&endrecord='+str(end)+'&perpage=18'
    row=['null','null','null','null','null'
        ,'null','null','null','null','null'
        ,'null','null','null','null','null'
        ,'null','null','null','null','null'
        ,'null','null','null','null','null'
        ,'null','null','null','null','null'
        ,'null','null','null','null','null'
        ,'null','null']
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
    }
    formdata={'appid':'1',
              'webid':'1',
              'path':'/',
              'columnid':'818',
              'sourceContentType':'1',
              'unitid':'10630',
              'webname':'浙江省人民政府',
              'permissiontype':'0'
           }
    try:
        response=requests.post(url,data=formdata,timeout=20)

        response.encoding = 'utf-8'
        response=response.text
        soup = BeautifulSoup(response)
        spans=soup.findAll('span')
        m = hashlib.md5()
        for span in spans:
            info=[]
            policy_num+=1
            url_content=span.a['href']
            aim_url=url_content[2:-2]#url
            aim_name=span.a.string
            m.update(aim_url.encode("utf8"))
            # md5 for url
            md5 = m.hexdigest()
            info.append(province)
            info.append(source_name)
            info.append(aim_url)
            info.append(md5)
            info.append(aim_name)
            row[1] = md5
            row[0]=aim_url
            print('正在爬取第'+str(policy_num)+'条数据...'+aim_name+' URL:'+aim_url)#title

            row[9]=aim_name
            try:
                aim_content=requests.get(aim_url,headers=header,timeout=5)
                print('scrapy success')
                aim_content.encoding='utf-8'
                aim_content=aim_content.text
                soup1=BeautifulSoup(aim_content)
                #trs=soup1.findAll('td',class_='bt_content')

                #keywords
                meta_keywords=soup1.find(attrs={"name":"Keywords"})['content']
                row[24]=meta_keywords
                info.append(meta_keywords)
                #maketime
                meta_Maketime = soup1.find(attrs={"name": "Maketime"})['content']
                row[13]=meta_Maketime
                info.append(meta_Maketime)
                #category
                meta_category = soup1.find(attrs={"name": "category"})['content']
                row[26]=meta_category
                info.append(meta_category)
                #pubDate
                meta_pubDate = soup1.find(attrs={"name": "pubDate"})['content']
                row[15]=meta_pubDate
                info.append(meta_pubDate)
                #source
                meta_source = soup1.find(attrs={"name": "source"})['content']
                row[27]=meta_source
                #location
                #meta_location = soup1.find(attrs={"name": "location"})['content']
                #department
                #meta_department = soup1.find(attrs={"name": "department"})['content']
                #guid
                meta_guid = soup1.find(attrs={"name": "guid"})['content']
                row[12]=meta_guid
                #print(meta_guid)

                div_contents = soup1.findAll(id='zoom')
                #contents=''
                info.append(str(div_contents))
                info.append(get_person)
                info.append('1')
                info.append(document_type)
                post_info(post_url,info)
                policy_success_num += 1
            except Exception as err:
                policy_fail_num+=1
                print('scrapy failed')

    except Exception as err:
        print('scrapy failed')
    print("一共访问"+str(policy_num)+'条数据')
    print('成功'+str(policy_success_num)+'条')
    print('失败'+str(policy_fail_num)+'条')


def main(i):
    get_one_page(i)

def post_info(url, info):
    data = {"province":'',"sitename":'',"url":'',"url_md5":'',"title":'',"keywords":'',"written_date":'',"category":'',"release_date":'',"category":'',"release_date":'',"content":'',"get_person":'',"status":'',"document_type":''}
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
    pool = Pool(2)
    pool.map(main, range(2500,145154))