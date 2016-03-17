#!/usr/bin/env python
# encoding: utf-8
from bs4 import BeautifulSoup
import urllib
def url_make(name):
    baseurl = 'http://www.ttmeiju.com/search.php?keyword='
    res = ','
    print len(name)
    for i in range(0,len(name),2):
        res+=name[i:i+2]
        res+=','
    return baseurl+urllib.quote(res)+'&range=0'
name = (raw_input(u'请输入需要下载的美剧名称'))
soup = BeautifulSoup(urllib.urlopen(url_make(name)).read(),"html.parser")
for i in soup.find_all('table',class_ = 'seedtable'):
    for ii in i.find_all('tr'):
        print ii
        print
        print
