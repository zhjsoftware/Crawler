__author__ = 'jing'


import MySQLdb,json

def loadPropertyFromFile():
  pro = open('resources/propety', 'r')
  while True:
    content = pro.read()
    if content:
      return json.loads(content)
    else:
      break
  pro.close()

def initConnection(hostname, username, password, dbname):
    connection = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname, charset="utf8")
    return connection.cursor()

obj = loadPropertyFromFile()
connection = MySQLdb.connect(host=obj['host'], user=obj['user'], passwd=obj['password'], db=obj['database'], charset=obj['charset'])
cursor = connection.cursor()

n = cursor.execute('select * from user')
print n

for record in cursor.fetchall():
    print 'name:%s age:%d' %(record[0], record[1])


cursor.close()
connection.close()
