"""
Author: Shane Yu
Date created: April 13, 2017
Date last modified: April 14, 2017
"""
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import xml.etree.ElementTree as ET
import pprint
import collections
import json
import time


class SportsCrawler(object):
    """
    exec function will create a json file in result/
    """
    def __init__(self):
        self.url = 'http://www.espn.com/espn/rss/news'

    def getResultDict(self):
        resultDict = dict()
        resultDict['item'] = list()

        res = requests.get(self.url)
        tree_root = ET.fromstring(res.content)
        # print(tree_root[0][9][0].text)
        for item in tree_root[0].findall('item'):
            appendDict = collections.OrderedDict()
            appendDict['title'] = item.find('title').text
            appendDict['category'] = 'event'
            appendDict['type'] = 'sports'
            appendDict['channel'] = 'ESPN'
            appendDict['time'] = item.find('pubDate').text
            appendDict['location'] = 'United States'
            appendDict['price'] = 0
            appendDict['image'] = ''
            
            link = item.find('link').text
            appendDict['description'] = self.getDescriptions(link)
            appendDict['link'] = link
            resultDict['item'].append(appendDict)
        # pprint.pprint(self.resultDict)
        return resultDict

    def getDescriptions(self, link):
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        returnStr = ''
        for item in soup.find_all('p')[0:4]:
            returnStr += (item.text + '\n')

        return returnStr

    def dumpToJson(self, resultDict):
        with open('./user_interest_api_server/SportsNews.json', 'w') as wf:
            json.dump(resultDict, wf)

    def exec(self):
        print('==================')
        print('正在爬取體育新聞...')
        print('現在時間： ' + str(datetime.now()))
        writeDict = self.getResultDict()
        self.dumpToJson(writeDict)
        print('體育新聞寫檔完成')


class TechNewsCrawler(object):
    def __init__(self):
        self.url = 'https://www.cnet.com/rss/news/'

    def parseXmlToDict(self):
        resultDict = dict()
        resultDict['item'] = list()

        res = requests.get(self.url)
        tree_root = ET.fromstring(res.content)
        for item in tree_root[0].findall('item'):
            # print(item.find('title').text)
            appendDict = collections.OrderedDict()
            appendDict['title'] = item.find('title').text
            appendDict['category'] = 'event'
            appendDict['type'] = 'tech'
            appendDict['channel'] = 'CNET'
            appendDict['time'] = item.find('pubDate').text
            appendDict['location'] = ''
            appendDict['price'] = 0
            appendDict['image'] = ''
            appendDict['description'] = item.find('description').text
            appendDict['link'] = item.find('link').text
            resultDict['item'].append(appendDict)
        # pprint.pprint(self.resultDict)
        return resultDict

    def dumpToJson(self, resultDict):
        with open('./user_interest_api_server/TechNews.json', 'w') as wf:
            json.dump(resultDict, wf)

    def exec(self):
        print('==================')
        print('正在爬取科技新聞...')
        print('現在時間： ' + str(datetime.now()))
        writeDict = self.parseXmlToDict()
        self.dumpToJson(writeDict)
        print('科技新聞寫檔完成')


class moviesCrawler(object):
    def __init__(self):
        self.url = 'http://www.imdb.com/movies-in-theaters/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2750721702&pf_rd_r=09SYP6Z61W2AAJB86DXA&pf_rd_s=right-2&pf_rd_t=15061&pf_rd_i=homepage&ref_=hm_otw_hd'
        self.baseUrl = 'http://www.imdb.com'

    def parseImdbToDict(self):
        resultDict = dict()
        resultDict['item'] = list()

        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.select('div.list.detail.sub-list'): # 2個 <div class=list detail sub-list>
            for div in item.select('div.list_item'): # <div class=list_item odd> 和 <div class=list_item even>
                appendDict = collections.OrderedDict()
                appendDict['title'] = div.select('h4 > a')[0].text
                appendDict['category'] = 'event'
                appendDict['type'] = 'movies'
                appendDict['channel'] = 'IMDB'
                appendDict['time'] = ''
                appendDict['location'] = ''
                appendDict['price'] = 0
                appendDict['image'] = div.select('img.poster.shadowed')[0]['src']
                string = div.select('div.outline')[0].text
                appendDict['description'] = string[1:] # delete the first \n charactor
                appendDict['link'] = self.baseUrl + div.select('h4 > a')[0]['href']
                resultDict['item'].append(appendDict)

        return resultDict

    def dumpToJson(self, resultDict):
        with open('./user_interest_api_server/Movies.json', 'w') as wf:
            json.dump(resultDict, wf)

    def exec(self):
        print('==================')
        print('正在爬取電影資訊(IMDB)...')
        print('現在時間： ' + str(datetime.now()))
        writeDict = self.parseImdbToDict()
        self.dumpToJson(writeDict)
        print('電影資訊寫檔完成')



if __name__ == '__main__':
    sportsObj = SportsCrawler()
    sportsObj.exec()
    TechNewsObj = TechNewsCrawler()
    TechNewsObj.exec()
    moviesObj = moviesCrawler()
    moviesObj.exec()
    time.sleep(86400) # sleep for 24 hours
