# -*- coding: utf-8 -*-
import sys
from HTMLParser import HTMLParser
import urllib, urllib2, cookielib
import os, time
import xml.dom.minidom

from datetime import *  
#import locale
from decimal import Decimal
from re import sub

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# get history list
# get number of pages
# go through each page
# go through each item in page
# get the detail of each item
# analyze information of the item, title, comments, date, price, last prizing


# search list:
# text format:
# name, catalog\n

# search result:
# xml format:
# <history><item><id><name><comments><quality><date><price>

class HtmlDownloader():
    offLine = False
    headers = {'Host': 'www.zhaoonline.com',
               'Connection': 'keep-alive',
               'Content-Length': '50',
               'Accept': '*/*',
               'Origin': 'www.zhaoonline.com',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Referer': 'http://www.zhaoonline.com/',
               #'Accept-Encoding': 'gzip,deflate,sdch',
               #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'}
    login_data = None

    def __init__(self, user, passwd):
        # initialize the opener, cookie
        if user != None and passwd != None:
            self.login_data = urllib.urlencode({'loginId': user, 'password': passwd, 'back': 'index'})
        else:
            # offline mode
            self.offLine = True
            print "Warning: username/passwd not provided, working in offline mode"
            return

        try:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            host_url = r'http://www.zhaoonline.com/'
            login_url = r'http://www.zhaoonline.com/login/submit.shtml'
            h = urllib2.urlopen(host_url)
            request = urllib2.Request(login_url, self.login_data, self.headers)
            response = urllib2.urlopen(request)  
            response.read()
        except Exception, e:
            self.offLine = True
            print "Warning: network not available, working in offline mode"

    def isOffLine(self):
        return self.offLine

    def getHtml(self, url):
        #print "downloading file: " + url
        request = urllib2.Request(url, self.login_data, self.headers)
        try:
            response = urllib2.urlopen(request)  
            html = response.read()
        except Exception, e:
            html = None
        return html
    
    def downLoad(self, url):
        #print "downloading file: " + url
        #request = urllib2.Request(url, self.login_data, self.headers)
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request)  
            downloaded = response.read()
        except Exception, e:
            print e
            downloaded = None
        return downloaded


class HistoryItemListParser(HTMLParser):
    historyItems = [] #HistoryItem[]
    html = None
    inCenterList = False
    currentPage = -1
    totalPage = 0
    itemsFoundInCurrentPage = 1

    def __init__(self):
        HTMLParser.__init__(self)
        self.historyItems = []
        self.html = None
        self.inCenterList = False
        self.currentPage = -1
        self.totalPage = 1

    def clean(self):
        self.historyItems = []
        self.html = None
        self.inCenterList = False
        self.currentPage = -1
        self.totalPage = 0
    
    def parse(self, html):
        try:
            self.itemsFoundInCurrentPage = 0
            self.feed(html)
            return True
        except Exception, e:
            print e
            return False


    def handle_starttag(self,tag,attrs):
        if self.inCenterList == True and tag == "a" and len(attrs) == 4 and attrs[2][0] == 'href':
            item = HistoryItem()
            item.ref = attrs[2][1]
            item.name = attrs[1][1]
            self.historyItems.append(item)
            self.itemsFoundInCurrentPage += 1 
        elif tag == "div" and len(attrs) == 2 and attrs[1] == ('id', 'center_list_id'):
            self.inCenterList = True
        elif tag == 'input' and len(attrs) == 4 and attrs[3] == ('id', 'totalPage'):
            self.totalPage = int(attrs[2][1])
        elif tag == 'input' and len(attrs) == 4 and attrs[3] == ('id', 'currentPage'):
            self.currentPage = int(attrs[2][1])

    def hasNextPage(self, page):
        return page <= self.totalPage

    def getHistoryItemList(self):
        return self.historyItems

