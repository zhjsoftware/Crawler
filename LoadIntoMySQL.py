__author__ = 'jing'

import ConfigParser
import sys
from MySqlDBC import MySqlOps
import json

configParser = ConfigParser.ConfigParser()
configParser.read('resources/property.ini')

# get parameter of MySQL Database
userName = configParser.get('DB config', 'username')
password = configParser.get('DB config', 'password')
host = configParser.get("DB config", 'hostname')
charset = configParser.get('DB config', 'charset')

# load valuse from file
# filePath = '/home/jing/data/brand.txt'
filePath = "/home/jing/data/knowledge.txt"
values = []
with open(filePath) as fileHandler:
    record = ''
    content = fileHandler.readline()
    while content:
        if content.startswith('"title"'):
            if record:
                record = record[0:len(record)-len('\n')]
                record += '}'
                record = record.replace('\n', "\\n")
                try:
                    decodedContent = json.loads(record)
                except BaseException, e:
                    record = "{" + content
                    content = fileHandler.readline()
                    continue
                values.append((decodedContent["date"], decodedContent["title"], decodedContent["content"]))
            record = '{' + content
        else:
            record += content
        content = fileHandler.readline()

# insertSql = "insert into wine_brand (date, title, content) values (%s, %s, %s)"
insertsql = "insert into wine_knowledge (date, title, content) values (%s, %s, %s)"
try:
    mysqlUtil = MySqlOps(userName, password, 'petfriend', host, charset)
    # mysqlUtil.updateQuery("set names %s", 'utf8')
    # mysqlUtil.updateQuery(insertSql, values, True)
    mysqlUtil.updateQuery(insertsql, values, True)
except BaseException, e:
    print "Error occurs in MySQL Operation!"
finally:
    mysqlUtil.close()