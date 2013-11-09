from bs4 import BeautifulSoup as bs,SoupStrainer as ss
import urllib,re,os,urlparse
from dltorrent import *
from axdb import *

#[{"img":[],"tor":xxxxx},]
#
#
def fromMonthPage(url):
    """
    return:[{"title":item_title."url":url_of_next_page},more...]
    """
    html=urllib.urlopen(url).read()
    bx=bs(html,parse_only=ss("div",id="content"))
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
    html=urllib.urlopen(url).read()
    bx=bs(html,parse_only=ss("div",id="content"))
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

def WriteLog(img_url):
    print "[ImgFail]"+img
    with open("log.txt",'a') as f:
        f.write(img+os.linesep)
def _None(url):
    pass
def download_ax(ax,tgt_path,seperate_dir=False,ondisableimg=WriteLog,ondisabletor=_None,onsuccessimg=_None,onsuccesstor=_None,onitem=_None):
    """
    input: ax return by fromItemPage
            tgt_path the dir to put
            seperate_dir true if you want to mkdir for every item(one torrent and more pic)
    return:None for final use
    """
    for axx in ax:       
        dk=axx["tor"].split("/")[-1]
        print dk+"_ing........."
        todir=tgt_path
        if seperate_dir:
            todir=os.path.join(tgt_path,dk)
            os.mkdir(todir)
        url,rlt=torrent_download(axx['tor'],todir)
        onitem({'path':dk,"url":axx['tor'],"purl":axx['purl'],"img":axx['img']})
        if not rlt:
            ondisabletor({"url":url,"purl":axx['purl']})
        for img in axx['img']:
            t=os.path.join(todir,dk+"_"+img.split("/")[-1])
            if not os.path.exists(t):
                try:
                    urllib.urlretrieve(img,t)
                    onsuccessimg({"url":img,"tor":url})
                except:
                    ondisableimg({"url":img,"tor":url})
def print_month_page(ax):
    for axx in ax:
        print axx.get("tor")
        print axx["img"]
        print "*"*50
def print_item_page(ax):
    for x in ax:
        print x["title"]
        print x["url"]
        print '*'*50
if __name__=="__main__":
    logger=axDB("E:/xxxxx")
    def xfimg(ax):
        logger.addDisableImg(ax)
    def xftor(ax):
        logger.addDisableTor(ax)
    def itemme(ax):
        logger.addItem(ax,ax['path'])
    for x in range(1,5):
        mains=fromMonthPage("http://99.99btgongchang.info/00/{0}.html".format(str(x+100)[-2:]))
        for xm in mains:
            logger.addMonthPage(xm["title"],xm['url'])
            print xm["title"]+"*"*10
            ax=fromItemPage(xm['url'])
            #logger.addPageItems(ax,"e:")
            download_ax(ax,"E:/xxxxx",ondisableimg=xfimg,ondisabletor=xftor)
    #print_main(fromMain("http://99.99btgongchang.info/00/01.html"))
    #print_ex(x)
    #download_ex(x,"e:/")