class HistoryItemParser(HTMLParser):
    historyItem = None
    parsingID = False
    parsingName = False
    parsingDatePre = False
    parsingDate = False
    parsingComments = False
    parsingQuality = False
    parsingPrice = False
    parsingAuction = False

    def __init__(self):
        HTMLParser.__init__(self)
        self.historyItem = HistoryItem()

    def parse(self, html):
        self.feed(html)

    def handle_starttag(self,tag,attrs):
        if tag == "div" and len(attrs) > 0 and attrs[0] == ('class', 'Id'):
            self.parsingID = True
        elif tag == "span" and len(attrs) > 0 and attrs[0] == ('class', 'name'):
            self.parsingName = True
        elif tag == "p" and len(attrs) > 0 and attrs[0] == ('class', 'time'):
            self.parsingDatePre = True
        elif self.parsingDatePre == True and tag == "span":
            self.parsingDatePre = False
            self.parsingDate = True
        elif tag == "span" and len(attrs) > 0 and attrs[0] == ('id', 'character') and attrs[1] == ('class', 'character'):
            self.parsingQuality = True
        elif tag == "p" and len(attrs) > 0 and attrs[0] == ('class', 'currentPrice'):
            self.parsingPrice = True
        elif tag == "div" and len(attrs) > 0 and attrs[0] == ('class', 'description'):
            self.parsingComments = True
        elif tag == "script" and len(attrs) > 0 and attrs[0] == ('type', 'text/javascript'):
            self.parsingAuction = True

    def handle_data(self, data):
        if self.parsingID == True:
            self.historyItem.id = data
            self.parsingID = False
        elif self.parsingName == True:
            self.historyItem.name = data
            self.parsingName = False
        elif self.parsingDate == True:
            self.historyItem.date = data
            self.parsingDate = False
        elif self.parsingComments == True:
            self.historyItem.comments = data
            self.parsingComments = False
        elif self.parsingQuality == True:
            self.historyItem.quality = data
            self.parsingQuality = False
        elif self.parsingPrice == True:
            self.historyItem.price = data
            self.parsingPrice = False
        elif self.parsingAuction == True:
            if str(data).find('var auction = ') >= 0:
                (self.historyItem.auctionText, self.historyItem.auctionData) = self.parseRawAuctionData(data)
            self.parsingAuction = False


    def findAuctionBlock(self, text):
        # print "findAuctionBlock(): text = "
        # print text
        remainingBrackets = []
        blockText = ""
        for c in text:
            blockText += c
            if c == "{":
                remainingBrackets.append("}")
            elif c == "[":
                remainingBrackets.append("]")
            elif c == "]":
                if remainingBrackets[len(remainingBrackets)-1] == c:
                    del remainingBrackets[len(remainingBrackets)-1]
                    if len(remainingBrackets) == 0:
                        break
                else:
                    print "bracket [] mismatch"
                    return ""
            elif c == "}":
                if remainingBrackets[len(remainingBrackets)-1] == c:
                    del remainingBrackets[len(remainingBrackets)-1]
                    if len(remainingBrackets) == 0:
                        break
                else:
                    print "brackets {} mismatch"
                    return ""
        # print "findAuctionBlock(): return = "
        # print blockText[1:len(blockText)-1]
        return blockText[1:len(blockText)-1]
            

    def buildAuctionList(self, text):
        li = []
        i = 0
        while(i < len(text)):
            c = text[i]
            if c == "{":
                blockText = self.findAuctionBlock(text[i:])
                blockDic = self.buildAuctionDic(blockText)
                li.append(blockDic)
                i += len(blockText) + 1
            i += 1
        return li
                

    def buildAuctionDic(self, text):
        dic = {}
        findingKey = True
        findingValue = False
        key = ""
        value = ""
        i = 0
        quoting = False
        while(i < len(text)):
            c = text[i]
            if c == '"':
                if quoting == False:
                    quoting = True
                else:
                    quoting = False
            elif quoting == True:
                if findingValue == True:
                    value += c
                else:
                    key += c
            elif c == ":":
                findingKey = False
                findingValue = True
            elif c == ",":
                findingKey = True
                findingValue = False
