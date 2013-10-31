#-*- encoding:utf8 -*-
import urllib2, urllib, re, os, sys, HTMLParser, urlparse
from bs4 import BeautifulSoup as Bs
titles={"日本有码":None,"日本同步":None,"美女骑兵":None,}
#"灣搭拉咩"使用——————
#"欧美无码"=======中间，如果多个===则后半部分为其他
def log(x):
    _log=open('log.txt','w')
    for xx in x:
        for xxx in xx:
            _log.write(str(xx[xxx])+"\n")

        _log.write('*'*50+"\n")
    _log.close()
host="http://97.99bitgongchang.org/00/10.html"

def gethostcontent(eurl):
    s=urllib2.urlopen(eurl).read()
    root=Bs(s)
    ai=root.find_all("div",{'id':'content'})    
    g=re.search(r'<div.*?>(?P<content>.*)</div',str(ai[0]),flags=re.S)
    sss=g.group("content")
    return sss
def dealone(ct):
    one={}        
    img=re.findall(r'<img.*src="(?P<url>.*?jpg)"',ct)
    tor=re.findall(r'<a.*href="(?P<url>.*?html)"',ct)
    if img:
        one.setdefault("img",[])
        for ig in img:
            one['img'].append(ig)
    if tor:
        one.setdefault("torrent",[])
        for tr in tor:
            one['torrent'].append(tr)
    one['title']=re.search(r'\S+',re.sub(r'(<a.*?</a>)',"",ct,flags=re.S)).group(0)
    return one
def dealfull(ct):
    alls=[]  
    lss=re.split(r'(<br.*?>)|(</?font.*?>)|(</?strong>)|([\n\r])',ct,re.S)
    #lss=re.split(r'[\n\r]',sss,re.S)
    print len(lss)
    lasttor=4
    tmpstr=[]
    meettor=False
    for ln in lss:
        if not ln:
            continue
        #print ln
        img=re.search(r'<img.*src="(?P<url>.*?jpg)"',ln)
        tor=re.search(r'<a.*href="(?P<url>.*?html)"',ln)
        if img:
            alls[-1].setdefault("img",[])
            alls[-1]['img'].append(img.group('url'))
        elif tor:
            alls[-1].setdefault("torrent",[])
            alls[-1]['torrent'].append(tor.group("url"))
            lasttor=4
            meettor=True
        elif re.search(r'</a>',ln):
            continue
        else:
            if meettor:
                if lasttor==0:
                    alls.append({'title':tmpstr[0]})
                    del tmpstr[:]
                    meettor=False
                else:
                    lasttor-=1
                    tmpstr.append(ln)
            else:
                alls.append({'title':ln})
    return alls
def fromhostpath(host,x):
    return urlparse.urljoin(host, x['link'])
def rbym(url):
    #日本有碼
    alls=[]
    sss=re.sub(r'(<br.*?>)|(</?font.*?>)|(</?strong>)','',gethostcontent(url))
    lss=re.split(r'={5,}',sss,re.S)
    alls.extend(dealfull(lss[1]))
    for x in lss[2:-1]:
        alls.append(dealone(x))
    return alls
def yzwm(url):
    #亚洲无码，
    alls=[]    
    sss=re.sub(r'(<br.*?>)|(</?font.*?>)|(<strong>.*?</strong>)','',gethostcontent(url))
    lss=re.split(r'={5,}',sss,flags=re.S)
    for ct in lss[:-1]:
        alls.append(dealone(ct))
    return alls
def mnqb(url):
#美女骑兵，日本同步Nike，
    #eurl=urlparse.urljoin(host, x['link'])
    return dealfull(gethostcontent(url))


##    alls=[]  
##    sss=re.sub(r'(<br.*?>)|(</?font.*?>)|(</?strong>)','',gethostcontent(url))
##    lss=re.split(r'(<a.*?>.*?</a>)',sss,flags=re.S)
##    for ct in lss:
##        if not ct:
##            continue
##        lxx=re.split(r'(<img.*?>)',ct,flags=re.S)    
##        for xx in lxx:
##            if len(xx)<20:
##                continue
##            img=re.search(r'<img.*src="(?P<url>.*?jpg)"',xx)
##            tor=re.search(r'<a.*href="(?P<url>.*?html)"',xx)
##            aaa=re.search(r'(</?a.*?>)|(img.*?/?>)',xx)
##            if img:
##                alls[-1].setdefault("img",[])
##                alls[-1]['img'].append(img.group("url"))
##            elif tor:
##                alls[-1].setdefault("torrent",[])
##                alls[-1]['torrent'].append(tor.group("url"))
##            elif aaa:
##                continue
##            else:
##                c=re.search(r'[^\s]+',xx,flags=re.S).group(0)
##                alls.append({"title":c})
##    return alls
def wtlml(url):
    #灣搭拉咩
    alls=[]    
    sss=re.sub(r'(<br.*?>)|(</?font.*?>)|(<strong>.*?</strong>)','',gethostcontent(url))
    lss=re.split(r'-{5,}',sss,flags=re.S)
    for ct in lss:
        alls.append(dealone(ct))
    return alls

#MNQB({'link':'/p2p/10/13-09-30-23-06-49.html'})
log(mnqb('http://ko.99bitgc.info/p2p/10/13-10-26-22-58-54.html'))
