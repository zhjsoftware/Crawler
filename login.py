import base64

__author__ = 'jing'

import urllib2,urllib
import cookielib
import json
import re
import hashlib
import base64

def renren_login(user, passwd):
    loginurl = "http://www.renren.com/PLogin.do"
    url = 'http://www.renren.com/home.do'
    try:
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        data = urllib.urlencode({"email":user,"password":passwd})
        urllib2.install_opener(opener)
        opener.open(loginurl,data)
        op = opener.open(url)
        content = op.read()
        return content
    except Exception, e:
        print str(e)

def get_servertime():
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo' + \
                     '&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk'+\
                     '&client=ssologin.js(v1.3.18)&_=1329806375939'
    predata = urllib2.urlopen(prelogin_url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(predata).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        return servertime, nonce
    except :
        print 'Get ServerTime error! exiting...'
        return None

def get_password(pwd, servertime, nonce):
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd_intm = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd_intm).hexdigest()
    return pwd3


def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username

def sina_login():
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    postdata = {'entry' : 'weibo',
                'gateway' : '1',
                'from' : '',
                'savestate' : '7',
                'userticket' : '1',
                'ssosimplelogin' : '1',
                'vsnf' : '1',
                'vsnval' : '',
                'su' : '',
                'service' : 'miniblog',
                'servertime' : '',
                'nonce' : '',
                'pwencode' : 'wsse',
                'sp' : '',
                'encoding' : 'utf-8',
                'url' : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                'returntype' : 'META'
    }
    username = 'zhjsoftware@gmail.com'
    pwd = '870912zz'
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
    try:
        servertime, nonce = get_servertime()
    except :
        return
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['su'] = get_user(username)
    postdata['sp'] = get_password(pwd, servertime, nonce)
    postdata = urllib.urlencode(postdata)
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req = urllib2.Request(url = url, data=postdata, headers=headers)
    result = urllib2.urlopen(req)
    text = result.read()
    print text
    p = re.compile('location\.replace\(\"(.*?)\"\)')
    try:
        login_url = p.search(text).group(1)
        print login_url
        response = urllib2.urlopen(login_url)
        print 'login succeed!'
    except :
        print 'login error.'


if __name__ == "__main__":
#    print renren_login("","")
    sina_login()




