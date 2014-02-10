# -*- coding: utf8 -*-
from bs4 import BeautifulSoup as bs,SoupStrainer as ss
import urllib2,urllib,re,os,urlparse,httplib
from lib_db import *
from lib_download import *
from lib_common import *
from lib_thread import *
#[{"img":[],"tor":xxxxx},]
def fromMonthPage(url):
    rlt=[]
    request=urllib2.Request(url,headers=Common.HEADER)
    try:
        html=urllib2.urlopen(request).read()    
    except :
        if Common.DEBUG:
            print "Error:Reading MonthPage From %s"%url
        return rlt
    bx=bs(html,"html.parser",parse_only=ss("div",id="content"))    
    aas=bx.find_all("a")
    for a in aas:
        href=a.get("href")
        if re.search(r'(\d\d-){5}\d\d\.html',href):
            rlt.append({"title":a.text,"url":urlparse.urljoin(url,href)})
    return rlt

def fromItemPage(url):
    request=urllib2.Request(url,headers=Common.HEADER)
    rlt=[]
    try:
        html=urllib2.urlopen(request).read()  
    except:
        if Common.DEBUG:
            print "Error:Reading %s"%url
            return {url:rlt}
    bx=bs(html,"html.parser",parse_only=ss("div",id="content"))        
    nexxt=bx.find(["a","img"])
    while nexxt: 
        if nexxt.name=="a":
            try:
                nexxt.img.get("src")
            except:
                if len(rlt)!=0:
                    href=nexxt.get("href").strip()
                    if not rlt[-1].get("tor",None) and re.search(r'([A-Z0-9]{6,10}\.html$)|([a-z0-9]{16}\.html$)',href) :
                        rlt[-1]["tor"]=href
        elif nexxt.name=="img":
            src=nexxt.get("src").strip()
            if re.search(r'jpg$',src,re.I):                
                if len(rlt)==0 or  rlt[-1].get("tor",None):
                    rlt.append({"img":[src]})
                else:
                    rlt[-1]["img"].append(src)
        nexxt=nexxt.find_next(["a","img"])            
    return {url:rlt}

def download_ax(ax,tgt_path,db_instance,seperate_dir=False):
    if not os.path.exists(tgt_path):
        os.makedirs(tgt_path)
    if db_instance.isUsed():
        db_instance.connect()
        axpg=ax.keys()
        for dpg in db_instance.getPages():
            if dpg[1] in axpg:
                if int(dpg[2])==1:
                    del ax[dpg[1]]
                else:
                    urls=[x[0] for x in db_instance.getTorrentUrlByPageId(dpg[0],1)]
                    for item in ax[dpg[1]][::-1]:
                        if not item.get("tor",None) or item['tor'] in urls:
                            ax[dpg[1]].remove(item)
    
    db_instance.connect()
    db_instance.init_all()
    for axk,axv in ax.items():
        Common.LOCK_DB.acquire()
        pid=db_instance.addPage(axk,"",0)
        Common.LOCK_DB.release()
        item_lock=thread.allocate_lock()
        col_item=Collect_Item(axv,item_lock)
        thread_item=[Thread_Item(col_item,tgt_path,db_instance,axk,pid,seperate_dir) for i in range(Common.ITEM_THREAD_NUM)]
        for ti in thread_item:
            ti.start()                 
