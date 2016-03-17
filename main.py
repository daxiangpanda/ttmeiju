#!/usr/bin/env python
# encoding: utf-8
from bs4 import BeautifulSoup
import random
import urllib
import urllib2
def url_open(url):
    req = urllib2.Request(url)
    header1 = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'
    header2 = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'
    header3 = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
    header4 = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
    header5 = 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+'
    header6 = 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+'
    header7 = 'Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36'
    header8 = 'Mozilla/5.0 (Linux; Android 4.3; Nexus 10 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Safari/537.36'
    header9 = 'Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Safari/537.36'
    header10 = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)'
    header11 = 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
    header12 = 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    header = [header1,header2,header3,header4,header5,header6,header7,header8,header9,header10,header11,header12]
    req.add_header('User-Agent',random.choice(header))
    # proxies = ['120.195.198.69:80','120.195.195.249:80','112.64.28.11:8090']
    # proxy = random.choice(proxies)
    #
    # proxy_support = urllib2.ProxyHandler({'http':proxy})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)
    response = urllib2.urlopen(req)
    html = response.read()
    #print html
    return html

def url_make(name):
    baseurl = 'http://www.ttmeiju.com/search.php?keyword='
    res = ','
    print len(name)
    for i in range(0,len(name),2):
        res+=name[i:i+2]
        res+=','
    # print [res]
    # print baseurl+urllib.quote(res)+'&range=0'
    return baseurl+urllib.quote(res)+'&range=0'

def process_soup_teleplay(soup):
    soupinfo = soup.find_all('td')
    # print soupinfo
    name = soupinfo[1].find_all('a')[0].string
    link = soupinfo[1].find_all('a')[0]['href'].replace(u'\n','http://www.ttmeiju.com')
    state = soupinfo[2].string
    time_update=soupinfo[3].string
    return [name,link,state,time_update]

def find_link_teleplay(name,baselink):
    page = 0
    # link = baselink + 'page='+page
    # soup = BeautifulSoup(url_open(link))
    res = []
    while True:
        link = baselink + '?page='+str(page)
        soup = BeautifulSoup(url_open(link), "html.parser")
        result_tags = soup.find_all('tr',class_ = 'Scontent')
        if len(result_tags) == 0:
            print u'资源：%s抓取完毕'%name
            return res
        else:
            for i in result_tags:
                info = i.find_all('td')
                namel = info[1].find('a').string
                link = []
                for ii in info[2].find_all('a'):
                    link.append([ii['title'],ii['href']])
                size = info[3].string
                format = info[4].string
                res.append([namel,link,size,format])
                page+=1

def store()


# print find_link_teleplay(u'无耻','http://www.ttmeiju.com/meiju/Shameless.html')

if __name__ == '__main__':
    while True:
        name = (raw_input(u'请输入需要下载的美剧名称'))
        if name == '':
            name = '电影'
        soup = BeautifulSoup(urllib.urlopen(url_make(name.decode('utf-8').encode('gbk'))).read(),"html.parser")
        n = 0
        for i in soup.find_all('table',class_ = 'seedtable'):
            for ii in i.find_all('tr',bgcolor="#ffffff"):
                n+=1
                print '找到第%s条记录'%n
                info_tele = process_soup_teleplay(ii)
                print info_tele
                print find_link_teleplay(info_tele[0],info_tele[1])
                print
                print
