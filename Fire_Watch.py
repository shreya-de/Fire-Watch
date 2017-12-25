from os import system
import requests
import time
import subprocess

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
    print(r.status_code,'\n')
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
        'Cookie': 'language=en; ecos_pw=YWRtaW4=tgb:language=en'
        }
    r = requests.get(url,headers=headers)
    print(r.headers)
    print(r.status_code,'\n')

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
        'Cookie': 'language=en; ecos_pw=YWRtaW4=tgb:language=en'
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
	# SYSTEM CONFIGS
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
    # ENSURES NO INSTANCE OF EVENT IS ALREADY RUNNING
    # OTHERWISE THE EVENT WILL BE SHOWN RUNNING BY DEFAULT IN POLL() CALL
    # HOWEVER SUBPROCESS COULDN'T EXTEND CONTROL ON IT AS IT WASN'T STARTED BY IT
    system("TASKKILL /F /IM qbittorrent.exe")
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    event = subprocess.Popen(r"C:\\Program Files (x86)\\qBittorrent\\qbittorrent.exe",startupinfo=startupinfo)
    print()
    while(event.poll() == 1):
    	print("WAITING TO START")
    print("PROCESS STARTED")
    down_time=0
    up_time=time.time()
    last_usage=0
    ##############################################################################################################################

    while(True):
    	ajax_calls(url,headers,payload,stats)
    	for IP in IP_ADDRESSES:
    		node = stats.get(IP)
    		if(node is not None):
    			# STOPS EVENT ONLY IF USAGE INCREASES MENTIONED LIMITS
    			# AND THE PROCESS WAS ACTIVE
    			if((float(node[1]) > 4.0)):
    				if((event.poll() is None)):
	    				event = stop_event(event)
	    				down_time = time.time()
	    				print("TOTAL UP TIME:",round(down_time-up_time,2),"sec")
	    			# UPDATES LAST USAGE EVEN WHEN PROCESS IS CLOSED
	    			# THIS ENSURES THAT PROCESS IS STARTED ONLY IF THERE WAS NO USAGE
	    			# MAKING IT INDEPENDANT OF DOWN_TIME. THIS IS NECESSARY BECUASE DOWN_TIME IS
	    			# UPDATED ONLY WHEN PROCESS IS KILLED. THUS FIREWATCH MAKES INTELLIGENT DECISIONS
	    			# BASED ON LAST USAGE OF USERS. AND NOT LAST DOWN TIME OF APPLICATION
	    			last_usage = time.time()
	    			break

    	if((event.poll() == 1)):
    		# AS MENTIONED DECISION BASED ON LAST USAGE AND NOT DOWN TIME
    		if((time.time()-last_usage > 16.0)):
	    		event = start_event(event)
	    		up_time = time.time()
	    		print("TOTAL DOWN TIME:",round(up_time-down_time,2),"sec")
	    	else:
	    		print("THIS WAIT SHOULD REACH 16 sec, LAST USAGE:",round(time.time()-last_usage,2),"sec AGO")
    	else:
    		print("\t--> 142 (RUNNING)")
    	time.sleep(2)


def start_event(event):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    event = subprocess.Popen(r"C:\\Program Files (x86)\\qBittorrent\\qbittorrent.exe",startupinfo=startupinfo)
    while(event.poll() == 1):
    	print("WAITING TO START")
    print("PROCESS STARTED")
    return event

def stop_event(event):
    event.terminate()
    while(event.poll() is None):
    	print("WAITING TO KILL")
    print("PROCESS KILLED")
    return event

login()
#advanced()
#ipt_account()


IP_ADDRESSES = ['192.168.0.100','192.168.0.104']
Fire_Watch(IP_ADDRESSES)
