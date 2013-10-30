#-*- encoding:utf8 -*-
import urllib2, urllib, re, os, sys, HTMLParser, urlparse
from bs4 import BeautifulSoup as Bs

class eHPer(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self._link_found=False
        self._links=[]
        self._amI_in_content=False
    def handle_starttag(self, tag, attrs):
        for an, av in attrs:
            if an=='href' and re.search(r'/p2p/[\w/-]*\.html', av) and self._amI_in_content:
                self._link_found=True
                self._links.append({"link":av})
            if an=='id' and av=="content":
                self._amI_in_content=True
    def handle_endtag(self, tag):
        if tag=="a":
            self._link_found=False
    def handle_data(self, data):
        if self._link_found and self._amI_in_content:
            self._links[-1]['name']=data
    def links(self):
        return self._links

def parsePage(pagestring):
    rlt=re.search(r'<div id="content">(.*?)</div>', pagestring, re.S)
    page=rlt.group(1)
    lines=re.split(r'<br\s*/+>', page, flags=re.S)
    print len(lines)
#    torent=5
#    tcount=0
#    tbegin=False
#    all=[]
#    torlist=[]
#    for ln in lines:
#        
#        a=re.search(r'<a.*/a>?', ln)
#        if a:
#            
#    
    
#    cs=re.split(r'={5,100}(?=[^=])', rlt.group(1), flags=re.S)
#    for css in cs:
#        print css[30]
#        break


host="http://97.99bitgongchang.org/00/10.html"
#http://97.99bitgongchang.info"
rst=urllib2.urlopen(host).read()
eP=eHPer()
eP.feed(rst)
r=eP.links()
for x in r[:30]:
    print x['link']+";"+x['name']           
    eurl=urlparse.urljoin(host, x['link'])
    s=urllib2.urlopen(eurl).read()
    root=Bs(s)
    ai=root.find_all("div",{'id':'content'})
    for x in ai:
        sss=re.sub(r'<br.*?>','',str(x))
        sss=re.sub(r'<font.*?>','',sss)
        print sss
##    