#                print "key: \n" + str(key)
#                print "value: \n" + str(value)
                dic.update({key:value})
                key = ""
                value = ""
            elif c == "{":
                blockText = self.findAuctionBlock(text[i:])
                blockDic = self.buildAuctionDic(blockText)
                if findingValue == True:
                    value = blockDic
                else:
                    key = blockDic
                i += len(blockText) + 1
            elif c == "[":
                listText = self.findAuctionBlock(text[i:])
                blockList = self.buildAuctionList(listText)
                if findingValue == True:
                    value = blockList
                else:
                    key = blockList
                i += len(listText) + 1
            else:
                if findingValue == True:
                    value += c
                else:
                    key += c
            i += 1
        return dic

    def parseRawAuctionData(self, auction):
        auctionText = auction
        auctionText = auctionText[str(auctionText).find('var auction'):]
        auctionText = auctionText[str(auctionText).find('{'):]
        pureAuctionText = self.findAuctionBlock(auctionText)
        #print "#########################"
        #print pureAuctionText
        #print "#########################"
        dic = self.buildAuctionDic(pureAuctionText)
        return (pureAuctionText, dic)

    def parsePureAuctionData(self, pureAuctionText):
        dic = self.buildAuctionDic(pureAuctionText)
        return (pureAuctionText, dic)


    def getHistoryItem(self):
        return self.historyItem


categoryDic = {
    '清代邮票' : 140,
    '民国邮票' : 141,
    '纪特邮票' : 146,
    '文革邮票' : 171,
    '编号邮票' : 172,
    'JT邮票'   : 173,
    '散票'     : 178, 
}

class SearchCondition:
    base = ""
    category = []
    includes = []
    excludes = []
    folder = ""
    alias = ""
    description = ""

    def __init__(self, base, category, includes, excludes, folder, alias, description):
        self.base = base
        self.category = category
        self.includes = includes
        self.excludes = excludes
        self.folder = folder
        self.alias = alias
        self.description = description

    def toString(self):
        return self.base + " : " + self.alias

searchConditions = [
    SearchCondition("蟠龙1元新", ["清代邮票", "民国邮票"], ["蟠龙1元"], ["石印"], "coiling_dragon_1d_mint", "1dm", "大清蟠龙邮票 壹圆新票"),
    SearchCondition("蟠龙1元旧", ["清代邮票", "民国邮票"], ["蟠龙1元"], ["石印"], "coiling_dragon_1d_used", "1du", "大清蟠龙邮票 壹圆旧票"),
    SearchCondition("蟠龙2元新", ["清代邮票", "民国邮票"], ["蟠龙2元"], ["石印"], "coiling_dragon_2d_mint", "2dm", "大清蟠龙邮票 贰圆新票"),
    SearchCondition("蟠龙2元旧", ["清代邮票", "民国邮票"], ["蟠龙2元"], ["石印"], "coiling_dragon_2d_used", "2du", "大清蟠龙邮票 贰圆旧票"),
    SearchCondition("蟠龙5元新", ["清代邮票", "民国邮票"], ["蟠龙5元"], ["石印"], "coiling_dragon_5d_mint", "5dm", "大清蟠龙邮票 伍圆新票"),
    SearchCondition("蟠龙5元旧", ["清代邮票", "民国邮票"], ["蟠龙5元"], ["石印"], "coiling_dragon_5d_used", "5du", "大清蟠龙邮票 伍圆旧票"),
    ]

class HistoryItem():
    ref = ""
    id = ""
    name = ""
    quality = ""
    comments = ""
    date = 0
    price = 0
    auctionText = ""
    auctionData = None

class SearchItem():
    condition = None
    historyItems = [] #HistoryItem[]

class SearchData():
    searchItems = [] #SearchItem[]

