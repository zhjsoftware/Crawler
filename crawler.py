__author__ = 'jing'

import urllib2
import sys
import os
from sgmllib import SGMLParser

pwd_dir = os.getcwd()

class getList(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.name = []
        self.is_h4 = ''
    def start_h4(self, attrs):
        self.is_h4 = 1
    def end_h4(self):
        self.is_h4 = ''
    def handle_data(self, data):
        if self.is_h4 == 1:
            self.name.append(data)

content = urllib2.urlopen("http://list.taobao.com/browse/cat-0.htm").read()
#listname = getList()
#listname.feed(content)
#for item in listname.name:
#    print item.decode('gbk').encode('utf-8')
#print content
file_handler = open('taobao_content','w')

file_handler.write(content.decode('gbk').encode('utf-8'))
file_handler.close()
