__author__ = 'jing'


import MySQLdb
import json


# def loadPropertyFromFile():
#     pro = open('resources/property', 'r')
#     while True:
#         content = pro.read()
#         if content:
#             return json.loads(content)
#         else:
#             break
#     pro.close()
#
#
# def initConnection(hostname, username, password, dbname):
#     connection = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname, charset="utf8")
#     return connection.cursor()
#
# obj = loadPropertyFromFile()
# connection = MySQLdb.connect(host=obj['host'], user=obj['user'], passwd=obj['password'], db=obj['database'], charset=obj['charset'])
# cursor = connection.cursor()
#
# n = cursor.execute('select * from user')
# print n
#
# for record in cursor.fetchall():
#     print 'name:%s age:%d' % record
#
#
# cursor.close()
# connection.close()


class MySqlOps():

    def __init__(self, userName, password, dbName, host='localhost', charset='utf8'):
        try:
            self.connection = MySQLdb.connect(host=host, user=userName, passwd=password, db=dbName, charset=charset)
            self.cursor = self.connection.cursor()
        except MySQLdb.Error, e:
            print "MySQL connection Error %d: %s" % (e.args[0], e.args[1])
            raise

    def selectQuery(self, querySql):
        try:
            self.cursor.execute(querySql)
            return self.cursor.fetchall()
        except MySQLdb.Error, e:
            print "MySQL execution Error %d: %s" % (e.args[0], e.args[1])
            raise

    def updateQuery(self, querySql, param, multiQuery=False):
        try:
            if not multiQuery:
                self.cursor.execute(querySql, param)
                self.connection.commit()
            else:
                self.cursor.executemany(querySql, param)
                self.connection.commit()
        except MySQLdb.Error, e:
            print "MySQL execution Error %d: %s" % (e.args[0], e.args[1])
            raise

    def close(self):
        self.cursor.close()
        self.connection.close()