class DataHandler():
    searchData = None
    downloader = None
    failureList = []

    def __init__(self, user, passwd):
        self.searchData = SearchData()
        self.downloader = HtmlDownloader(user, passwd)
    
    def isOffLine(self):
        return self.downloader.isOffLine()

    def download(self, url):
        return self.downloader.downLoad(url)

    def printLog(self):
        print "failure records: "
        for failure in self.failureList:
            print "  " + failure
        self.failureList = []
        
    def addSearchItem(self, condition):
        newItem = SearchItem()
        newItem.condition = condition
        for item in self.searchData.searchItems:
            if cmp (newItem.condition.alias, item.condition.alias) == 0 or (cmp(newItem.condition.base, item.condition.base) == 0):
                print "exist"
                return item
        self.searchData.searchItems.append(newItem)
        return newItem

    def getSearchItemURL(self, searchItem, page):
        url = "http://www.zhaoonline.com/search/"
        url += urllib.pathname2url(searchItem.condition.base)
        url += "-8-3-trade-"
        categoryStr = ""
        for category in searchItem.condition.category:
            if categoryStr == "":
                categoryStr = urllib.pathname2url(str(categoryDic[category]))
            else:
                categoryStr += urllib.pathname2url(",")
                categoryStr += urllib.pathname2url(str(categoryDic[category]))
        if categoryStr == "":
            categoryStr = urllib.pathname2url("N")
        url += categoryStr
        url += "-N-00-N-0-N-1-N-N-N-N-8-"
        url += str(page)
        url += ".htm"
        return  url

    def getHistoryItemURL(self, ref):
        url = "http://www.zhaoonline.com"
        url += ref
        return url

    def updateSearchItem(self, searchItem):
        page = 1
        historyItemListParser = HistoryItemListParser()
        while historyItemListParser.hasNextPage(page):
            url = self.getSearchItemURL(searchItem, page)
            print "parsing search list: " + url
            html = self.downloader.getHtml(url)
            if html == None:
                break
            if historyItemListParser.parse(html) == False:
                self.failureList.append(url)
            # save the tmp file to debug
            self.saveToListFile(searchItem.condition.base+"_"+str(page), html)
            page += 1
        historyItemList = historyItemListParser.getHistoryItemList()
        historyItemListParser.clean()  
        searchItem.historyItems = []
        for historyItem in historyItemList:
            passed = False
            for inc in searchItem.condition.includes:
                if historyItem.name.find(inc) < 0:
                    passed = True
                    break
            for exc in searchItem.condition.excludes:
                if historyItem.name.find(exc) >= 0:
                    passed = True
                    break
            if passed == True:
                continue
            else:
                searchItem.historyItems.append(historyItem)
        # now every HistoryItem has id only
        for i in range(0, len(searchItem.historyItems)):
            historyItem = searchItem.historyItems[i]
            url = self.getHistoryItemURL(historyItem.ref)
            print "(" + str(i) + "/" + str(len(searchItem.historyItems))+ ") downloading page: " + url
            html = self.downloader.getHtml(url)
            if html == None:
                continue
            historyItemParser = HistoryItemParser()
            historyItemParser.parse(html)
            tmpItem = historyItemParser.getHistoryItem()
            #historyItem.ref = tmpItem.ref
            historyItem.id = tmpItem.id
            historyItem.name = tmpItem.name
            historyItem.comments = tmpItem.comments
            historyItem.quality = tmpItem.quality
            historyItem.date = tmpItem.date
            historyItem.price = tmpItem.price
            historyItem.auctionText = tmpItem.auctionText
            historyItem.auctionData = tmpItem.auctionData
            # save the html content to tmp directory
            # self.saveToTmpFile(historyItem, html)
        return

    def loadAllSearchItemsFromXml(self):
        searchResultXmlLoader = SearchResultXmlLoader()
        self.searchData = searchResultXmlLoader.loadAllXmlFiles()
        # debug
        #for searchItem in self.searchData.searchItems:
        #    self.dumpSearchItem(searchItem)
        return

    def saveAllSearchItemsToXml(self):
        for searchItem in self.searchData.searchItems:
            self.saveSearchItemToXml(searchItem)
        return

    def saveSearchItemToXml(self, searchItem):
        searchResultXmlGenerator = SearchResultXmlGenerator(searchItem)
        searchResultXmlGenerator.generateXml()
        return

    def getSearchItemByAlias(self, alias):
        if alias == None:
            return None
        for searchItem in self.searchData.searchItems:
            if cmp(searchItem.condition.alias, alias) == 0:
                return searchItem
        return None

    def getAllSearchItems(self):
        return self.searchData.searchItems

    def saveToTmpFile(self, historyItem, html):
        fileName = 'debug/' + historyItem.id + ".shtml"
        f = open(fileName, 'w')
        f.write(html)
        f.close()

    def saveToListFile(self, name, html):
        fileName = 'debug/' + name + ".html"
        f= open(fileName, 'w')
        f.write(html)
        f.close()
        
    # debug function
    def dumpSearchItem(self, searchItem):
        print "Dumping SearchItem: " + searchItem.name
        print "  alias: " + searchItem.alias
        print "  category: " + searchItem.category
        print "  quality: " + searchItem.quality
        for historyItem in searchItem.historyItems:
            print "    name =     " + historyItem.name
            print "    comments = " + historyItem.comments


