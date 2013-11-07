from bs4 import BeautifulSoup as bs,SoupStrainer as ss
import urllib,re,os
from dltorrent import *
#[{"img":[],"tor":xxxxx},]
#
#
def done(url):
    html=urllib.urlopen(url).read()
    bx=bs(html,parse_only=ss("div",id="content"))
    rlt=[]
    nexxt=bx.find(["a","img"])
    cc=0
    while nexxt:
        cc+=1    
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
x=done("http://99.99btgongchang.info/p2p/01/13-01-01-23-16-48.html")
def download_ex(ax,tgt_path,seperate_dir=False):
    for axx in ax:       
        dk=axx["tor"].split("/")[-1]
        print dk+"ing........."
        todir=tgt_path
        if seperate_dir:
            todir=os.path.join(tgt_path,dk)
            os.mkdir(todir)
        write_torrent(axx['tor'],todir)
        for img in axx['img']:
            t=os.path.join(todir,dk+"_"+img.split("/")[-1])
            if not os.path.exists(t):
                urllib.urlretrieve(img,t)
def print_ex(ax):
    for axx in ax:
        print axx.get("tor")
        print axx["img"]
        print "*"*50
#print_ex(x)
download_ex(x,"e:/")
