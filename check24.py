# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 18:05:08 2016

@author: Moh2
"""

import re
import urlparse
import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import matplotlib.pyplot as plt
import numpy as np
import os
#, sys
#import subprocess
import csv
# save everything even without recommendations and place "-" in no recommendation field
# Save a structure with hotel id and price... so that we can plot vs time


npages = 8
pc = 1
urlss = []
nummber_recs = []
recommendation_values = []
hotel_names = []
prices_hotels =[]
durations = []
airports = []
dep_dates = []
ret_dates = []
isOffers = []
hotel_ids = []
nonrated_prices = []
#baselink = "https://urlaub.check24.de/suche/hotel?regionId=764&extendedSearch=1&sorting=rating&order=desc&regionSort=topregion&regionSortOrder=asc&hotelCategory=&airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&departureDate=2016-11-01&returnDate=2017-02-28&travelDuration=1w&adult=2&recommendation=-&page="
baselink = "https://urlaub.check24.de/suche/hotel?regionId=764&extendedSearch=1&regionSort=topregion&regionSortOrder=asc&hotelCategory=&airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&adult=2&departureDate=2016-11-01&returnDate=2017-02-28&travelDuration=1w&page="
while pc<=npages :
    print "page:"+str(pc)
    link = baselink+str(pc)
    pc = pc+1    
    page = urllib2.urlopen(link)
    soup_packtpage = BeautifulSoup(page)
    
    
    ban=[]
    i=1
    #getting urls
    print "picking urls..."
    all_offers = soup_packtpage.find_all("a",class_="hotel-list-offer-link no-spin")
    for offer in all_offers:
        st = time.time()        
        print "url no.="+str(i)
        time.sleep(0.75)
        div = offer.findParent("div",class_="offer-cnt")
        rev = div.findAll("span",class_="reviews")
        if rev:
            tmp = offer["href"]
            tmp=tmp.encode('utf-8')
            urlss.append(tmp)
            k=tmp.find("hotelId=")
            hotel_ids.append(tmp[k+8:len(tmp)])
            trip_page = urllib2.urlopen(tmp)
            soup = BeautifulSoup(trip_page)
            offer_box = soup.find("div",class_="offer-box")
            duration = offer_box.find_next("span")
            tmp =        duration.string
            tmp=tmp.encode('utf-8')
            k=tmp.find(" ")
            tmp=tmp[0:k]
            durations.append(tmp)
            tmp = duration.find_next("span").string
            tmp = tmp.encode('utf-8')
            airports.append(tmp)
            dep = soup.find("span",class_="flight-date-ele")
            tmp = dep.string
            tmp = tmp.encode('utf-8')
            tmp = tmp[4:12]
            dep_dates.append(tmp)
            ret = dep.find_next("span",class_="flight-date-ele")
            tmp = ret.string
            tmp = tmp.encode('utf-8')
            tmp = tmp[4:12]
            ret_dates.append(tmp)
            isOffer = div.find("span",class_="stroke-price-ele")
            if isOffer:
                isOffers.append(1)
            else:
                isOffers.append(0)
             
                
        else:
            ban.append(i)
        i = i+1
        en = time.time()
        elap = en-st
        #print "Rest time ="+str((((npages+1-pc)*25*elap)+elap*(25-i))/60)+" minutes"
    
    print "picking number of recommendations..."
    kw = "B"
    # Getting number of recommendations
    all_nrecs = soup_packtpage.find_all("span",class_="reviews")
    for nrec in all_nrecs:
        tmp = nrec.string.encode('utf-8')
        k=tmp.find(kw)
        tmp=tmp[1:k-1]
        nummber_recs.append(int(tmp))
    print "picking recommendations..."    
    kw = "%"
    # Getting recommendations
    all_recs = soup_packtpage.find_all("span",class_="recommendation-percent")
    for rec in all_recs:
        tmp=rec.string.encode('utf-8')
        k=tmp.find(kw)
        tmp=tmp[0:k]
        recommendation_values.append(int(tmp))
    print "picking titles..."
    # Getting title
    i=1
    all_titles = soup_packtpage.find_all("div",class_="offer-header")
    for title in all_titles:
        #div = title.findParent("div",class_="offer-cnt")
        #rev = div.findAll("span",class_="reviews")
        #if rev:
         if i not in ban:
            tmp  = title.a.string.encode('utf-8')
            tmp = tmp[1:len(tmp)]
            hotel_names.append(tmp)
         i=i+1
    
    kw = " "
    i=1
    print "picking prices..."
    # Getting prices
    all_prices = soup_packtpage.find_all("span",class_="price")
    for price in all_prices:
        tmp = price.string.encode('utf-8')
        tmp=tmp.replace('.','')
        k=tmp.find(kw)
        tmp=tmp[0:k]   
        #div = price.findParent("div",class_="offer-cnt")
        #rev = div.findAll("span",class_="reviews")
        #if rev:
        if i not in ban:
            prices_hotels.append(int(tmp))
        else:
            nonrated_prices.append(int(tmp))
        i=i+1
        
    time.sleep(1)
print "plotting..."

homedir = "C:/Users/Moh2/Desktop/scraping"
os.chdir(homedir)
destination = "Dubai_"+time.strftime("%d-%m-%Y")+"_"+time.strftime("%I-%M-%S")
os.mkdir(destination)



csvFile = open(homedir+"/"+destination+"/"+destination+".csv","w+")
try:
    writer =csv.writer(csvFile)
    writer.writerow(('Hotel ID','Price','Airport','Dep','Arr','Duration','Recommendation','Number of recommendations','Stars','Meal','Name'))
    for ji in range(len(prices_hotels)):
        writer.writerow(( hotel_ids[ji] ,prices_hotels[ji] , airports[ji] , dep_dates[ji] , ret_dates[ji] , durations[ji] , recommendation_values[ji] ,nummber_recs[ji] , 3,"HP", hotel_names[ji] ))
finally:
    csvFile.close()
    
    
    
fig = plt.figure()
fontr = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 4,
        }
fontb = {'family': 'serif',
        'color':  'blue',
        'weight': 'normal',
        'size': 4,
        }        
for ci in range(0,len(durations)):
    tmp = airports[ci]
    if len(tmp)==8 and tmp[0]=='M':
        plt.plot(nummber_recs[ci],prices_hotels[ci],'ro')
        plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci], str(ci)+"|"+str(recommendation_values[ci]), fontdict=fontr)
    else:
        plt.plot(nummber_recs[ci],prices_hotels[ci],'bo')
        plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci],str(ci)+"|"+str(recommendation_values[ci]), fontdict=fontb)



    
plt.plot(np.zeros(len(nonrated_prices)),nonrated_prices,'yo')

plt.grid()
plt.xlabel("Number of recommendations")
plt.ylabel("Price")
plt.axhline(500, 0,500, 300)
plt.ylim(100,2000)
plt.show()

fig.savefig(destination+'/dubai_fig.eps')
fig.savefig(destination+'/dubai_fig.png')

plt.xlim(0,100)

fig.savefig(destination+'/dubai_fig_z.eps')
fig.savefig(destination+'/dubai_fig_z.png')

print "filling latex..."




tfile = open(destination+'/'+str(destination)+".tex", "w")
tfile.write("\n")
tfile.write("\documentclass{article}")
tfile.write("\n")
tfile.write("\usepackage[a4paper, total={8in, 10in}]{geometry}")
tfile.write("\n")
tfile.write("\usepackage{color}")
tfile.write("\n")
tfile.write("\usepackage{mathrsfs,amsfonts,graphicx,color, amsmath, setspace, epstopdf,caption,slashbox,hyperref}")
tfile.write("\n")
tfile.write("\setlength\parindent{0pt}")
tfile.write("\n")
tfile.write("\\title{Dubai}")
tfile.write("\n")
tfile.write("\\begin{document}")
tfile.write("\n")
tfile.write("\maketitle")
tfile.write("\n")
oi = 0
tfile.write("\\begin{figure}[htp!] \centering ")
tfile.write("\n")
tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{dubai_fig.eps} ")
tfile.write("\n")
tfile.write("\caption{price vs popularity}")
tfile.write("\n")
tfile.write("\label{F:pvp} ")
tfile.write("\n")
tfile.write("\end{figure}")
tfile.write("\n")

tfile.write("\\begin{figure}[htp!] \centering ")
tfile.write("\n")
tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{dubai_fig_z.eps} ")
tfile.write("\n")
tfile.write("\caption{price vs popularity zoom}")
tfile.write("\n")
tfile.write("\label{F:pvpz} ")
tfile.write("\n")
tfile.write("\end{figure}")
tfile.write("\n")


while oi<len(urlss):
    tfile.write("\section{"+hotel_names[oi].replace("&","\&")+"-{\color{red}"+str(prices_hotels[oi])+"}-"+"("+str(hotel_ids[oi])+")"+"}")
    tfile.write("\n")
    tfile.write("Airport:"+str(airports[oi])+"-")
    tfile.write("\n")    
    tfile.write("Dep date:"+str(dep_dates[oi])+"-")
    tfile.write("\n")
    tfile.write("Ret date:"+str(ret_dates[oi])+"-")
    tfile.write("\n")
    tfile.write("Recommendations:"+str(recommendation_values[oi])+"\% -")
    tfile.write("\n")
    tfile.write("Number of Rec:"+str(nummber_recs[oi])+"-")
    tfile.write("\n")
    tfile.write("Duration:"+str(durations[oi])+"-")
    tfile.write("\n")
    tfile.write("\n")
    tfile.write("\n")
    
    
    
    oi=oi+1

tfile.write("\n")    
tfile.write("\end{document}")    
tfile.close()  
print "Compiling latex..."

time.sleep(1)
os.chdir(destination)
comnd = "pdflatex.exe -synctex=1 -interaction=nonstopmode "+destination+".tex"
os.system(comnd)
os.chdir("C:/Users/Moh2/Desktop/scraping")
print "Done..."
#subprocess.call(comnd)