class SearchResultXmlLoader():

    def __init__(self):
        return

    def loadXmlFile(self, file):
        searchItem = SearchItem()
        doc = xml.dom.minidom.parse(file)
        searchResult = doc.documentElement
        searchItem.alias = searchResult.getElementsByTagName("Alias")[0].childNodes[0].nodeValue#.encode("utf-8")
        searchItem.name = searchResult.getElementsByTagName("Keyword")[0].childNodes[0].nodeValue#.encode("utf-8")
        searchItem.category = searchResult.getElementsByTagName("Category")[0].childNodes[0].nodeValue#.encode("utf-8")
        searchItem.quality = searchResult.getElementsByTagName("Quality")[0].childNodes[0].nodeValue#.encode("utf-8")
        items = searchResult.getElementsByTagName("ItemList")[0].childNodes
        for item in items:
            print item
            try:
                historyItem = HistoryItem()
                historyItem.ref = item.getElementsByTagName("Ref")[0].childNodes[0].nodeValue#.encode("utf-8")
                #print historyItem.ref
                historyItem.id = item.getElementsByTagName("ID")[0].childNodes[0].nodeValue#.encode("utf-8")
                #print historyItem.id
                historyItem.name = item.getElementsByTagName("Name")[0].childNodes[0].nodeValue#.encode("utf-8")
                #print historyItem.name
                historyItem.quality = item.getElementsByTagName("Quality")[0].childNodes[0].nodeValue#.encode("utf-8")
                #print historyItem.quality
                historyItem.comments = item.getElementsByTagName("Comments")[0].childNodes[0].nodeValue#.encode("utf-8")
                #print historyItem.comments
                historyItem.date = item.getElementsByTagName("Date")[0].childNodes[0].nodeValue#.encode("utf-8")
                #print historyItem.date
                historyItem.price = item.getElementsByTagName("Price")[0].childNodes[0].nodeValue#.encode("utf-8")
                #print historyItem.price
                historyItem.auctionText = item.getElementsByTagName("Auction")[0].childNodes[0].nodeValue#.encode("utf-8")
                #print historyItem.auctionText
                #historyItemParser = HistoryItemParser()
                #(xxx, historyItem.auctionData) = historyItemParser.parsePureAuctionData(historyItem.auctionText)

                searchItem.historyItems.append(historyItem)
            except Exception, e:
                #print e
                continue

        return searchItem

    def loadAllXmlFiles(self):
        searchData = SearchData()
        fileNames = os.listdir('data/')
        for fileName in fileNames:
            fileName = 'data/' + fileName
            if os.path.isfile(fileName):
                fileNameBase, fileNameExt = os.path.splitext(fileName)
                if cmp(fileNameExt, '.xml') == 0:
                    print "loading file: " + fileName
                    searchItem = self.loadXmlFile(fileName)
                    searchData.searchItems.append(searchItem)
        return searchData


