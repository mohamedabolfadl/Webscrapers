# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:43:31 2016

@author: Moh2
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import re

print "Started..."
link = "http://www.momondo.de/flightsearch/?Search=true&TripType=2&SegNo=2&SO0=MUC&SD0=LCA&SDP0=11-08-2016&SO1=LCA&SD1=MUC&SDP1=18-08-2016&AD=1&TK=ECO&DO=false&NA=false"
print "Creating driver..."
driver = webdriver.PhantomJS(executable_path='C:/Users/Moh2/Desktop/scraping/phantomjs-2.1.1-windows/bin/phantomjs.exe')
sleep(10)

print "Setting window size..."
driver.set_window_size(1120,550)
print "Asked for link now waiting.."
driver.get(link)
sleep(20)
print "Got link.."

driver.save_screenshot('pg1.png')

s = BeautifulSoup(driver.page_source)
print "Finished waiting"
r = re.compile(r'height:\s\d+\.*\d*%;')
elements = s.findAll("div",style=r)
hlth =[]
prices=[]
dates = []
for element in elements:
    tmp = element['style'].encode("utf-8")
    if tmp:
        kw="%"
        loc = tmp.find(kw)
        tmp = tmp[8:loc]
        hlth.append(tmp)
        dt = element.findNext("span",class_="date")
        if dt:
            dates.append(dt.string.encode('utf-8'))
        prc = element.findNext("span",class_="price")
        if prc:
            tmp = prc.string.encode('utf-8')
            tmp = tmp[3:len(tmp)]
            prices.append(int(tmp))

print "Grabbing prices"
elements = s.findAll("span",class_="value")
if elements:
    prcs = []
    for element in elements:
        if (len(element.attrs)<2 and element.findParent('div',class_='price-pax')):
            prcs.append(element.string.encode('utf-8'))            
else:
    print "No prices found"


print "Grabbing airports"
elements = s.findAll("span",class_="iata")
if elements:
    arps = []
    for element in elements:
        if (len(element.attrs)<2):
            arps.append(element.string.encode('utf-8'))            
else:
    print "No airports found"


print "Grabbing airlines"
elements = s.findAll("div",class_="names")
if elements:
    als = []
    for element in elements:
        if (len(element.attrs)<2):
            als.append(element.string.encode('utf-8'))            
else:
    print "No airlines found"


print "Grabbing travel times"
elements = s.findAll("div",class_="travel-time")
if elements:
    travel_times = []
    for element in elements:
        if (len(element.attrs)<2):
            travel_times.append(element.string.encode('utf-8'))            
else:
    print "No travel times found"


sleep(1.1)
#next_page_elem = driver.find_element_by_xpath('//*[@id="results-tickets"]/div[2]div[2]div/ul/li[6]')
next_page_elem = driver.find_element_by_xpath('//*[@id="results-tickets"]/div[2]/div[2]/div/ul/li[6]')
next_page_elem.click()
sleep(0.5)
driver.save_screenshot('pg2.png')



driver.quit()










