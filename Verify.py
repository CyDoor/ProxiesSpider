#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import threading
import requests

# config-start
testUrl = "http://1212.ip138.com/ic.asp" # 利用了ip138的IP查询接口
timeout = 5 # 设置超时
threadNumber = 50 # 设置线程数
proxiesFileName = "proxies.txt"
successFileName = "success.txt"
# config-end

def testOnline(ip,port):
    '''
    测试HTTP代理是否可用
        利用IP138的接口 , 在响应的页面中寻找本机IP , 如果找到 , 则说明代理可以成功连接
    '''
    global successFileName
    global testUrl
    global timeout
    keyWord = ip
    proxies = {"http":"http://"+ip+":"+port}
    try:
        content=requests.get(testUrl,proxies=proxies,timeout=timeout).text
        if keyWord in content:
            print ip+":"+port
            file=open(successFileName,"a+")
            file.write(ip+":"+port+"\n")
            file.close()
        else:
            print "Proxy Error..."
    except Exception as e:
        print "NetWork Error..."

class myThread (threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
    def run(self):
        testOnline(self.ip,self.port)

proxies=open(proxiesFileName,"r")

threads = [] # 线程池

for proxy in proxies:
    line = proxy[0:-1]
    ip = line.split(":")[0] # 获取IP
    port = line.split(":")[1]
    threads.append(myThread(ip,port))

for t in threads:
    t.start()
    while True:
        if(len(threading.enumerate())<threadNumber):
            break
