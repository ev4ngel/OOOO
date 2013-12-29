from bs4 import BeautifulSoup as bs,SoupStrainer as ss
import urllib2,urllib,re,os,urlparse
from torgetter import *
from axdb import *

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
    html=urllib2.urlopen(request).read()  
    bx=bs(html,"html.parser",parse_only=ss("div",id="content"))
    rlt=[]
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
                        rlt[-1]["purl"]=url
        elif nexxt.name=="img":
            src=nexxt.get("src").strip()
            if re.search(r'jpg$',src,re.I):                
                if len(rlt)==0 or  rlt[-1].get("tor",None):
                    rlt.append({"img":[src]})
                else:
                    rlt[-1]["img"].append(src)
        nexxt=nexxt.find_next(["a","img"])
    return rlt

def _None(url):
    pass
def download_ax(ax,tgt_path,seperate_dir=False,
                ondisableimg=_None,
                ondisabletor=_None,
                onsuccessimg=_None,
                onsuccesstor=_None,
                onitem=_None):
    """
    input: ax return by fromItemPage
            tgt_path the dir to put
            seperate_dir true if you want to mkdir for every item(one torrent and more pic)
    return:None for final use
    """
    for axx in ax:        
        dk=axx["tor"].split("/")[-1]
        print axx["tor"]
        #print dk+"_ing........."
        todir=tgt_path
        if seperate_dir:
            todir=os.path.join(tgt_path,dk)
            os.mkdir(todir)
        url,rlt=torrent_download(axx['tor'],todir)
        onitem({'path':dk,"url":axx['tor'],"purl":axx['purl'],"img":axx['img']})
        if not rlt: 
            ondisabletor({"url":url,"purl":axx['purl']})
        for img in axx['img']:
            imgrlt=img_download(img,todir,dk+"_")
            if not imgrlt[2]:
                ondisableimg([])
            else:
                onsuccessimg([])
