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
    while nexxt:
        if nexxt.name=="a":
            try:
                nexxt.img.get("src")
            except:
                #print nexxt
                if len(rlt)!=0:
                    if not rlt[-1].get("tor",None):
                        rlt[-1]["tor"]=nexxt.get("href")
        elif nexxt.name=="img":
            src=nexxt.get("src")
            if re.search(r'jpg$',src,re.I):
                if len(rlt)==0 or  rlt[-1].get("tor",None):
                    rlt.append({"img":[src]})
                else:
                    rlt[-1]["img"].append(src)
        #print nexxt.name
        nexxt=nexxt.find_next(["a","img"])
    return rlt
x=done("http://99.99btgongchang.info/p2p/01/12-12-31-10-58-28.html")
def download_ex(ax,tgt_path):
    for axx in ax:       
        dk=axx["tor"].split("/")[-1]
        print dk+"ing........."
        tar=os.path.join(tgt_path,dk)
        os.mkdir(tar)
        write_torrent(axx['tor'],tar)
        for img in axx['img']:
            urllib.urlretrieve(img,os.path.join(tar,dk+"_"+img.split("/")[-1]))
download_ex(x,"e:/")
