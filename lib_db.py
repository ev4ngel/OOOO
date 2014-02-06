#-*- encoding:utf8 -*-
import sqlite3
import os
class axDBCfg:
    name="abx.db"
class axDB:
    #imgs:url,name,path,stat,torrent_id
    #torrents:url,name,path,stat,page_id
    #pages:url,title,stat(1 over,0 not over)
    def __init__(self,path=os.getcwd(),removeifexists=False):
        self._path=path
        self._dbname=axDBCfg.name
        self._new=False
        
    def isUsed(self):
        if os.path.exists(os.path.join(self._path,self._dbname)):
            self.connect()
            try:
                self.getPages()
                return True
            except:
                pass
            finally:
                self.close()
                return False
        else:
            return False
    def connect(self):
        abspath=os.path.join(self._path,self._dbname)
        self._cn=sqlite3.connect(abspath)
        self._cr=self._cn.cursor()
    def init_all(self):
        self.connect()
        try:
            self._cr.execute("CREATE TABLE imgs (url TEXT,name TEXT,path TEXT,stat INT,torrent_id INT)")
            self._cr.execute("CREATE TABLE torrents (url TEXT,name TEXT,path TEXT,stat INT,page_id INT)")
            self._cr.execute("CREATE TABLE pages (url TEXT,title TEXT,stat INT)")
            self._cn.commit()
        except:
            self._new=True
    def addImg(self,url,name,path,stat,torrent_id,commit=True):
        self._cr.execute("INSERT INTO imgs  VALUES(?,?,?,?,?)",(url,name,path,stat,torrent_id))
        if commit:
            self._cn.commit()
            return self._cr.lastrowid
        else:
            return -1
    def addImgs(self,img_s):
        self._cr.executemany("INSERT INTO imgs  VALUES(?,?,?,?,?)",img_s)
        self._cn.commit()
        return len(img_s)
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
    def addPage(self,url,title,stat,commit=True):
        self._cr.execute("INSERT INTO pages  VALUES(?,?,?)",(url,title,stat))
        if commit:
            self._cn.commit()
            return self._cr.lastrowid
        else:
            return -1
    def togglePageState(self,pid):
        self._cr.execute("UPDATE SET STAT=1 WHERE OID=?",(pid,))
        self._cn.commit()
    def addPages(self,page_s):
        self._cr.excutemany("INSERT INTO pages VALUES (?,?)",page_s)
        self._cn.commit()
        return len(page_s)
    def getPageIdByUrl(self,url):
        self._cr.execute("SELECT OID FROM pages WHERE url='%s'"%url)
        try:
            return self._cr.fetchone()[0]
        except:
            return -1
    def addTorrent(self,tor_url,tor_name,tor_dir,tor_stat,page_id,commit=True):
        self._cr.execute("INSERT INTO torrents VALUES (?,?,?,?,?)",(tor_url,tor_name,tor_dir,tor_stat,page_id))
        if commit:
            self._cn.commit()
            return self._cr.lastrowid
        else:
            return -1
    def addTorrents(self,tor_s):
        self._cr.executemany("INSERT INTO torrents VALUES (?,?,?,?,?)",tor_s)
##        for tor in tor_s:#Which method is the best?
##            self.addTorrent(*tor,commit=False)
        self._cr.commit()
        return len(tor_s)
    def getTorrentIdByName(self,tor_name):
        self._cr.execute("SELECT OID FROM TORRENTS where name='%s'"%tor_name)
        try:
            return self._cr.fetchone()[0]
        except:
            return -1
    def getTorrentUrlByPageId(self,page_id):
        self._cr.execute("SELECT URL,NAME FROM TORRENTS WHRER PAGE_ID=%s"%page_id)
        return self._cr.fentchall()

    def addPageItems(self,axItems,path):
        """http://99.99btgongchang.info/00/11.html
        [{'tor':"xxx",'img':[],'purl':xxx},]
        
        """
        for ai in axItems:
            self.addItem(ai,path,True)
        self._cn.commit()

    def getPages(self):
        self._cr.execute("SELECT OID,URL,STAT FROM PAGES")
        return self._cr.fetchall()
    def close(self):
        try:
            self._cn.close()
        except:
            pass#closed already
