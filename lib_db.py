#-*- coding:utf8 -*-
import sqlite3
import os
from lib_common import *

class axDB:
    def __init__(self,path=os.getcwd(),removeifexists=False):
        self._path=path
        self._dbname=Common.DBNAME
        self._cr=self._cn=None
    def isUsed(self):
        rlt_stat=False
        if os.path.exists(os.path.join(self._path,self._dbname)):
            self.connect()
            try:
                self.getPages()
                rlt_stat= True
            except:
                pass
            finally:
                self.close()
        return rlt_stat
    def connect(self):
        abspath=os.path.join(self._path,self._dbname)
        if not self._cn and not self._cr:
            self._cn=sqlite3.connect(abspath,check_same_thread=False)
            self._cr=self._cn.cursor()
    def init_all(self):
        self.connect()
        try:
            self._cr.execute("CREATE TABLE imgs (url TEXT,name TEXT,path TEXT,stat INT,torrent_id INT)")
            self._cr.execute("CREATE TABLE torrents (url TEXT,name TEXT,path TEXT,stat INT,page_id INT)")
            self._cr.execute("CREATE TABLE pages (url TEXT,title TEXT,stat INT)")
            self._cn.commit()
        except:
            if Common.DEBUG:
                print "Warn:All Table Exists"
    def addImg(self,url,name,path,stat,torrent_id,commit=True):
        self._cr.execute("INSERT INTO imgs  VALUES(?,?,?,?,?)",(url,name,path,stat,torrent_id))
        if commit:
            self._cn.commit()
            return self._cr.lastrowid
        else:
            return -1

    def addPage(self,url,title,stat,commit=True):
        self._cr.execute("SELECT OID FROM PAGES WHERE URL=?",(url,))
        rlt=self._cr.fetchone()
        if rlt:
            return rlt[0]
        else:
            self._cr.execute("INSERT INTO pages  VALUES(?,?,?)",(url,title,stat))
            if commit:
                self._cn.commit()
                return self._cr.lastrowid
            else:
                return -1
    def togglePageState(self,pid):
        self._cr.execute("UPDATE  PAGES SET STAT=1 WHERE OID=?",(pid,))
        self._cn.commit()

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

    def getTorrentIdByName(self,tor_name):
        self._cr.execute("SELECT OID FROM TORRENTS where name='%s'"%tor_name)
        try:
            return self._cr.fetchone()[0]
        except:
            return -1
    def getTorrentUrlByPageId(self,page_id,selectall=-1):
        append=""
        par=(page_id,)
        if selectall!=-1:
            append="and STAT=?"
            par=(page_id,selectall)
        self._cr.execute("SELECT URL,NAME FROM TORRENTS WHERE PAGE_ID=?"+append,par)
        return self._cr.fetchall()

    def getPages(self):
        self._cr.execute("SELECT OID,URL,STAT FROM PAGES")
        return self._cr.fetchall()
    def close(self):
        try:
            self._cn.close()
            self._cn=None
            self._cr=None
        except:
            pass
