#-*- coding:utf-8 -*-
from gy99 import *
import json,sys,os
import axdb
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
#    logger=axDB("d:/xxxxx")
#    def xfimg(ax):
#        logger.adpath':dk,"url":axx['tor'],"purl":axx['purl'],"img":axx['img']})
#        if not rlt: dDisableImg(ax)
#    def xftor(ax):os.makedirs()
#        logger.addDisableTor(ax)
#    def itemme(ax):
#        logger.addItem(ax,ax['path'])
    #for x in range(1,5):
    #mains=fromMonthPage("http://ko.99bitgc.info/00/01.html")
    #a=json.dumps(mains)
    #open("d:\\axm.txt",'w').write(a)    
    #.format(str(x+100)[-2:]))
    month12=fromMonthPage("http://ko.99bitgongchang.com/00/11.html")
    cct,ct=0,str(len(month12))
    TAR="abc"
    t_db=axdb.axDB(TAR)
    par_urls=[x[0] for x in t_db.getPages()]
    t_db.close()
    for ak in month12:
        cct+=1
        print "["+str(cct)+"/"+ct+"]---->"+ak['title']
        if ak['url'] in par_urls:
            print "Exsited,Pass"
            continue
        #db=axdb.axDB(os.path.join(os.getcwd(),TAR))
        et=[]#[x[0] for x in db.getPages()]
        a=fromItemPage(ak['url'])
        if a not in et:
            download_ax(a,TAR)
    #a=fromItemPage("http://ko.99bitgc.info/p2p/11/13-11-29-22-05-48.html")
    #   download_ax(a,os.getcwd())
    #for xm in mains:
        #print "Getting "+xm['url']
#        logger.addMonthPage(xm["title"],xm['url'])
        #print xm["title"]+"*"*10
        #ax=fromItemPage(xm['url'])
        #x.extend(ax)
    #open("d:\\aaaxm.txt",'w').write(json.dumps(x))
    #sys.exit(0)
        #logger.addPageItems(ax,"e:")
    #try:
        #continue
        #u,r=download_ax(ax,"d:/ooii")#,ondisableimg=xfimg,ondisabletor=xftor)
        #if not r:
        #    print "failed to download "+u
    #print_main(fromMain("http://99.99btgongchang.info/00/01.html"))
    #print_ex(x)
    #download_ex(x,"e:/")
