import sys,os,re
from lib_page import *

def usage():
    print "99BT Downloader"
    print "%s url target_dir"%sys.argv[0]

def urlparser(url):
    if url.startswith("http"):
        _url=url[7:]
    typex=_url.split("/")[1]
    obj=None
    print typex
    if _url=="p2p":
        obj=fromItemPage
    else:
        obj=fromMonthPage
    return obj
        
if __name__=="__main__":
    """
    main.py url target
    """
    if len(sys.argv)==1:
        usage()
    elif len(sys.argv)==3:
        download_ax(urlparser(sys.argv[1])(sys.argv[1]),sys.argv[2])
        
