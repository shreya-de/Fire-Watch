import requests
import time

def login():    
    url = 'http://192.168.0.1/LoginCheck'
    headers = {
        'Host': '192.168.0.1',
        'Connection': 'keep-alive',
        'Content-Length': '34',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://192.168.0.1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://192.168.0.1/login.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cookie': 'language=en'
        }
    data = {
        'Username':'admin',
        'Password':'YWRtaW4='
        }

    r = requests.post(url, data=data, headers=headers)
    print(r.headers)
    print(r.status_code)
    #print(r.text)
    
def advanced():
    url = 'http://192.168.0.1/advance.asp'
    headers={
        'Host': '192.168.0.1',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://192.168.0.1/index.asp',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cookie': 'language=en; ecos_pw=YWRtaW4=mji:language=en'
        }
    r = requests.get(url,headers=headers)
    print(r.headers)
    print(r.status_code)

def ipt_account():
    url = 'http://192.168.0.1/sys_iptAccount.asp'
    headers = {
        'Host': '192.168.0.1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2787.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://192.168.0.1/advance.asp',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cookie': 'language=en; ecos_pw=YWRtaW4=mji:language=en'
        }
    
    r = requests.get(url,headers=headers)
    print(r.headers)
    print(r.status_code)

def ajax_calls(url,headers,payload,stats):
        r = requests.post(url,headers=headers,data=payload)
        call_response = r.text
        data = call_response.split('\n')
        for node in data:
            machine = node.split(';')
            if(machine[0] != ''):
                stats[machine[0]] = [machine[1],machine[2]]
  
def Fire_Watch(IP_ADDRESSES):
    url = 'http://192.168.0.1/goform/updateIptAccount'
    headers = {
        'Host': '192.168.0.1',
        'Connection': 'keep-alive',
        'Content-Length': '9',
        'Origin': 'http://192.168.0.1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'http://192.168.0.1/sys_iptAccount.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cookie': 'language=en; ecos_pw=YWRtaW4=mji:language=en'
        }
    payload = {'something':''}

    # {'IP':['UPLOAD_RATE','DOWNLOAD_RATE']}
    stats = dict()
    while(True):
        ajax_calls(url,headers,payload,stats)
        for IP_ADDRESS in IP_ADDRESSES:
            data = stats.get(IP_ADDRESS)
            if(data is not None):
                print("IP:",IP_ADDRESS,data)
        print("============")
        time.sleep(2)


#login()
#advanced()
#ipt_account()

IP_ADDRESSES = ['192.168.0.100','192.168.0.101','192.168.0.103']
Fire_Watch(IP_ADDRESSES)
