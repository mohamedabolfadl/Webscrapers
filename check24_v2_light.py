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
meals = []
strs = []
#baselink = "https://urlaub.check24.de/suche/hotel?regionId=764&extendedSearch=1&sorting=rating&order=desc&regionSort=topregion&regionSortOrder=asc&hotelCategory=&airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&departureDate=2016-11-01&returnDate=2017-02-28&travelDuration=1w&adult=2&recommendation=-&page="
baselink = "https://urlaub.check24.de/suche/hotel?regionId=764&extendedSearch=1&regionSort=topregion&regionSortOrder=asc&hotelCategory=&airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&adult=2&departureDate=2016-11-01&returnDate=2017-02-28&travelDuration=1w&page="
while pc<=npages :
    print "page:"+str(pc)
    link = baselink+str(pc)
    pc = pc+1    
    page = urllib2.urlopen(link)
    soup_packtpage = BeautifulSoup(page)
    
    all_offers = soup_packtpage.find_all("div",class_="offer-cnt")
    for offer in all_offers:
        li=offer.find("a",class_="hotel-list-offer-link no-spin")
        if li:
            url = li["href"]
            urlss.append(url.encode('utf-8'))
        
        name = offer.find("div",class_="offer-header")
        if name:        
            tmp  = name.a.string.encode('utf-8')
            tmp = tmp[1:len(tmp)]
            hotel_names.append(tmp)  
            
        price = offer.find("span",class_="price")
        if price:        
            tmp = price.string.encode('utf-8')
            tmp=tmp.replace('.','')
            kw = " "
            k=tmp.find(kw)
            tmp=tmp[0:k]   
            prices_hotels.append(int(tmp))

        duration = offer.find("div",class_="duration")
        if duration:        
            tmp =        duration.string
            tmp=tmp.encode('utf-8')
            k=tmp.find(" ")
            tmp=tmp[0:k]
            durations.append(tmp)
            
            r = re.compile(r'hotel\-category\-b')
            star = offer.find("span",class_=r)
        if star:
            tmp = star['class']
            tmp = tmp[1]
            tmp = tmp [len(tmp)-2:len(tmp)]
            tmp = tmp.encode('utf-8')
            strs.append(tmp)
        
        kw = "B"
        nrecs = offer.find("span",class_="reviews")
        if nrecs:
            tmp = nrecs.string.encode('utf-8')
            k=tmp.find(kw)
            tmp=tmp[1:k-1]
            nummber_recs.append(int(tmp))
        else:
            nummber_recs.append(int("0"))
        
        kw = "%"
        recs = offer.find("span",class_="recommendation-percent")
        if recs:
            tmp=recs.string.encode('utf-8')
            k=tmp.find(kw)
            tmp=tmp[0:k]
            recommendation_values.append(int(tmp))
        else:
            recommendation_values.append(int("0"))
        
            

    time.sleep(1)
  
print "plotting..."

homedir = "C:/Users/Moh2/Desktop/scraping/dubai"
os.chdir(homedir)
destination = "Dubai_light_"+time.strftime("%d-%m-%Y")+"_"+time.strftime("%I-%M-%S")
os.mkdir(destination)



csvFile = open(homedir+"/"+destination+"/"+destination+".csv","w+")
try:
    writer =csv.writer(csvFile)
    writer.writerow(('Price','Duration','Recommendation','Number of recommendations','Stars','Name'))
    for ji in range(len(prices_hotels)):
        writer.writerow((prices_hotels[ji] , durations[ji] , recommendation_values[ji] ,nummber_recs[ji] , strs[ji], hotel_names[ji] ))
finally:
    csvFile.close()
    
    
    
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
for ci in range(0,len(durations)):

    mark_code=''
    if strs[ci][0]=='5': # 5 stars
        mark_code='r'
    if strs[ci][0]=='4': # 4 stars
        mark_code='g'
    if strs[ci][0]=='3': # 3 stars
        mark_code='b'
    if strs[ci][0]=='2': # 2 stars
        mark_code='m'
    if strs[ci][0]=='1': # 1 stars
        mark_code='k'
    
    if recommendation_values[ci]>=95 :
        mark_code=mark_code+"*"
        
    if recommendation_values[ci]>=90 and recommendation_values[ci]<95 :
        mark_code=mark_code+"d"

    if recommendation_values[ci]>=85 and recommendation_values[ci]<90 :
        mark_code=mark_code+"s"

    if recommendation_values[ci]>=80 and recommendation_values[ci]<85 :
        mark_code=mark_code+"o"
        
    if recommendation_values[ci]<80 :
        mark_code=mark_code+"x"

    

        
        

        
    plt.plot(nummber_recs[ci],prices_hotels[ci],mark_code)
    plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci], str(ci+1), fontdict=font_sel)



    
plt.grid()
plt.xlabel("Number of recommendations")
plt.ylabel("Price")
plt.axhline(500, 0,500, 300)
plt.ylim(100,2000)
plt.show()

