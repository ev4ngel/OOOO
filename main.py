# -*- coding: utf8 -*-
import sys,os,re,json
from lib_page import *
from lib_db import *
def usage():
    print "99BT Downloader"
    print "%s url target_dir"%sys.argv[0]
def retry(path):
    """重新下载"""
    pass
def urlparser(url):
    if url.startswith("http"):
        _url=url[7:]
    typex=_url.split("/")[1]
    obj=None
    if typex=="p2p":
        obj=fromItemPage
    else:
        obj=fromMonthPage
    return obj(url)
def x():
    xy=urlparser(sys.argv[1])
    rlt={}
    if isinstance(xy,list):
        for x in xy:
            rlt.update(fromItemPage(x["url"]))
    else:
        rlt.update(xy)
    return rlt
if __name__=="__main__":
    """
    main.py url target
    """
    if len(sys.argv)==1:
        usage()
    elif len(sys.argv)>=3:
        db_instance=axDB(sys.argv[2])
        sd=False
        if "-s" in sys.argv:
            sd=True
        download_ax(x(),sys.argv[2],db_instance,seperate_dir=sd)
