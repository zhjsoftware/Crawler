__author__ = 'jing'

import urllib2
import sys
import os

pwd_dir = os.getcwd()
content = urllib2.urlopen("http://taobao.com").read()
print content
#file_handler = open('taobao_content','w')

#file_handler.write(content)
#file_handler.close()
