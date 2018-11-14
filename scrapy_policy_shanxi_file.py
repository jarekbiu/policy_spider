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
# 陕西省文件
file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_陕西_public.txt', 'a', encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_陕西_publicfail.txt', 'a', encoding='utf-8')
get_person = "zhaorui"
check_person = ''
province='陕西省'
source_name = '陕西省政府'
document_type='政府文件'
post_url="http://139.196.165.207:8002/ee_app/push_data/"

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

def has_title(tag):
    return tag.has_attr('title')

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}
url_lists = ['http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=陕西省人民政府令&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E5%8F%91&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E5%AD%97&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E4%BB%BB%E5%AD%97&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E9%80%9A%E6%8A%A5&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E5%87%BD&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E5%8A%9E%E5%8F%91&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E5%8A%9E%E5%AD%97&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E5%8A%9E%E5%8F%91%E6%98%8E%E7%94%B5&tm_id=69',
             'http://www.shaanxi.gov.cn/info/iList.jsp?node_id=GKszfbgt&file_head=%E9%99%95%E6%94%BF%E5%8A%9E%E5%87%BD&tm_id=69'
             ]
pages_lists=[10,72,18,103,68,54,138,6,14,52]
m = hashlib.md5()
def get_one_page(i):
    policy_num = 0
    policy_success_num = 0
    policy_fail_num = 0
    url=url_lists[i]
    pages=pages_lists[i]
    for page in range(1,pages_lists[i]+1):
        try:
            url=url+'&cur_page='+str(page)
            datas = requests.get(url)
            datas.encoding = 'utf-8'
            datas = datas.text
            soup = BeautifulSoup(datas)

            a_contents = soup.find_all(has_title)
            for a in a_contents:
                info=[]
                policy_num+=1
                a_url='http://www.shaanxi.gov.cn'+a['href']
                row[0] = a_url
                info.append(province)
                info.append(source_name)
                info.append(a_url)
                m.update(a_url.encode("utf8"))
                # md5 for url
                md5 = m.hexdigest()
                row[1] = md5
                info.append(md5)
                try:
                    title=a.string
                    row[9]=title
                    info.append(title)
                    contents = requests.get(a_url)
                    contents.encoding = 'utf-8'
                    contents = contents.text
                    soup1 = BeautifulSoup(contents)
                    print('正在抓取第'+str(policy_num)+'条数据...URL： '+a_url)

                    '''
                    表头部分
                    '''
                    table_content=soup1.find('table')
                    td_contents=table_content.find_all('td')
                    for td in td_contents:
                        if td.string=='索 引 号：':
                            td_value=td.find_next_sibling('td')
                            row[22]=td_value.string
                            index_number=td_value.string
                            info.append(index_number)
                        if td.string == '发文字号：':
                            td_value = td.find_next_sibling('td')
                            row[12] = td_value.string
                            issued_number=td_value.string
                            info.append(issued_number)
                        if td.string == '发布机构：':
                            td_value = td.find_next_sibling('td')
                            row[11] = td_value.string
                            department=td_value.string
                            info.append(department)
                        if td.string == '公文时效：':
                            td_value = td.find_next_sibling('td')
                            row[17] = td_value.string
                            timeliness=td_value.string
                            info.append(timeliness)
                        if td.string == '名　　称：':
                            td_value = td.find_next_sibling('td')
                            row[24] = td_value.string
                            #print(row[6])
                        if td.string == '主题分类：':
                            td_value = td.find_next_sibling('td')
                            row[26] = td_value.string
                            category=td_value.string
                            info.append(category)
                        if td.string == '发布日期：':
                            td_value = td.find_next_sibling('td')
                            row[15] = td_value.string
                            release_date=td_value.string
                            info.append(release_date)

                    p_tags=soup1.find_all('p')
                    #p_contents=''
                    #for p_tag in p_tags:
                    #    for string in p_tag.stripped_strings:
                    #        p_contents+=string
                    #print(p_contents)
                    #row[10]=p_contents
                    info.append(str(p_tags))
                    status='1'
                    info.append(get_person)
                    info.append(status)
                    info.append(document_type)
                    print('success')
                except Exception as err:
                    print('fail in policy item')
                    policy_fail_num+=1
                post_info(post_url,info)
        except Exception as err:
            print('fail in department')
            policy_fail_num+=pages_lists[i]

    print("一共访问" + str(policy_num) + '条数据')
    print('成功' + str(policy_success_num) + '条')
    print('失败' + str(policy_fail_num) + '条')

def main(i):
    get_one_page(i)

def post_info(url, info):
    data = {"province":'',"sitename":'',"url":'',"url_md5":'',"title":'',"index_number":'',"issued_number":'',"department":'',"timeliness":'',"category":'',"release_date":'',"content":'',"get_person":'',"status":'',"document_type":''}
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
    pool = Pool(2)
    pool.map(main, range(len(url_lists)))

