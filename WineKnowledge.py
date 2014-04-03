__author__ = 'jing'

import urllib2
from sgmllib import SGMLParser
from Queue import Queue
import time
import threading
import thread
import codecs


class KnowledgeLinkParser(SGMLParser):

    def reset(self):
        SGMLParser.reset(self)
        self.is_div = 0

    def start_div(self, attrs):
        for k, v in attrs:
            if (k, v) == ('id', 'post_list_more'):
                self.is_div = 1

    def end_div(self):
        self.is_div = 0

    def start_a(self, attrs):
        for k, v in attrs:
            if self.is_div == 1 and k == 'href':
                if knowledgeLock.acquire():
                    knowledgeLinkQueue.put(v)
                knowledgeLock.release()


class KnowledgeContentParser(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)
        self.template = '"title": "{0}","date":"{1}", "content":"{2}"'
        self.records = []

    def reset(self):
        SGMLParser.reset(self)
        self.is_h2 = 0
        self.is_p = 0
        self.is_remark = 0
        self.is_content = 0
        self.is_em = 0
        self.title = ''
        self.remark = ''
        self.contents = []

    def start_h2(self, attrs):
        self.is_h2 = 1
        self.is_remark = 1

    def end_h2(self):
        self.is_h2 = 0

    def start_p(self, attrs):
        self.is_p = 1

    def end_p(self):
        self.is_p = 0

    def start_a(self, attrs):
        self.is_remark = 0

    def start_em(self, attrs):
        self.is_em = 1

    def start_div(self, attrs):
        for k, v in attrs:
            if (k, v) == ('class', 'single_content'):
                self.is_content = 1
            if (k, v) == ('id', "divleft"):
                self.is_content = 0
                self.is_em = 0

    def handle_data(self, data):
        if self.is_em and self.is_h2 == 1:
            self.title = data
        if self.is_em and self.is_p == 1 and self.is_remark:
            self.remark = data
        if self.is_em and self.is_p == 1 and self.is_content == 1:
            self.contents.append(data)

    def summarize(self):
        if isinstance(self.title, unicode):
            recordTitle = self.title
        else:
            recordTitle = unicode(self.title, 'utf-8')
        if isinstance(self.remark, unicode):
            recordRemark = self.remark.split('|')[0]
        else:
            recordRemark = unicode(self.remark.split('|')[0], 'utf-8')
        if len(self.contents) > 0:
            if isinstance(self.contents[0], unicode):
                recordContent = '\n'.join(self.contents)
            else:
                recordContent = unicode(''.join(self.contents), 'utf-8')
            record = '"title": "' + recordTitle + '", "date": "' + recordRemark + '", "content": "' + recordContent + '"'
            self.records.append(record)
        self.title = ''
        self.remark = ''
        self.contents = []


class BrandLinkParser(SGMLParser):

    def reset(self):
        SGMLParser.reset(self)
        self.is_div = 0

    def start_div(self, attrs):
        for k, v in attrs:
            if (k, v) == ('id', 'post_list_more'):
                self.is_div = 1

    def end_div(self):
        self.is_div = 0

    def start_a(self, attrs):
        for k, v in attrs:
            if self.is_div == 1 and k == 'href':
                if brandLock.acquire():
                    brandLinkQueue.put(v)
                brandLock.release()


class BrandContentParser(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)
        self.template = '"title": "{0}","date":"{1}", "content":"{2}"'
        self.records = []

    def reset(self):
        SGMLParser.reset(self)
        self.is_h2 = 0
        self.is_p = 0
        self.is_remark = 0
        self.is_content = 0
        self.is_em = 0
        self.title = ''
        self.remark = ''
        self.contents = []

    def start_h2(self, attrs):
        self.is_h2 = 1
        self.is_remark = 1

    def end_h2(self):
        self.is_h2 = 0

    def start_p(self, attrs):
        self.is_p = 1

    def end_p(self):
        self.is_p = 0

    def start_a(self, attrs):
        self.is_remark = 0

    def start_em(self, attrs):
        self.is_em = 1

    def start_div(self, attrs):
        for k, v in attrs:
            if (k, v) == ('class', 'single_content'):
                self.is_content = 1
            if (k, v) == ('id', "divleft"):
                self.is_content = 0
                self.is_em = 0

    def handle_data(self, data):
        if self.is_em and self.is_h2 == 1:
            self.title = data
        if self.is_em and self.is_p == 1 and self.is_remark:
            self.remark = data
        if self.is_em and self.is_p == 1 and self.is_content == 1:
            self.contents.append(data)

    def summarize(self):
        if isinstance(self.title, unicode):
            recordTitle = self.title
        else:
            recordTitle = unicode(self.title, 'utf-8')
        if isinstance(self.remark, unicode):
            recordRemark = self.remark.split('|')[0]
        else:
            recordRemark = unicode(self.remark.split('|')[0], 'utf-8')
        if len(self.contents) > 0:
            if isinstance(self.contents[0], unicode):
                recordContent = '\n'.join(self.contents)
            else:
                recordContent = unicode(''.join(self.contents), 'utf-8')
            record = '"title": "' + recordTitle + '", "date": "' + recordRemark + '", "content": "' + recordContent + '"'
            self.records.append(record)
        self.title = ''
        self.remark = ''
        self.contents = []


