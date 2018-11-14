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
#浙江省文件
file_db = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_zhejiang_file.txt','a',encoding='utf-8')
file_fail = open(r'/Users/jarek-mac/THU/ipolicy/data_policy_zhejiangfail_file.txt','a',encoding='utf-8')
get_person="zhaorui"
check_person=''
province='浙江省'
source_name='浙江省政府'
aim_name=''
document_type='部门文件'
post_url="http://139.196.165.207:8002/ee_app/push_data/"
def get_one_page(i):
    policy_num = 0
    policy_success_num = 0
    policy_fail_num = 0
    if i==31276:
        end =i+33
    else:
        end=i+44
    #url='http://www.zj.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord='+str(start)+'&endrecord='+str(end)+'&perpage=18'
    url='http://www.zj.gov.cn/module/jslib/jquery/jpage/metasearchdataproxy.jsp?startrecord='+str(i)+'&endrecord='+str(end)+'&perpage=15'
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
              'columnid':'12879',
              'strcolumnid':'12879,12886,13783,13785,13786,13787,12887,13788,13791,13794,13798,14291,14072,14292,13803,12947,13789,14073,14074,14075,14076,13796,13801,14077,14078,14079,14080,14081,14082,14083,14084,14085,14086,14087,14088,14089,14090,14091,14092,12948,13790,13793,13797,13802,13808,14214,14215,14218,14219,14216,14231,14232,14217,12889,13795,13800,13805,14095,14096,13818,13852,14097,14098,14099,12890,13799,14311,14312,14314,14315,13815,14313,14100,14101,13846,14316,14317,13887,14262,14263,14233,14235,14236,14237,14238,14240,12891,13807,14102,14103,13820,13859,14104,14105,14106,14107,14108,14109,14110,14111,14112,14113,14114,13898,12892,13809,14337,13822,14339,13861,14331,14332,14333,14334,14335,14336,14338,14340,14341,14342,14343,14344,14345,14346,14347,31031,31032,13899,12894,13810,13823,13862,13900,13937,12949,13856,13931,13970,14175,14176,32531,13999,12895,13811,14432,14433,14434,14435,13863,13901,14431,14131,13939,12896,13812,13831,13870,13908,13947,12897,13813,13832,13872,13911,13948,12899,13814,13834,13874,13912,13949,14234,14239,14241,17252,12900,13816,14411,14412,14413,13885,13923,13961,12901,13817,14511,14512,14513,14514,13886,13924,13964,12902,13858,13896,13933,13971,12904,13821,14391,14392,13860,14393,14395,13897,13934,14394,14396,13972,12905,13825,13864,13902,13938,12907,13826,14133,14134,14135,14137,13903,13940,14136,14138,13974,12908,13827,13866,13904,13941,13975,12909,13828,13867,13905,13942,14151,13976,12910,13829,13906,32053,13943,14155,14156,14157,14348,14349,14350,14351,14352,14353,14354,14356,14355,14357,14358,13977,14371,14374,14375,12911,13959,14539,14541,13987,14542,14543,14000,14001,14158,14540,14002,12913,13830,13869,13907,13944,13978,12914,13833,14533,14535,14536,13871,13909,14537,14538,13945,13979,12915,13835,13910,13946,13980,12917,13836,14319,14320,13913,13950,13981,12919,13837,13876,13914,13951,13982,12920,13838,14451,14452,14454,14457,13915,13952,14455,14458,13983,14453,14456,12922,13839,14471,14472,14473,14474,13916,13953,12923,13840,14491,14492,13879,14493,13917,13954,14494,14495,13985,12924,13841,13918,13955,12926,13842,13881,14551,13919,13956,12927,13843,13882,13920,13957,12928,13844,13921,13958,12930,13854,14552,14553,14555,13892,14554,14556,13929,13967,13996,12931,13855,13893,13930,13968,12932,13857,13895,13932,13969,13998,14242,14243,14244,12939,13847,13884,14574,13922,14575,13960,14172,13991,12945,13853,13891,14576,13928,13966,12941,13849,14571,14573,13888,14572,13925,13962,13992,12943,13850,13889,13926,13963,13993,12944,13851,13890,13927,13965,13994,17531,17551,17554,17555,17571,17572,17532,17591,17592,17593,17594,17595,28731,28732',
              'unitid':'12879',
              'keyWordCount': '30',
              "vc_field": "vc_name:1,field_50281:1,field_42541:1",
              'vc_name':'',
              'field_50281':'',
              'field_42541':'',
              'webname':'浙江省人民政府'
           }
    try:
        response=requests.post(url,data=formdata,timeout=20)
        response.encoding = 'utf-8'
        response=response.text
        soup = BeautifulSoup(response)
        list_as=soup.findAll('a')
        #print(list_as)
        m = hashlib.md5()
        for list_a in list_as:
            info=[]
            policy_num+=1
            url_content=list_a['href']

            aim_url='http://www.zj.gov.cn'+url_content[7:-2]#url
            #print(aim_url)
            aim_name=list_a.string
            #print(aim_name)
            m.update(aim_url.encode("utf8"))
            # md5 for url
            md5 = m.hexdigest()
            info.append(province)
            info.append(source_name)
            info.append(aim_url)
            info.append(md5)
            print('正在爬取第'+str(policy_num)+'条数据...'+aim_name+' URL:'+aim_url)#title

            info.append(aim_name)
            try:
                aim_content=requests.get(aim_url,headers=header,timeout=5)
                print('scrapy success')
                aim_content.encoding='utf-8'
                aim_content=aim_content.text
                soup1=BeautifulSoup(aim_content)
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
                info.append(str(div_contents))
                info.append(get_person)
                info.append('1')
                info.append(document_type)
                post_info(post_url,info)
                '''
                contents = ''
                tablecontent = ''
                linkcontent=''
                for div_content in div_contents:
                    tables = div_content.findAll('table')
                    if len(tables) > 0:
                        for table in tables:
                            for table_string in table.strings:
                                tablecontent += table_string

                    links=div_content.findAll('a')
                    if len(links)>0:
                        for link in links:
                            file_url=link['href']
                            file_name=link.string
                            linkcontent=file_url+' '+file_name
                    for string in div_content.strings:
                        contents += string
                contents = ' table:' + tablecontent + ' link:'+linkcontent+' p:' + contents
                '''
                policy_success_num += 1
            except Exception as err:
                policy_fail_num+=1
                print('scrapy failed in inner')
        file_db.flush()
    except Exception as err:
        print('scrapy failed in outer')
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
    pool.map(main, range(1,31276,45))