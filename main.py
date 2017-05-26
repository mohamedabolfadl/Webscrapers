# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 17:13:52 2016

@author: Moh2
"""
import re
import urllib2
from bs4 import BeautifulSoup
import time 
import matplotlib.pyplot as plt
import os
#, sys
#import subprocess
import csv

        


def scrapeIt(dname,regId,mealID):
    
    npages = 10
    pc = 1
    urlss = []
    nummber_recs = []
    recommendation_values = []
    hotel_names = []
    prices_hotels =[]
    durations = []
    strs = []
    if mealID==0:
        baselink = "https://urlaub.check24.de/suche/hotel?regionId="+str(regId)+"&extendedSearch=1&regionSort=topregion&regionSortOrder=asc&hotelCategory=&airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&adult=2&departureDate=2016-12-15&returnDate=2017-02-28&travelDuration=1w&page="
        mealOpt =""
    if mealID==1:
        baselink = "https://urlaub.check24.de/suche/hotel?airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&adult=2&departureDate=2016-12-15&returnDate=2017-02-28&travelDuration=1w&catering=breakfast&regionId="+str(regId)+"&recommendation=-&sorting=categoryDistribution&order=asc&regionSort=topregion&regionSortOrder=asc&extendedSearch=1&oceanView=0&page="
        mealOpt ="minBreakFast"
    if mealID==2:
        baselink = "https://urlaub.check24.de/suche/hotel?airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&adult=2&departureDate=2016-12-15&returnDate=2017-02-28&travelDuration=1w&catering=halfboard&regionId="+str(regId)+"&recommendation=-&sorting=categoryDistribution&order=asc&regionSort=topregion&regionSortOrder=asc&extendedSearch=1&oceanView=0&page="
        mealOpt ="minHalbPension"
    if mealID==3:
        baselink = "https://urlaub.check24.de/suche/hotel?airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&adult=2&departureDate=2016-12-15&returnDate=2017-02-28&travelDuration=1w&catering=fullboard&regionId="+str(regId)+"&recommendation=-&sorting=categoryDistribution&order=asc&regionSort=topregion&regionSortOrder=asc&extendedSearch=1&oceanView=0&page="
        mealOpt ="minVollPension"

    if mealID==4:
        baselink = "https://urlaub.check24.de/suche/hotel?airport=BLL,BRE,BSL,CGN,CSO,DRS,DTM,DUS,EIN,ENS,ERF,FDH,FKB,FMM,FMO,FRA,GWT,HAJ,HAM,HDF,HHN,INN,KSF,LBC,LEJ,LGG,LUX,MST,MUC,NRN,NUE,PAD,PRG,RLG,SCN,STR,SXB,SXF,SZG,SZW,TXL,ZQW,ZRH&adult=2&departureDate=2016-12-15&returnDate=2017-02-28&travelDuration=1w&catering=allinclusive&regionId="+str(regId)+"&recommendation=-&sorting=categoryDistribution&order=asc&regionSort=topregion&regionSortOrder=asc&extendedSearch=1&oceanView=0&page="
        mealOpt ="minAllInklusiv"

    link = baselink+str(1)
    try:
        page = urllib2.urlopen(link)
        soup_packtpage = BeautifulSoup(page)
        
        pages = soup_packtpage.find("ul",class_="paging-cnt")
        if pages:            
            page_links = pages.find_all("li")
            tmp = page_links[len(page_links)-2].a.string.encode('utf-8')
            npages = int(tmp[1:len(tmp)-1])
        else:
            npages = 1
        print "Scraping "+str(npages)+" pages..."

            


    except:
        print "Couldnt open link to get npages, setting it to 10 instead"
        print link

 

    while pc<=npages :
        print "page:"+str(pc)
        link = baselink+str(pc)
        #print link
        pc = pc+1    
        if pc>2:
            try:
                page = urllib2.urlopen(link)
                soup_packtpage = BeautifulSoup(page)
            except:
                print "Failed to open this page, skipping..."
                print link
                continue
        if pc==1:
            pages = soup_packtpage.find("ul",class_="paging-cnt")
            page_links = pages.find_all("li")
            npages = page_links[len(page_links)-2].a.string
        
        all_offers = soup_packtpage.find_all("div",class_="offer-cnt")
        #print str(len(all_offers))
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
            nrecs = offer.find("span",class_="review-count")
            if nrecs:
                tmp = nrecs.string.encode('utf-8')
                k=tmp.find(kw)
                tmp=tmp[1:k-1]
                tmp = tmp.replace(".","")
                nummber_recs.append(int(tmp))
            else:
                nummber_recs.append(int("0"))
            
            kw = "/"
            recs = offer.find("span",class_="rating-scale")
            if recs:
                tmp=recs.text.encode('utf-8')
                k=tmp.find(kw)
                tmp=tmp[k-4:k-1]
                tmp= tmp.replace(",","")
                #print tmp
                recommendation_values.append(int(tmp))
            else:
                recommendation_values.append(int("0"))
            
                
    
        time.sleep(1)
      
    print "plotting..."
    
    homedir = "C:/Users/Moh2/Desktop/scraping/"+dname
    os.chdir(homedir)
    destination = dname+"_light_"+time.strftime("%d-%m-%Y")+"_"+time.strftime("%I-%M-%S")+mealOpt
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
        
        if recommendation_values[ci]>=55 :
            mark_code=mark_code+"*"
            
        if recommendation_values[ci]>=50 and recommendation_values[ci]<55 :
            mark_code=mark_code+"d"
    
        if recommendation_values[ci]>=45 and recommendation_values[ci]<50 :
            mark_code=mark_code+"s"
    
        if recommendation_values[ci]>=40 and recommendation_values[ci]<45 :
            mark_code=mark_code+"o"
            
        if recommendation_values[ci]<40 :
            mark_code=mark_code+"x"
    
        
    
            
            
    
            
        plt.plot(nummber_recs[ci],prices_hotels[ci],mark_code)
        plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci], str(ci+1), fontdict=font_sel)
    
    
    
        
    plt.grid()
    plt.xlabel("Number of recommendations")
    plt.ylabel("Price")
    plt.axhline(500, 0,500, 300)
    plt.ylim(100,2000)
    plt.show()
    
    fig.savefig(destination+'/'+dname+'_fig.eps')
    fig.savefig(destination+'/'+dname+'_fig.png')
    plt.ylim(400,1100)
    plt.xlim(0,100)
    
    fig.savefig(destination+'/'+dname+'_fig_z.eps')
    fig.savefig(destination+'/'+dname+'_fig_z.png')
    
    plt.close()
        
    fig = plt.figure()
    font = {'family': 'serif',
            'color':  'black',
            'weight': 'normal',
            'size': 8,
            }

            
    font_sel = font     
    for ci in range(0,len(durations)):
    
        mark_code=''
        if strs[ci][0]=='5': # 5 stars
            mark_code='r'
    
        
            if recommendation_values[ci]>=55 :
                mark_code=mark_code+"*"
                
            if recommendation_values[ci]>=50 and recommendation_values[ci]<55 :
                mark_code=mark_code+"d"
        
            if recommendation_values[ci]>=45 and recommendation_values[ci]<50 :
                mark_code=mark_code+"s"
        
            if recommendation_values[ci]>=40 and recommendation_values[ci]<45 :
                mark_code=mark_code+"o"
                
            if recommendation_values[ci]<40 :
                mark_code=mark_code+"x"
        
            
        
                
                
        
                
            plt.plot(nummber_recs[ci],prices_hotels[ci],mark_code)
            plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci], str(ci+1), fontdict=font_sel)
    
    
    
        
    plt.grid()
    plt.xlabel("Number of recommendations")
    plt.ylabel("Price")
    plt.axhline(500, 0,500, 300)
    plt.ylim(100,2000)
    plt.show()
    
    fig.savefig(destination+'/'+dname+'_fig_5.eps')
    fig.savefig(destination+'/'+dname+'_fig_5.png')
    plt.ylim(400,1100)
    plt.xlim(0,100)
    
    fig.savefig(destination+'/'+dname+'_fig_z_5.eps')
    fig.savefig(destination+'/'+dname+'_fig_z_5.png')
    
    
    
    plt.close()
    
        
        
        
    fig = plt.figure()
    font = {'family': 'serif',
            'color':  'black',
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
    
        
            if recommendation_values[ci]>=55 :
                mark_code=mark_code+"*"
                
            if recommendation_values[ci]>=50 and recommendation_values[ci]<55 :
                mark_code=mark_code+"d"
        
            if recommendation_values[ci]>=45 and recommendation_values[ci]<50 :
                mark_code=mark_code+"s"
        
            if recommendation_values[ci]>=40 and recommendation_values[ci]<45 :
                mark_code=mark_code+"o"
                
            if recommendation_values[ci]<40 :
                mark_code=mark_code+"x"
        
            
        
                
                
        
                
            plt.plot(nummber_recs[ci],prices_hotels[ci],mark_code)
            plt.text(0.5+nummber_recs[ci],-5+prices_hotels[ci], str(ci+1), fontdict=font_sel)
    
    
    
        
    plt.grid()
    plt.xlabel("Number of recommendations")
    plt.ylabel("Price")
    plt.axhline(500, 0,500, 300)
    plt.ylim(100,2000)
    plt.show()
    
    fig.savefig(destination+'/'+dname+'_fig_4.eps')
    fig.savefig(destination+'/'+dname+'_fig_4.png')
    plt.ylim(400,1100)
    plt.xlim(0,100)
    
    fig.savefig(destination+'/'+dname+'_fig_z_4.eps')
    fig.savefig(destination+'/'+dname+'_fig_z_4.png')
    
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
    tfile.write("\\title{"+dname+"}")
    tfile.write("\n")
    tfile.write("\\begin{document}")
    tfile.write("\n")
    tfile.write("\maketitle")
    tfile.write("\n")
    
    tfile.write("\\begin{figure}[htp!] \centering ")
    tfile.write("\n")
    tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{"+dname+"_fig.eps} ")
    tfile.write("\n")
    tfile.write("\caption{price vs popularity}")
    tfile.write("\n")
    tfile.write("\label{F:pvp} ")
    tfile.write("\n")
    tfile.write("\end{figure}")
    tfile.write("\n")
    
    tfile.write("\\begin{figure}[htp!] \centering ")
    tfile.write("\n")
    tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{"+dname+"_fig_z.eps} ")
    tfile.write("\n")
    tfile.write("\caption{price vs popularity zoom}")
    tfile.write("\n")
    tfile.write("\label{F:pvpz} ")
    tfile.write("\n")
    tfile.write("\end{figure}")
    tfile.write("\n")
    
    tfile.write("\\begin{figure}[htp!] \centering ")
    tfile.write("\n")
    tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{"+dname+"_fig_5.eps} ")
    tfile.write("\n")
    tfile.write("\caption{5 star price vs popularity}")
    tfile.write("\n")
    tfile.write("\label{F:pvp} ")
    tfile.write("\n")
    tfile.write("\end{figure}")
    tfile.write("\n")
    
    tfile.write("\\begin{figure}[htp!] \centering ")
    tfile.write("\n")
    tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{"+dname+"_fig_z_5.eps} ")
    tfile.write("\n")
    tfile.write("\caption{5 star price vs popularity zoom}")
    tfile.write("\n")
    tfile.write("\label{F:pvpz} ")
    tfile.write("\n")
    tfile.write("\end{figure}")
    tfile.write("\n")
    
    
    tfile.write("\\begin{figure}[htp!] \centering ")
    tfile.write("\n")
    tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{"+dname+"_fig_4.eps} ")
    tfile.write("\n")
    tfile.write("\caption{4 star price vs popularity}")
    tfile.write("\n")
    tfile.write("\label{F:pvp} ")
    tfile.write("\n")
    tfile.write("\end{figure}")
    tfile.write("\n")
    
    tfile.write("\\begin{figure}[htp!] \centering ")
    tfile.write("\n")
    tfile.write("\includegraphics[keepaspectratio=true, width=210mm]{"+dname+"_fig_z_4.eps} ")
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





if __name__ == '__main__':
#    region_ids = ['1079','821','818','734','703','697','547','673','1077','1078','682','720','551','674','764']
#    region_names=['maldives','thailandPhuket','thailandBangkok','mexicoCancun','bahamas','dominican','teneriffe','egyptHurghada','mauritius','seychelles','southafricaCapetown','miami','grancanaria','egyptSharm','dubai']
    region_ids = ['764']
    region_names=['dubai']
    
    i=0   
    while i<len(region_ids):
        print "Scraping "+region_names[i]
 #       print "scraping all options"
 #       scrapeIt(region_names[i],region_ids[i],0) # All
#        print "scraping min breakfast"
#        scrapeIt(region_names[i],region_ids[i],1) # All
        print "scraping min half board"
        scrapeIt(region_names[i],region_ids[i],2) # All
#        print "scraping min full board"
#        scrapeIt(region_names[i],region_ids[i],3) # All
#        print "scraping all inklusiv"
#        scrapeIt(region_names[i],region_ids[i],4) # All
        i=i+1