fig.savefig(destination+'/dubai_fig.eps')
fig.savefig(destination+'/dubai_fig.png')
plt.ylim(400,1100)
plt.xlim(0,100)

fig.savefig(destination+'/dubai_fig_z.eps')
fig.savefig(destination+'/dubai_fig_z.png')

    
    
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
for ci in range(0,len(durations)):

    mark_code=''
    if strs[ci][0]=='5': # 5 stars
        mark_code='r'

    
        if recommendation_values[ci]>=95 :
            mark_code=mark_code+"*"
            
        if recommendation_values[ci]>=90 and recommendation_values[ci]<95 :
            mark_code=mark_code+"d"
    
        if recommendation_values[ci]>=85 and recommendation_values[ci]<90 :
            mark_code=mark_code+"s"
    
        if recommendation_values[ci]>=80 and recommendation_values[ci]<85 :
            mark_code=mark_code+"o"
            
        if recommendation_values[ci]<80 :
            mark_code=mark_code+"x"
    
        
    
            
            
    
            
        plt.plot(nummber_recs[ci],prices_hotels[ci],mark_code)
        plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci], str(ci+1), fontdict=font_sel)



    
plt.grid()
plt.xlabel("Number of recommendations")
plt.ylabel("Price")
plt.axhline(500, 0,500, 300)
plt.ylim(100,2000)
plt.show()

fig.savefig(destination+'/dubai_fig_5.eps')
fig.savefig(destination+'/dubai_fig_5.png')
plt.ylim(400,1100)
plt.xlim(0,100)

fig.savefig(destination+'/dubai_fig_z_5.eps')
fig.savefig(destination+'/dubai_fig_z_5.png')





    
    
    
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
for ci in range(0,len(durations)):

    mark_code=''
    if strs[ci][0]=='5': # 5 stars
        mark_code='r'
    if strs[ci][0]=='4': # 4 stars
        mark_code='g'

    
        if recommendation_values[ci]>=95 :
            mark_code=mark_code+"*"
            
        if recommendation_values[ci]>=90 and recommendation_values[ci]<95 :
            mark_code=mark_code+"d"
    
        if recommendation_values[ci]>=85 and recommendation_values[ci]<90 :
            mark_code=mark_code+"s"
    
        if recommendation_values[ci]>=80 and recommendation_values[ci]<85 :
            mark_code=mark_code+"o"
            
        if recommendation_values[ci]<80 :
            mark_code=mark_code+"x"
    
        
    
            
            
    
            
        plt.plot(nummber_recs[ci],prices_hotels[ci],mark_code)
        plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci], str(ci+1), fontdict=font_sel)



    
plt.grid()
plt.xlabel("Number of recommendations")
plt.ylabel("Price")
plt.axhline(500, 0,500, 300)
plt.ylim(100,2000)
plt.show()

fig.savefig(destination+'/dubai_fig_4.eps')
fig.savefig(destination+'/dubai_fig_4.png')
plt.ylim(400,1100)
plt.xlim(0,100)

fig.savefig(destination+'/dubai_fig_z_4.eps')
fig.savefig(destination+'/dubai_fig_z_4.png')

plt.close()

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

tfile.write("\\begin{figure}[htp!] \centering ")
tfile.write("\n")
tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{dubai_fig_5.eps} ")
tfile.write("\n")
tfile.write("\caption{5 star price vs popularity}")
tfile.write("\n")
tfile.write("\label{F:pvp} ")
tfile.write("\n")
tfile.write("\end{figure}")
tfile.write("\n")

tfile.write("\\begin{figure}[htp!] \centering ")
tfile.write("\n")
tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{dubai_fig_z_5.eps} ")
tfile.write("\n")
tfile.write("\caption{5 star price vs popularity zoom}")
tfile.write("\n")
tfile.write("\label{F:pvpz} ")
tfile.write("\n")
tfile.write("\end{figure}")
tfile.write("\n")


tfile.write("\\begin{figure}[htp!] \centering ")
tfile.write("\n")
tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{dubai_fig_4.eps} ")
tfile.write("\n")
tfile.write("\caption{4 star price vs popularity}")
tfile.write("\n")
tfile.write("\label{F:pvp} ")
tfile.write("\n")
tfile.write("\end{figure}")
tfile.write("\n")

tfile.write("\\begin{figure}[htp!] \centering ")
tfile.write("\n")
tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{dubai_fig_z_4.eps} ")
tfile.write("\n")
tfile.write("\caption{4 star price vs popularity zoom}")
tfile.write("\n")
tfile.write("\label{F:pvpz} ")
tfile.write("\n")
tfile.write("\end{figure}")
tfile.write("\n")

oi = 0
while oi<len(hotel_names):
    tfile.write("\section{\href{"+urlss[oi]+"}{"+hotel_names[oi].replace("&","\&")+"}-{\color{red}"+str(prices_hotels[oi])+"}-"+strs[oi][0]+"."+strs[oi][1]+" stars}")
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
os.chdir(homedir)
print "Done..."
#subprocess.call(comnd)