class SearchResultXmlGenerator():
    dom = None
    root = None
    itemList = None
    searchItem = None

    def __init__(self, searchItem):
        self.searchItem = searchItem
        impl = xml.dom.minidom.getDOMImplementation()
        self.dom = impl.createDocument(None, 'SearchResult', None)
        self.root = self.dom.documentElement 
        return
        
    def setAlias(self, aliasText):
        alias = self.dom.createElement('Alias')
        aliasValue = self.dom.createTextNode(aliasText)
        alias.appendChild(aliasValue)
        self.root.appendChild(alias)

    def setKeyword(self, keywordText):
        keyword = self.dom.createElement('Keyword')
        keywordValue = self.dom.createTextNode(keywordText)
        keyword.appendChild(keywordValue)
        self.root.appendChild(keyword)

    def setCategory(self, categoryText):
        category = self.dom.createElement('Category')
        categoryValue = self.dom.createTextNode(categoryText)
        category.appendChild(categoryValue)
        self.root.appendChild(category)

    def setQuality(self, qualityText):
        quality = self.dom.createElement('Quality')
        qualityValue = self.dom.createTextNode(qualityText)
        quality.appendChild(qualityValue)
        self.root.appendChild(quality)

    def addHistoryItem(self, historyItem):
        item = self.dom.createElement('Item')

        tag = self.dom.createElement('Ref')
        value = self.dom.createTextNode(historyItem.ref)
        tag.appendChild(value)
        item.appendChild(tag)

        tag = self.dom.createElement('ID')
        value = self.dom.createTextNode(historyItem.id)
        tag.appendChild(value)
        item.appendChild(tag)

        tag = self.dom.createElement('Name')
        value = self.dom.createTextNode(historyItem.name)
        tag.appendChild(value)
        item.appendChild(tag)

        tag = self.dom.createElement('Quality')
        value = self.dom.createTextNode(historyItem.quality)
        tag.appendChild(value)
        item.appendChild(tag)

        tag = self.dom.createElement('Comments')
        value = self.dom.createTextNode(historyItem.comments)
        tag.appendChild(value)
        item.appendChild(tag)

        tag = self.dom.createElement('Date')
        value = self.dom.createTextNode(str(historyItem.date))
        tag.appendChild(value)
        item.appendChild(tag)

        tag = self.dom.createElement('Price')
        value = self.dom.createTextNode(str(historyItem.price))
        tag.appendChild(value)
        item.appendChild(tag)

        tag = self.dom.createElement('Auction')
        value = self.dom.createTextNode(str(historyItem.auctionText))
        tag.appendChild(value)
        item.appendChild(tag)

        if self.itemList == None:
            self.itemList = self.dom.createElement('ItemList')
            self.root.appendChild(self.itemList)
        self.itemList.appendChild(item)

    def writeToFile(self):
        f= open("data/" + self.searchItem.name + "_" + self.searchItem.category + "_" + self.searchItem.quality + ".xml", 'w')
        self.dom.writexml(f, addindent='  ', newl='\n',encoding='utf-8')
        f.close() 

    def generateXml(self):
        self.setAlias(self.searchItem.alias)
        self.setKeyword(self.searchItem.name)
        self.setCategory(self.searchItem.category)
        self.setQuality(self.searchItem.quality)
#.decode("utf-8").encode("GBK"))
#.decode("GBK").encode("utf-8"))
        for item in self.searchItem.historyItems:
            self.addHistoryItem(item)
        self.writeToFile()

def doCommandUpdate(alias, dataHandler):
    if True:
        if True:
            if True:
                if alias == 'all':
                    searchItems = dataHandler.getAllSearchItems()
                    for searchItem in searchItems:
                        print "updating searchItem: " + searchItem.condition.toString().decode("utf-8")
                        dataHandler.updateSearchItem(searchItem)
                        # debug
                        #dataHandler.dumpSearchItem(searchItem)
                    dataHandler.printLog()
                else:
                    searchItem = dataHandler.getSearchItemByAlias(alias)
                    if searchItem == None:
                        print "ERROR: can't find alias: " + alias
                    else:
                        print "updating searchItem: " + searchItem.condition.toString().decode("utf-8")
                        dataHandler.updateSearchItem(searchItem)
                    dataHandler.printLog()
    return

