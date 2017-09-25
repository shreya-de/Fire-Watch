import requests
import time

def ajax_calls(url,headers,payload,stats):
        r = requests.post(url,headers=headers,data=payload)
        call_response = r.text
        data = call_response.split('\n')
        for node in data:
            machine = node.split(';')
            if(machine[0] != ''):
                stats[machine[0]] = [machine[1],machine[2]]
  
def Statistics():
    ##############################################################################################################################
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
        'Cookie': 'ecos_pw=YWRtaW4=cvb:language=en'
        }
    payload = {'something':''}
    # {'IP':['UPLOAD_RATE','DOWNLOAD_RATE']}
    stats = dict()
    down_time=0
    up_time=time.time()
    level=0
    factors=[1,60,3600,86400,2592000,31104000,31104000]
    limits = [60,60,24,30,12,10]
    info = ['sec','min','hour','day','month','year','decade']
    factor = factors[level]
    duration=0
    ##############################################################################################################################

    while(True):
        ajax_calls(url,headers,payload,stats)
        duration = (time.time()-up_time)/factor
        if(duration >= limits[level]):
            level+=1
            factor = factors[level]
            duration = (time.time()-up_time)/factor
        print("\n\t\tUPTIME: ",round(duration,3),info[level])
        print("\t\t------")
        for IP, DATA in stats.items():
            print("IP:",IP,"\tDOWN:",DATA[1],"\tUP:",DATA[0])
        #print("==============")
        time.sleep(2)

Statistics()
