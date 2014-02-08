# -*- coding: utf8 -*-
from bs4 import BeautifulSoup as bs,SoupStrainer as ss
import urllib2,urllib,re,os,urlparse
from lib_db import *
from lib_tor import *
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
    sum_pg=len(ax)
    ct_pg=1
    for axk,axv in ax.items():#这里就可以放心大胆的存放所有剩余链接地址了        
        pid=db_instance.addPage(axk,"",0)
        todir=tgt_path
        sum_itm=len(axv)
        print "Downloading {0}:[{1}/{2},{3} TORs]".format(axk.split('/')[-1],ct_pg,sum_pg,sum_itm)
        ct_tor=1
        for item in axv:
            tor_rlt=0
            dk=item["tor"].split("/")[-1]
            if seperate_dir:
                todir=os.path.join(tgt_path,dk)
                os.mkdir(todir)
            print "[{0}/{1}]{2},{3} Pics".format(ct_tor,sum_itm,item['tor'],len(item['img']))
            url,rlt=torrent_download(item['tor'],todir)
            if rlt:
                tor_rlt=1
            tid=db_instance.addTorrent(url,url.split("/")[-1],todir,int(tor_rlt),pid)
            
            try:
                for img in item['img']:
                    imgrlt=img_download(img,todir,dk+"_")
                    db_instance.addImg(imgrlt[1],imgrlt[0],todir,int(imgrlt[2]),tid)
            except KeyError as ke:
                print "No Img Found"
            ct_tor+=1
        db_instance.togglePageState(pid)
        ct_pg+=1