def loadKnowledgeLink(url, parser):
    pageNum = 1
    global knowledgeLastPage
    while not knowledgeLastPage:
        actualUrl = url + str(pageNum)
        req = urllib2.Request(actualUrl, headers=header)
        try:
            response = urllib2.urlopen(req)
            topPage = response.read()
            parser.feed(topPage)
            pageNum += 1
        except urllib2.HTTPError, e:
            if hasattr(e, 'code') and e.code == 404:
                knowledgeLastPage = True


def loadBrandLink(url, parser):
    pageNum = 1
    global brandLastPage
    while not brandLastPage:
        actualUrl = url + str(pageNum)
        req = urllib2.Request(actualUrl, headers=header)
        try:
            response = urllib2.urlopen(req)
            topPage = response.read()
            parser.feed(topPage)
            pageNum += 1
        except urllib2.HTTPError, e:
            if hasattr(e, 'code') and e.code == 404:
                brandLastPage = True


def loadKnowledgeContent(parser):
    global knowledgeLinkQueue
    global thread1Running
    while not knowledgeLastPage or not knowledgeLinkQueue.empty():
        if knowledgeLinkQueue.empty():
            time.sleep(2)
        else:
            if knowledgeLock.acquire():
                detailUrl = knowledgeLinkQueue.get()
            knowledgeLock.release()
            req = urllib2.Request(detailUrl, headers=header)
            try:
                response = urllib2.urlopen(req)
                text = response.read()
                print detailUrl
                parser.feed(text)
                parser.summarize()
            except urllib2.HTTPError, e:
                if hasattr(e, 'reason'):
                    print 'url: ' + detailUrl + " not reachable. Reason: " + e.reason
            except AttributeError, e:
                print e.message
                continue
    thread1Running = False


def loadBrandContent(parser):
    global brandLinkQueue
    global thread2Running
    while not brandLastPage or not brandLinkQueue.empty():
        if brandLinkQueue.empty():
            time.sleep(2)
        else:
            if brandLock.acquire():
                detailUrl = brandLinkQueue.get()
            brandLock.release()
            req = urllib2.Request(detailUrl, headers=header)
            try:
                response = urllib2.urlopen(req)
                content = response.read()
                parser.feed(content)
                parser.summarize()
            except urllib2.HTTPError, e:
                if hasattr(e, 'reason'):
                    print 'url: ' + detailUrl + " not reachable. Reason: " + e.reason
    thread2Running = False


def appendFile(content, filename):
    fileHandler = open(filename, 'a')
    fileHandler.write(content)
    fileHandler.close()

knowledgeParser = KnowledgeLinkParser()
knowledgeContentParser = KnowledgeContentParser()
brandLinkParser = BrandLinkParser()
brandContentParser = BrandContentParser()
knowledgeLinkQueue = Queue()
brandLinkQueue = Queue()
knowledgeLastPage = False
brandLastPage = False
knowledgeLock = thread.allocate_lock()
brandLock = thread.allocate_lock()
thread1Running = True
thread2Running = True
seedUrl1 = 'http://www.ncvop.com/post/category/wine-knowledge/page/'
seedUrl2 = "http://www.ncvop.com/post/category/wine-brands/page/"
header = {"UserAgent": "Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0"}
thread.start_new_thread(loadKnowledgeLink, (seedUrl1, knowledgeParser))
time.sleep(1)
thread.start_new_thread(loadKnowledgeContent, (knowledgeContentParser,))
thread.start_new_thread(loadBrandLink, (seedUrl2, brandLinkParser))
thread.start_new_thread(loadBrandContent, (brandContentParser,))
# time.sleep(1)
# while threading.activeCount() != 1:
#     time.sleep(10)
# time.sleep(5)
while thread1Running:
    time.sleep(10)
with codecs.open("/home/jing/data/knowledge.txt", "a", 'utf-8') as knowledgeFile:
    for record in knowledgeContentParser.records:
        knowledgeFile.write(record)
        knowledgeFile.write('\n')
with codecs.open('/home/jing/data/brand.txt','a','utf-8') as brandFile:
    for record in brandContentParser.records:
        brandFile.write(record)
        brandFile.write('\n')
# print brandLinkQueue.qsize()
# url = 'http://www.ncvop.com/post/682.html'
# req = urllib2.Request(url, headers=header)
# response = urllib2.urlopen(req)
# s = '\xe8\x91\xa1\xe8\x90\x84\xe9\x85\x92\xe4\xb8\x8e\xe9\xa3\x9f\xe7\x89\xa9\xe7\x9a\x84\xe6\x90\xad\xe9\x85\x8d\xe5\x8e\x9f\xe5\x88\x99'
# y=u'abc | cde'
# print type(s)
# print y.split("|")[0]
# print type(unicode(s, 'utf-8'))
# print isinstance(response.read(), unicode)
# knowledgeContentParser.feed(response.read())
# print knowledgeContentParser.title
# print knowledgeContentParser.remark
# knowledgeContentParser.summarize()
# print knowledgeContentParser.records
# for content in knowledgeContentParser.contents:
#     print content