# -*- coding: utf8 -*-
from bs4 import BeautifulSoup as bs,SoupStrainer as ss
import urllib2,urllib,re,os,urlparse
from lib_page import *
from lib_db import *

#[{"img":[],"tor":xxxxx},]
#
#
def fromMonthPage(url):
    """
    return:[{"title":item_title."url":url_of_next_page},more...]
    """
    request=urllib2.Request(url,headers={"user-agent":"Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0"})
    html=urllib2.urlopen(request).read()    
    bx=bs(html,"html.parser",parse_only=ss("div",id="content"))
    rlt=[]
    aas=bx.find_all("a")
    for a in aas:
        href=a.get("href")
        if re.search(r'(\d\d-){5}\d\d\.html',href):
            rlt.append({"title":a.text,"url":urlparse.urljoin(url,href)})
    return rlt
def fromItemPage(url):
    """
    return:[{"tor":url_of_torrent_page,"img":[url_of_one_img,url_of_other_img],'purl':parent_url},{more...}]
    """
    #urlparse.urljoin(filepath,n)
    request=urllib2.Request(url,headers={"user-agent":"Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0"})
    rlt=[]
    try:
        html=urllib2.urlopen(request).read()  
        bx=bs(html,"html.parser",parse_only=ss("div",id="content"))
        
        nexxt=bx.find(["a","img"])
        while nexxt: 
            if nexxt.name=="a":
                try:
                    nexxt.img.get("src")
                except:
                    if len(rlt)!=0:
                        href=nexxt.get("href").strip()
                        if not rlt[-1].get("tor",None) and re.search(r'[A-Z0-9]{6,10}\.html$',href) :
                            rlt[-1]["tor"]=href
                            #rlt[-1]["purl"]=url
            elif nexxt.name=="img":
                src=nexxt.get("src").strip()
                if re.search(r'jpg$',src,re.I):                
                    if len(rlt)==0 or  rlt[-1].get("tor",None):
                        rlt.append({"img":[src]})
                    else:
                        rlt[-1]["img"].append(src)
            nexxt=nexxt.find_next(["a","img"])
    except:
        print "Failed to Get "+url
    return {url:rlt}

def _None(url):
    pass
def download_ax(ax,tgt_path,db_instance,seperate_dir=False,
                ondisableimg=_None,
                ondisabletor=_None,
                onsuccessimg=_None,
                onsuccesstor=_None,
                onitem=_None):
    """
    input:{"page_url":[{tor:xxx,img:[xxx,xxx]},{tor:xxx,img:[xxx,xxx]},{url:xxx,tor:xxx,img:[xxx,xxx]}],"page_url":[]}
        ax return by fromItemPage
            tgt_path the dir to put
            seperate_dir true if you want to mkdir for every item(one torrent and more pic)
    return:None for final use
    """
    
    if not os.path.exists(tgt_path):
        os.makedirs(tgt_path)
    if db_instance.isUsed():
        db_instance.connect()
        for dpg in db_instance.getPages():
            if int(dpg[2])==0:
                del ax[dpg[1]]
            else:
                urls=[x[0] for x in db_instance.getTorrentsUrlByPageId(dpg[0])]       
                for item in ax[dpg]:
                    if item.get("tor",None) or item['tor'] in urls:
                        del item
        
    for axk,axv in ax:#这里就可以放心大胆的存放所有剩余链接地址了
        pid=db_instance.addPage(axk,"",0)
        todir=tgt_path
        for item in axv:
            tor_rlt=0
            dk=item["tor"].split("/")[-1]
            if seperate_dir:
                todir=os.path.join(tgt_path,dk)
                os.mkdir(todir)
            url,rlt=torrent_download(item['tor'],todir)
            if rlt:
                tor_rlt=1
            tid=db_instance.addTorrent(url,url.split("/")[-1],todir,int(tor_rlt),pid)
            try:
                for img in item['img']:
                    imgrlt=img_download(img,todir,dk+"_")
                    db.addImg(imgrlt[1],imgrlt[0],todir,int(imgrlt[2]),tid)
            except KeyError as ke:
                print "No Img Found"
        db_instance.togglePageState(pid)
            
##        todir=tgt_path
##        try:
##            dk=axx["tor"].split("/")[-1]
##            pid=db.getPageIdByUrl(axx['purl'])
##            if pid==-1:
##                pid=db.addPage(axx['purl'],"",1)            
##            if seperate_dir:
##                todir=os.path.join(tgt_path,dk)
##                os.mkdir(todir)
##            print "[Tor]"+axx['tor']+"_ing..."
##            if db.getTorrentIdByName(dk)>0:
##                print "Existing,Cancel..."
##                continue
##            url,rlt=torrent_download(axx['tor'],todir)
##            print "OK:"+str(rlt)
##            tid=db.addTorrent(url,url.split("/")[-1],todir,int(rlt),pid)
##        except KeyError as ke:
##            print "No Torrent Found"
##        try:
##            for img in axx['img']:
##                print "[Img]"+img.split("/")[-1]+"_ing..."
##                imgrlt=img_download(img,todir,dk+"_")
##                print "OK:"+str(imgrlt[0])
##                db.addImg(imgrlt[1],imgrlt[0],todir,int(imgrlt[2]),tid)
##        except KeyError as ke:
##            print "No Img Found"
