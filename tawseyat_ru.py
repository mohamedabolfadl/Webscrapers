# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 19:15:49 2017

@author: Moh2
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 21:00:47 2017

@author: Moh2
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 14:53:18 2017

@author: Moh2
"""

import re
import os 
import urllib 
import urllib2 
from selenium import webdriver 
from bs4 import BeautifulSoup 
from time import sleep 
import numpy as np 
import matplotlib.pyplot as plt
def IsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

live=True
if(live):
    link = "http://forexsystemsru.com/besplatnye-torgovye-signaly/82423-free-forex-trading-signals-daily-1.html"
    driver = webdriver.PhantomJS(executable_path='C:/Users/Moh2/Desktop/scraping/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.set_window_size(50, 50)
    driver.get(link)

    sleep(1)
    s=BeautifulSoup(driver.page_source)
    sleep(1)

    
    elements = s.findAll("a",href=True)
    lastPg = -1
    for element in elements:
        tmpe = element['href']
        tmp =tmpe.encode('utf-8')
        if "free-forex-trading-signals-daily-" in tmp:
            curr = tmp[tmp.find("page=")+5:len(tmp)]
            st = curr.find('.html')
            curr=curr[st-2:st]            
            
            if(IsInt(curr)):
                if(int(curr)>lastPg):
                    lastPg=int(curr)
    print lastPg
    lastlink = 'http://forexsystemsru.com/besplatnye-torgovye-signaly/82423-free-forex-trading-signals-daily-'+str(lastPg)+'.html' 
# Getting last comment ID
    driver.get(lastlink)
    sleep(1)
    s=BeautifulSoup(driver.page_source)
    sleep(1)
else:
    html_data = open ("fx_pg242.htm1",'r').read()
    s = BeautifulSoup(html_data) 
elements = s.findAll("a",href=True,target=True,id=True) 
lastComm = -1 
dates = []
#dates =  = [0] * len(elements)
ic=0
for element in elements:
    curr = element['name'].encode("utf-8")
    dates.append(element.findParent("div").findParent("div").findNext("span").get_text())
    ic=ic+1
    if(IsInt(curr)):
        if(int(curr)>lastComm):
            lastComm= int(curr)
print dates
print 'Last comment ID='+str(lastComm)
r = re.compile(r'post_message_\d+')
comments = s.findAll('div',id=r)
r = re.compile(r'\.png')
img_c = 1
lastComm = -1
print 'Number of comments='+str(len(comments))
for comment in comments:
    comm=comment.get_text()
    comm=comm[comm.find('[B]'):len(comm)].replace('[B]Forex Market Trading Signals:','')
    print comm
    txts=comment.findAll("img",src=r,border=True)
    #print comment    
    #print 'Lenght of text='+str(len(txts))
    for txt in txts:
        curr=txt["src"].encode("utf-8")
        print curr
        #stid=curr.find("www.")
        #imgURL=str(curr[stid:len(curr)])
        #imgURL='http://'+imgURL
        urllib.urlretrieve(curr,str(img_c)+".png")
        img_c=img_c+1 

driver.quit()










