from bs4 import BeautifulSoup as bs,SoupStrainer as ss
import urllib,re,os,urlparse
from dltorrent import *
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
    return:[{"tor":url_of_torrent_page,"img":[url_of_one_img,url_of_other_img]},{more...}]
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
        elif nexxt.name=="img":
            src=nexxt.get("src").strip()
            if re.search(r'jpg$',src,re.I):                
                if len(rlt)==0 or  rlt[-1].get("tor",None):
                    rlt.append({"img":[src]})
                else:
                    rlt[-1]["img"].append(src)
        nexxt=nexxt.find_next(["a","img"])
    return rlt

def download_ax(ax,tgt_path,seperate_dir=False):
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
        torrent_download(axx['tor'],todir)
        for img in axx['img']:
            t=os.path.join(todir,dk+"_"+img.split("/")[-1])
            if not os.path.exists(t):
                try:
                    urllib.urlretrieve(img,t)
                except:
                    print "[ImgFail]"+img
                    with open("log.txt",'a') as f:
                        f.write(img+os.linesep)
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
    for x in range(1,5):
        mains=fromMonthPage("http://99.99btgongchang.info/00/{0}.html".format(str(x+100)[-2:]))
        for xm in mains:
            print xm["title"]+"*"*10
            ax=fromItemPage(xm['url'])
            download_ax(ax,"d:/xxxxx")
    #print_main(fromMain("http://99.99btgongchang.info/00/01.html"))
    #print_ex(x)
    #download_ex(x,"e:/")
