# -*- coding: UTF-8 -*- 
#中国政府网 公报2000-2017
import requests
import re
import xlwt
import time
import random
import json
from bs4 import BeautifulSoup
import hashlib
import random
from multiprocessing import Pool
from requests.exceptions import RequestException
post_url="http://139.196.165.207:8002/ee_app/push_data/"
def get_page_content():
	sitename='中国政府网'
	province='国务院'
	get_person = "zhaorui"
	policy_num=0
	success_num=0
	list_communiqueUrl=[]
	with open('/Users/jarek-mac/THU/ipolicy/url.json','r') as file:
		url_file=json.load(file)
		v_dic=url_file[0]
		year_dic=v_dic['values']
		for year in year_dic:
			journal_dic=year_dic[year]
			for journal in journal_dic:
				journalInfo_dic=journal_dic[journal]
				c_url='http://www.gov.cn'+journalInfo_dic['gname']
				list_communiqueUrl.append(c_url)

	for i in range(len(list_communiqueUrl)):
		url=list_communiqueUrl[i]
		header = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
		}
		datas=requests.get(url,headers=header)
		datas.encoding = 'utf-8'
		datas=datas.text
		soup = BeautifulSoup(datas)
		div_content=soup.findAll(class_="pubListBox01")
		li_content=div_content[0].findAll('li')
		m = hashlib.md5()

		for li in li_content:
			info=[]
			info.append(province)
			info.append(sitename)
			policy_num+=1
			#url for each policy
			policy_url='http://www.gov.cn'+li.a['href']
			info.append(policy_url)
			m.update(policy_url.encode("utf8"))
			#md5 for url
			md5 = m.hexdigest()
			info.append(md5)
			try:
				post_data={
					'table':'ipolicy',
					'url_md5':md5
				}
				rep = post_info(post_url, data=post_data)
				if rep:
					code = json.loads(rep).get('code', 1)
					number = json.loads(rep).get('number', 0)
					if code == 0 and number >= 0:
						already_exists = True
						print("url already_exists")
						continue
					else:
						already_exists = False
				else:
					already_exists = False

			except Exception as e:
				already_exists = False

			if(already_exists==False):
				title=''
				for string in li.stripped_strings:
					string.replace('<br>','')
					title+=string
				info.append(title)

				policy_info=requests.get(policy_url,headers=header)
				policy_info.encoding = 'utf-8'
				policy_info=policy_info.text
				soup2 = BeautifulSoup(policy_info)

				page_content=soup2.findAll(class_="pages_content")
				content=page_content[0]
				info.append(str(content))
				info.append(get_person)
				status='1'
				success_num+=1
				info.append(status)
				info.append('公告公示')
				post_info(post_url,info)
	print('policy num is '+str(policy_num))
	print('success num is ' + str(success_num))

def post_info(url, info):
    data = {"province":'',"sitename":'',"url":'',"url_md5":'',"title":'',"content":'',"get_person":'',"status":'',"document_type":''}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }
    for one_info ,one_key in zip(info,data.keys()):
        data[one_key] = one_info
    #print(data)
    push_data = {
        'table': 'ipolicy',
        'data': json.dumps(data),
		'override':1
    }
    #print(push_data)
    result = requests.post(url, headers=header, data=push_data)
    print(result.text)

if __name__ == '__main__':
	get_page_content()