#-*- encoding:utf8 -*-
import sqlite3
import os
class axDB:
    def __init__(self,path=os.getcwd()):
        self._path=path
        self._dbname="ax.db"
        self.initall()
    def initall(self):
        abspath=os.path.exists(os.path.join(self._path,self._dbname)):
        if not os.path.exists(abspath):
            self._cn=sqlite3.connect(abspath)
            self._cr=self._cn.cursor
            