def doCommandDownload(alias, dataHandler):
    if True:
        if True:
            if True:
                if alias == 'all':
                    searchItems = dataHandler.getAllSearchItems()
                else:
                    searchItems = [dataHandler.getSearchItemByAlias(alias)]
                downloadList = []
                for searchItem in searchItems:
                    if searchItem == None:
                        print "ERROR: can't find alias: " + alias
                    else:
                        historyItems = sorted(searchItem.historyItems, key=lambda x: x.date)
                                                # make category dir
                        dirName = searchItem.condition.folder
                        if os.path.exists(dirName) == False:
                            os.mkdir(dirName)
                        elif os.path.isdir(dirName) == False:
                            print '"' + dirName + '" file exist, remove it'
                            continue
                        # make sub dir
                        subDirNames = ["src", "m_size"]
                        for subDirName in subDirNames:
                            subDir = dirName + "/" + subDirName
                            if os.path.exists(subDir) == False:
                                os.mkdir(subDir)
                            elif os.path.isdir(subDir) == False:
                                print '"' + subDir + '" file exist, remove it'
                            continue
                            
                        # build download list at first
                        for historyItem in historyItems:
                            dt = datetime.strptime(historyItem.date, "%Y-%m-%d %H:%M:%S")
                            historyItemParser = HistoryItemParser()
                            (xxx, historyItem.auctionData) = historyItemParser.parsePureAuctionData(historyItem.auctionText)
                            #print historyItem.auctionData
                            pictureDatas = historyItem.auctionData.get("pictures")
                            for pictureData in pictureDatas:
                                keys = subDirNames
                                for key in keys:
                                    picURL = pictureData.get(key)
                                    if picURL <> None:
                                        nameLen = len(picURL.split("/")[-1].split(".")[0])
                                        picFileName = searchItem.condition.folder + "/" + key + "/" 
                                        picFileName = picFileName + dt.strftime("%Y-%m-%d") + "_"
                                        uniqueNameLen = 0
                                        if (key == "src"):
                                            uniqueNameLen = 12
                                        elif (key == "m_size"):
                                            uniqueNameLen = 12
                                        else:
                                            print "ERROR"
                                            continue
                                        for i in range(0, uniqueNameLen - nameLen):
                                            picFileName = picFileName + "0"
                                        picFileName = picFileName + picURL.split("/")[-1]
                                        if picFileName.find('!') > 0:
                                            picFileName = picFileName[:picFileName.find('!')]
                                        if os.path.exists(picFileName) == False:
                                            downloadList.append([picURL, picFileName])
                # then download image one by one
                for i in range(0, len(downloadList)):
                    picURL = downloadList[i][0]
                    picFileName = downloadList[i][1]
                    try:
                        print "(" + str(i) + "/" + str(len(downloadList))+ ") downloading image: " + picURL
                        pic = dataHandler.download(picURL)
                        if pic <> None:
                            picFile = open(picFileName, "wb")
                            picFile.write(pic)
                            picFile.close()
                    except Exception, e:
                        print e
                        continue
    return

if __name__ == '__main__':
    user = None
    passwd = None
    if len(sys.argv) == 1:
        # offline mode
        user = None
        passwd = None
    elif len(sys.argv) == 3:
        user = sys.argv[1]
        passwd = sys.argv[2]
    else:
        print "ERROR: wrong count of parameter"
        print "Usage: "
        print "  python analyzer.py <user name> <password>"
        print "or offline mode: "
        print "  python analyzer.py"

    dataHandler = DataHandler(user, passwd)
    for searchConditon in searchConditions:
        dataHandler.addSearchItem(searchConditon)
    quitCommand = False
    while quitCommand == False:
        command = raw_input("[image downloader] ")
        parameters = command.split(' ', 4)
        if parameters[0] == "q" or parameters[0] == "quit" or parameters[0] == "exit":
            quitCommand = True
        elif parameters[0] == "list" or parameters[0] == "l":
            searchItems = dataHandler.getAllSearchItems()
            for searchItem in searchItems:
                print searchItem.condition.toString().decode("utf-8")
        
        elif parameters[0] == "download" or parameters[0] == "d":
            # format: download <alias>
            if len(parameters) == 2:
                if dataHandler.isOffLine():
                    print "ERROR: offline mode, can't download"
                    continue
                alias = parameters[1]
                doCommandDownload(alias, dataHandler)
            else:
                print "ERROR: wrong count of parameter"

        elif parameters[0] == "u" or parameters[0] == "update":
            # format: update <alias>
            if len(parameters) == 2:
                if dataHandler.isOffLine():
                    print "ERROR: offline mode, can't update"
                    continue
                alias = parameters[1]
                doCommandUpdate(alias, dataHandler)
            else:
                print "ERROR: wrong count of parameter"

        elif parameters[0] == "f" or parameters[0] == "finish":
            # format: finish <alias>
            if len(parameters) == 2:
                if dataHandler.isOffLine():
                    print "ERROR: offline mode, can't update"
                    continue
                alias = parameters[1]
                doCommandUpdate(alias, dataHandler)
                doCommandDownload(alias, dataHandler)
            else:
                print "ERROR: wrong count of parameter"
                
        else:
            print "ERROR: wrong command"



