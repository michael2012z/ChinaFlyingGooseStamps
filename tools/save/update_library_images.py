# -*- coding: utf-8 -*-
import sys
import urllib, urllib2, cookielib
import os, time

from datetime import *  

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import requests



def test():
    html = requests.get('http://www.zhaoonline.com/search/%E8%9F%A0%E9%BE%992%E5%85%83%E6%97%A7%E4%B8%80%E6%9E%9A-8-8-trade-140,141-N-00-N-0-N-1-N-N-N-N-0-42.htm').content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

    tags = soup.find_all('a', class_="item-title")
    for tag in tags:
        print tag['href']
        #print tag.get_text()


    html = requests.get('http://www.zhaoonline.com/qingdaiyoupiao/5166412.shtml').content
    print html
    startLoc = html.find('"picPath":"') + len('"picPath":"')
    endLoc = startLoc + html[startLoc:].find('"')
    print html[startLoc:endLoc]


    startLoc = html.find('"endAt":"') + len('"endAt":"')
    endLoc = startLoc + html[startLoc:].find(' ')
    print html[startLoc:endLoc]

def getAuctionDetails(url):
    html = requests.get(url).content
    startLoc = html.find('"picPath":"') + len('"picPath":"')
    endLoc = startLoc + html[startLoc:].find('"')
    picURL = html[startLoc:endLoc]

    startLoc = html.find('"endAt":"') + len('"endAt":"')
    endLoc = startLoc + html[startLoc:].find(' ')
    auctionDate = html[startLoc:endLoc]

    return {'pic': picURL, 'date': auctionDate}

def getAuctionPages(stamp):
    ''' Return the list of auction urls'''
    url = "http://www.zhaoonline.com/search/"
    url += urllib.pathname2url(stamp['base'])
    url += "-8-3-trade-140,141-N-00-N-0-N-1-N-N-N-N-0-"
    auctionList = []
    n = 0
    while True:
        n += 1
        urln = url + str(n) + ".htm"
        html = requests.get(urln).content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        tags = soup.find_all('a', class_="item-title")
        if len(tags) == 0:
            break
        for tag in tags:
            excluded = False
            for exclude in stamp['exclude'].split():
                if tag.get_text().find(exclude) >= 0:
                    excluded = True
            if excluded == True:
                continue
            auctionList.append("http://www.zhaoonline.com/search" + tag['href'])
            #print tag.get_text()
            
    return auctionList

def makePicFileName(picDate, picURL):
    picFileName = picURL.split("/")[-1]
    picFileNameBase = picFileName.split(".")[0]
    nameBaseLen = len(picFileNameBase)
    uniqueNameLen = 12
    for i in range(0, uniqueNameLen - nameBaseLen):
        picFileName = "0" + picFileName
    picFileName = picDate + "_" + picFileName
    return picFileName

def savePicture(picURL, picPath):
    try:
        pic = requests.get(picURL).content
        picFile = open(picPath, "wb")
        picFile.write(pic)
        picFile.close()
        print picPath + '  is saved'                                         
    except Exception, e:
        print e

if __name__ == '__main__':
    stamps = [
        {'folder':'1d/library/mint/src/', 'base':"蟠龙1元新", 'exclude':'石印 元年'},
        {'folder':'1d/library/used/src/', 'base':"蟠龙1元戳", 'exclude':'石印 元年'},
        {'folder':'1d/library/used/src/', 'base':"蟠龙1元旧", 'exclude':'石印 元年'},
        {'folder':'2d/library/mint/src/', 'base':"蟠龙2元新", 'exclude':'石印 元年'},
        {'folder':'2d/library/used/src/', 'base':"蟠龙2元戳", 'exclude':'石印 元年'},
        {'folder':'2d/library/used/src/', 'base':"蟠龙2元旧", 'exclude':'石印 元年'},
        {'folder':'5d/library/mint/src/', 'base':"蟠龙5元新", 'exclude':'石印 元年'},
        {'folder':'5d/library/used/src/', 'base':"蟠龙5元戳", 'exclude':'石印 元年'},
        {'folder':'5d/library/used/src/', 'base':"蟠龙5元旧", 'exclude':'石印 元年'},
    ]

    #test()
    
    for stamp in stamps:
        auctionList = getAuctionPages(stamp)
        for auction in auctionList:
            auctionDetail = getAuctionDetails(auction)
            print auctionDetail['date'] + ' : ' + auctionDetail['pic']
            picFileName = makePicFileName(auctionDetail['date'], auctionDetail['pic'])
            picFilePath = '../' + stamp['folder'] + picFileName
            if os.path.exists(picFilePath):
                print picFileName + '  exists'
            else:
                savePicture(auctionDetail['pic'], picFilePath)
                        
