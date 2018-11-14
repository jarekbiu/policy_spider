# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup

def spider():
    url='http://www.bjrbj.gov.cn/gwy/publicQuery/msrymd'

    header = {
        'User-Agent': 'Mozilla / 5.0(Macintosh;IntelMacOSX10_13_3) AppleWebKit / 604.5.6(KHTML, likeGecko) Version / 11.0.3Safari / 604.5.6'
    }


    formdata = {'yhid': '2551140',
                'zwdm':'219923114',
                'mslb':'1'}

    try:
        response=requests.post(url,headers=header,data=formdata,timeout=20)

        response.encoding = 'GBK'
        response=response.text

        #soup = BeautifulSoup(response)

        print(response)
    except Exception as err:
        print(err)


#登录的主方法
def login(baseurl,email,password):
    #post需要的表单数据，类型为字典
    login_data = {
            'JSESSIONID': '',
            'username': '',
            'lt': 'true',
            'execution': '',
            '_eventId':'',
            'yhlx':'',
            'password':'',
            'yzm':''
    }
    #设置头信息
    headers_base = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
        'Referer': 'http://www.zhihu.com/',
    }
    #使用seesion登录，这样的好处是可以在接下来的访问中可以保留登录信息
    session = requests.session()
    #登录的URL
    baseurl += "/login/email"
    #requests 的session登录，以post方式，参数分别为url、headers、data
    content = session.post(baseurl, headers = headers_base, data = login_data)
    #成功登录后输出为 {"r":0,#"msg": "\u767b\u9646\u6210\u529f"#}
    print(content.text)
　　#再次使用session以get去访问知乎首页，一定要设置verify = False，否则会访问失败
# s = session.get("http://www.zhihu.com", verify = False)
    print(s.text.encode('utf-8'))
　　#把爬下来的知乎首页写到文本中
    f = open('zhihu.txt', 'w')
    f.write(s.text.encode('utf-8'))

if __name__ == '__main__':
    spider()