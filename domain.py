import urllib.request
import json
import urllib.request
from bs4 import BeautifulSoup
import socket
import time
from urllib.error import URLError
from retry import retry
def get_ip():
    #获取当前ip
    url = 'http://www.net.cn/static/customercare/yourip.asp'
    req = urllib.request.Request(url)
    rsp=urllib.request.urlopen(req)
    html=rsp.read().decode('utf-8',"ignore")
    html=BeautifulSoup(html,'html.parser')
    iph2=html.h2
    global ip
    ip=iph2.get_text()
get_ip()
ip_addr = ip
#修改域名
api_url = 'https://api.godaddy.com/v1/domains/你的域名/records'
head = {}
head['Accept'] = 'application/json'
head['Content-Type'] = 'application/json'
#api key
head['Authorization'] = 'sso-key 你的key:你的secret'
records_a = {
"data" : ip_addr,
"name" : "@",
"ttl" : 600,
"type" : 'A',
}
records_NS01 = {
"data" : "ns07.domaincontrol.com",
"name" : "@",
"ttl" : 3600,
"type" : "NS",
}

records_NS02 = {
"data" : "ns08.domaincontrol.com",
"name" : "@",
"ttl" : 3600,
"type" : "NS",
}
put_data = [records_a,records_NS01,records_NS02]
while True:
    try:
        req = urllib.request.Request(api_url,headers = head,data = json.dumps(put_data).encode(),method = "PUT")
        rsp = urllib.request.urlopen(req)
        code = rsp.getcode()
        if code == 200:
            print('成功更改域名解析：'+ip_addr)
            break
        else:
            print('更改失败！')
    except:
        print("错误")
