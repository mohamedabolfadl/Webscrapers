# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 20:52:03 2017

@author: Moh2
"""



import re
import os 
import urllib 
import urllib2 
from selenium import webdriver 
from bs4 import BeautifulSoup 
from time import sleep 
import telepot

#NZDUSD 53668
#EURUSD_1 50592
#Crude 34824
#USDJPY 29816
#EURUSD_2 63753
#Sayyad 61544
#Fara7at 63005
#Gold 34781
#USDCAD 62017
#GBPJPY 49591
#GBPUSD 48205

telegram_token = '376116064:AAEKBXPsHxqvdDwqdDxn2amHRztIDzPs08s'
telegram_id = 353653926

topic_list = [63005,50592,34824,29816,63753,61544,53668,34781,62017,49591,48205]
topic_name = ['Fara7at','EURUSD1','Crude','USDJPY','EURUSD2','Sayyad','NZDUSD','Gold','USDCAD','GBPJPY','GBPUSD']
lastcomment_list = [2421,1631,1182,1085,2972,3353,332,1686,321,618,948]
updateRate = 300


def IsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False




def checkArabFXUpdates(topic_counter,driver,lcID):
    topic=topic_list[topic_counter]
    link = "http://www.arabfx.net/vb/showthread.php?t="+str(topic)+"&page=1"

    driver.get(link)

    #ulink=urllib2.urlopen(link)
    sleep(1)
    #s=BeautifulSoup(ulink)
    s=BeautifulSoup(driver.page_source)
    
    #sleep(5)
    elements = s.findAll("a",href=True)
    lastPg = -1
    for element in elements:
        tmpe = element['href']
        tmp =tmpe.encode('utf-8')
        if str(topic)+"&page=" in tmp:
            curr = tmp[tmp.find("page=")+5:len(tmp)]
            if(IsInt(curr)):
                if(int(curr)>lastPg):
                    lastPg=int(curr)
    #print lastPg
    lastlink = 'http://www.arabfx.net/vb/showthread.php?t='+str(topic)+'&page='+str(lastPg) 
# Getting last comment ID
    driver.get(lastlink)
    sleep(1) 
    s =BeautifulSoup(driver.page_source)
    #ulink=urllib2.urlopen(lastlink)
    #s=BeautifulSoup(ulink)
    sleep(1)
    elements = s.findAll("a",href=True,target=True,id=True) 
    #lastComm = -1 
    dates = []
    newComment = False
    newCommentCount = 0
    startIDofNewComment = -1
    element_i = 0
    for element in elements:
        curr = element['name'].encode("utf-8")
        #print date    
        if(IsInt(curr)):
            if(int(curr)>lcID):
                lcID= int(curr)
                tes = element.findParent("div").get_text().replace('\n','-')
                dates.append(tes[20:41])
                newComment = True
                newCommentCount = newCommentCount +1
                if(startIDofNewComment<0):
                    startIDofNewComment = element_i
        element_i =element_i +1
    if(newComment):
        f = open('lc'+str(topic_counter)+'.txt', 'w')
        f.write(str(lcID))
        f.close()
        str_send= 'ARABFX '+topic_name[topic_counter] + ': \n'
        print 'Got '+str(newCommentCount)+' new comment(s) ... sending them'
        #print dates
        r = re.compile(r'post_message_\d+')
        comments = s.findAll('div',id=r)
        r = re.compile(r'\.png')
        img_c = 1
        send_i=0        
        comment_i = 0
        for comment in comments:
            if(comment_i>startIDofNewComment-1):            
                message2send = comment.get_text().replace('\n','-')
                bot.sendMessage(telegram_id, str_send+dates[send_i]+'\n'+message2send)
                send_i=send_i+1
                #print comment.get_text().replace('\n','-')
                #print '------------------------------------------'
                txts=comment.findAll("img",src=r,border=True,width=True,height=True)
        
                for txt in txts:
                    curr=txt["src"].encode("utf-8")
                    stid=curr.find("www.")
                    imgURL=str(curr[stid:len(curr)])
                    imgURL='http://'+imgURL
                    file_name = topic_name[topic_counter]+str(img_c)+".png"
                    urllib.urlretrieve(imgURL,file_name)
                    f = open(file_name, 'rb')
                    bot.sendPhoto(telegram_id,f)
                    f.close()
                    img_c=img_c+1 
                comment_i = comment_i+1
                bot.sendMessage(telegram_id, '--------------------------------------')
            else:
                comment_i = comment_i+1                    

    
def checkFSysRUUpdates(driver,lcID):
    
    link = "http://forexsystemsru.com/besplatnye-torgovye-signaly/82423-free-forex-trading-signals-daily-1.html"

    driver.get(link)

    #ulink=urllib2.urlopen(link)
    sleep(1)
    #s=BeautifulSoup(ulink)
    s=BeautifulSoup(driver.page_source)
    
    #sleep(5)
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
    #print lastPg
    lastlink = 'http://forexsystemsru.com/besplatnye-torgovye-signaly/82423-free-forex-trading-signals-daily-'+str(lastPg)+'.html' 
# Getting last comment ID
    driver.get(lastlink)
    sleep(1) 
    s =BeautifulSoup(driver.page_source)
    #ulink=urllib2.urlopen(lastlink)
    #s=BeautifulSoup(ulink)
    sleep(1)
    elements = s.findAll("a",href=True,target=True,id=True) 
    #lastComm = -1 
    dates = []
    newComment = False
    newCommentCount = 0
    startIDofNewComment = -1
    element_i = 0
    for element in elements:
        curr = element['name'].encode("utf-8")
        #print date    
        if(IsInt(curr)):
            if(int(curr)>lcID):
                lcID= int(curr)
                dates.append(element.findParent("div").findParent("div").findNext("span").get_text())
                newComment = True
                newCommentCount = newCommentCount +1
                if(startIDofNewComment<0):
                    startIDofNewComment = element_i
        element_i =element_i +1
    if(newComment):
        f = open('SySRUS_lc.txt', 'w')
        f.write(str(lcID))
        f.close()
        str_send= 'SySRUS: \n'
        print 'Got '+str(newCommentCount)+' new comment(s) ... sending them'
        #print dates
        r = re.compile(r'post_message_\d+')
        comments = s.findAll('div',id=r)
        r = re.compile(r'\.png')
        img_c = 1
        send_i=0        
        comment_i = 0
        for comment in comments:
            if(comment_i>startIDofNewComment-1):            
                message2send=comment.get_text()
                message2send=message2send[message2send.find('[B]'):len(message2send)].replace('[B]Forex Market Trading Signals:','')
                bot.sendMessage(telegram_id, str_send+dates[send_i]+'\n'+message2send)
                send_i=send_i+1
                #print comment.get_text().replace('\n','-')
                #print '------------------------------------------'
                txts=comment.findAll("img",src=r)
        
                for txt in txts:
                    imgURL=txt["src"].encode("utf-8")
                    file_name = 'SySRUS_'+str(img_c)+".png"
                    urllib.urlretrieve(imgURL,file_name)
                    f = open(file_name, 'rb')
                    bot.sendPhoto(telegram_id,f)
                    f.close()
                    img_c=img_c+1 
                comment_i = comment_i+1
                bot.sendMessage(telegram_id, '--------------------------------------')
            else:
                comment_i = comment_i+1   
                

#driver = webdriver.PhantomJS(executable_path='C:/Users/Moh2/Desktop/scraping/phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver = webdriver.PhantomJS()
driver.set_window_size(50, 50)

bot = telepot.Bot(telegram_token)

while 1:
    topic_counter = 0
    while topic_counter<len(topic_list):
        f = open('lc'+str(topic_counter)+'.txt', 'rb')
        lc_curr = int(f.read())
        f.close()
        print '----------------------------'
        print 'Topic of '+topic_name[topic_counter]+' with ID '+str(topic_counter)
        checkArabFXUpdates(topic_counter,driver,lc_curr)
        topic_counter=topic_counter+1
    f = open('SySRUS_lc.txt', 'rb')
    lc_curr = int(f.read())
    f.close()
    print '----------------------------'
    print 'Topic of SysRus'
    checkFSysRUUpdates(driver,lc_curr)
    
    sleep(updateRate)




driver.quit()     








    
#while 1:
    
#    topic_counter = 1
#    while topic_counter<len(topic_list)+1:
#        checkArabFXUpdates(topic_counter,driver)
#    topic_counter=topic_counter+1    
    
#    sleep(updateRate)






