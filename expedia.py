# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:43:31 2016

@author: Moh2
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import re
import math
import matplotlib.pyplot as plt


link = "https://www.expedia.de/Hotel-Search?#&destination=Bangkok, Thailand&startDate=03.12.2016&endDate=10.12.2016&regionId=178236&latLong=13.747500,100.536010&adults=2&page=1"
baselink = "https://www.expedia.de/Hotel-Search?#&destination=Bangkok, Thailand&startDate=03.12.2016&endDate=10.12.2016&regionId=178236&latLong=13.747500,100.536010&adults=2&page="



driver = webdriver.PhantomJS(executable_path='C:/Users/Moh2/Desktop/scraping/phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver.set_window_size(1120,550)
driver.get(link)
driver.save_screenshot('loading.png')
sleep(30)
print "Got link.."

driver.save_screenshot('loaded.png')

s = BeautifulSoup(driver.page_source)


hotels = s.find("p",class_="showing-results")
tmp=hotels.string.encode("utf-8")
print tmp
kw = 'von'
loc = tmp.find(kw)
tmp=int(tmp[loc+4:len(tmp)])
npages = math.ceil(tmp/50.0)


prcs_mod = []
rvs =[]
scores = []
strs = []

print 'Scraping '+str(npages)+' pages...'
i=1

while i<=npages:
    print "scraping page "+str(i)
    link = baselink+str(i)
    driver.get(link)
    sleep(1)
    driver.save_screenshot('loade_pg_'+str(i)+'.png')
    s=BeautifulSoup(driver.page_source)
    
    hotels = s.findAll('div',class_='hotelWrapper')
    
    for hotel in hotels:
        tmp = hotel.findNext('span',class_='actualPrice fakeLink')
        if tmp:
            tmp = tmp.string.encode('utf-8')
            loc = tmp.find('€')
            tmp = tmp[0:loc-2]
            tmp = tmp.replace('.','')
            prcs_mod.append(int(tmp))
        else:
            prcs_mod.append(0)
            
        tmp=hotel.findNext('span',class_='hotelSearchResultReviewTotal reviewCount fakeLink')
        if tmp:
            tmp = tmp.string.encode('utf-8')
            loc1=tmp.find('(')
            loc2=tmp.find('B')
            tmp=tmp[loc1+1:loc2-1]
            rvs.append(int(tmp))
        else:
            rvs.append(0)
        
        tmp = hotel.find('span',class_='reviewOverall icon icon-infoalt')
        if tmp:
            tmp = tmp.string.encode('utf-8')
            loc = tmp.find('/')
            tmp = tmp[loc-3:loc]
            tmp=tmp[0]+tmp[2]
            tmpi = 2*int(tmp)
            scores.append(tmpi)
        else:
            scores.append(0)            
        
        star_cont = hotel.find("strong",class_='star-rating rating-secondary star rating')
        if star_cont:        
            tmp=star_cont.findNext('span')
            if tmp:
                tmp = tmp.string.encode('utf-8')
                loc = tmp.find('v')
                tmp = tmp[0:loc]
                tmp = tmp.replace('.','')
                strs.append(tmp)            
            else:
                strs.append(0)
        else:
            strs.append(0)
        
        
    i = i+1
    

driver.quit()


fig = plt.figure()
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 8,
        }
fontM = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 8,
        }
        
font_sel = font     
for ci in range(0,len(prcs_mod)):

    mark_code=''
    if strs[ci]>=50: # 5 stars
        mark_code='r'
    if strs[ci]>=40 and strs[ci]<50: # 4 stars
        mark_code='g'
    if strs[ci]>=30 and strs[ci]<40: # 3 stars
        #mark_code='b'
        continue
    if strs[ci]>=20 and strs[ci]<30: # 2 stars
        #mark_code='m'
        continue
    if strs[ci]>=10 and strs[ci]<20: # 1 stars
        #mark_code='k'
        continue
    
    if scores[ci]>=95 :
        mark_code=mark_code+"*"
        
    if scores[ci]>=90 and scores[ci]<95 :
        mark_code=mark_code+"d"

    if scores[ci]>=85 and scores[ci]<90 :
        mark_code=mark_code+"s"

    if scores[ci]>=80 and scores[ci]<85 :
        mark_code=mark_code+"o"
        
    if scores[ci]<80 :
        mark_code=mark_code+"x"

    

        
        

        
    plt.plot(rvs[ci],prcs_mod[ci],mark_code)
    #plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci], str(ci+1), fontdict=font_sel)



    
plt.grid()
plt.xlabel("Number of recommendations")
plt.ylabel("Price")
plt.axhline(500, 0,500, 300)
#plt.ylim(100,2000)
plt.show()
    
    




