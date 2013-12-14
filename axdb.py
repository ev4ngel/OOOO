#-*- encoding:utf8 -*-
import sqlite3
import os
class axDB:
    def __init__(self,path=os.getcwd()):
        self._path=path
        self._dbname="ax.db"
        self.init_all()
    def init_all(self):
        abspath=os.path.join(self._path,self._dbname)
        if not os.path.exists(abspath):
            self._cn=sqlite3.connect(abspath)
            self._cr=self._cn.cursor()
            self._cr.execute("CREATE TABLE DISABLEIMG (URL TEXT,PTID INT)")
            self._cr.execute("CREATE TABLE MONTHPAGE (MPURL TEXT,MPTITLE TEXT,MPDOWNSTATE INT DEFAULT 0)")
            self._cr.execute("CREATE TABLE IMGS (IURL TEXT,INAME TEXT,TID INT,IPATH TEXT,IDOWNSTATE INT DEFAULT 0)")
            self._cr.execute("CREATE TABLE TORS (TNAME TEXT,MPID INT,TPURL TEXT,TPATH TEXT DEFAULT NULL,TDOWNSTATE INT  DEFAULT 0)")
            self._cr.execute("CREATE TABLE DISABLETOR (URL TEXT,PURL TEXT)")
            self._cn.commit()
        else:
            self._cn=sqlite3.connect(abspath)
            self._cr=self._cn.cursor()
    def addMonthPage(self,title,url):
        self._cr.execute("INSERT INTO MONTHPAGE (MPTITLE,MPURL) VALUES(?,?)",(title,url))
        self._cn.commit()
        return self._cr.lastrowid
    def addMonthPages(self,axmps):
        self._cr.excutemany("INSERT INTO MONTHPAGE (MPTITLE,MPURL) VALUES (?,?)",[(a['title'],a['url']) for a in axmps])
        self._cn.commit()
    def addItem(self,axItem,path,mpid,waitforcommit=False):
        """
        axItem:["tor",img:[]]
        """
        self._cr.execute("SELECT OID FROM MONTHPAGE WHERE MPURL='?'",(axItem["purl"],))
        r=self._cr.fetchone()
        mpid=r[0] if r else -1
##        mpid=self.getPageIdByUrl(ax)
        self._cr.execute("INSERT INTO TORS (TNAME,TPURL,MPID,TPATH) VALUES (?,?,?,?)",(axItem['tor'].split("/")[-1],axItem['tor'],mpid,path))
        lastrow=self._cr.lastrowid
        self._cr.executemany("INSERT INTO IMGS (IURL,INAME,TID) VALUES (?,?,?)",[(a,a.split('/')[-1],lastrow) for a in axItem["img"]])
        if not waitforcommit:
            self._cn.commit()
    def getPageIdByUrl(self,url):
        self._cr.execute("SELECT OID FROM MONTHPAGE WHERE MPURL='?'",(url,))
        r=self._cr.fetchone()
        rlt=-1 if not r else r[0]
        return rlt
    def addTorrent(self,tor_url,tor_dir,tor_page_id):
        self._cr.execute("INSERT INTO TORS(TNAME,TPURL,TPATH,MPID) VALUES (?,?,?,?)",(tor_url.split("/")[-1],tor_url,tor_dir,tor_page_id))
        self._cn.commit()
        return self._cr.lastrowid
    def addDisableTor(self,ax):
        self._cr.execute("INSERT INTO DISABLETOR (URL,PURL) VALUES (?,?)",(ax['url'],ax['purl']))
        self._cn.commit()
    def addPageItems(self,axItems,path):
        """http://99.99btgongchang.info/00/11.html
        [{'tor':"xxx",'img':[],'purl':xxx},]
        
        """
        for ai in axItems:
            self.addItem(ai,path,True)
        self._cn.commit()
        
    def addDisableImg(self,ax):
        """
        ax {"tor":"","img":[]}
        """
        self._cr.execute("SELECT OID FROM TORS WHERE TURL='?'",(ax['tor'],))
        r=self._cr.fetchone()
        self._cr.executemany("INSERT INTO DISABLEIMG (URL,PTID) VALUES (?,?)",[(a,r[0]) for a in ax['img']])
        self._cr.commit()
    def close(self):
        try:
            self._cn.close()
        except:
            pass
