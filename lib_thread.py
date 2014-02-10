#-*- coding:utf8 -*-
import thread,threading
from lib_common import *
from lib_download import *
class Collect_Item:
    def __init__(self,items,lock):
        self._c=items
        self._lock=lock
        self._len=len(self._c)
        self._counter=0
    def length(self):
        return self._len
    def get(self):
        self._lock.acquire()
        if self._counter==self._len:
            self._lock.release()
            return None
        else:
            rt=self._c[self._counter]
            self._counter+=1
            self._lock.release()
            return (self._counter-1,rt)

class Thread_Pic(threading.Thread):
    def __init__(self,pics,path,database,tid,prefix):
        threading.Thread.__init__(self)
        self._pics=pics
        self._tid=tid
        self._dir=path
        self.db_instance=database
        self._prefix=prefix
    def run(self):
        while True:
            pic=self._pics.get()
            if not pic:
                return None
            else:
                imgrlt=img_download(pic[1],self._dir,self._prefix+"_")
                Common.LOCK_DB.acquire()
                self.db_instance.addImg(imgrlt[1],imgrlt[0],self._dir,int(imgrlt[2]),self._tid)
                Common.LOCK_DB.release()
    
class Thread_Item(threading.Thread):
    def __init__(self,item,path_to,database,url,pid,seperate_dir=False):
        threading.Thread.__init__(self)
        self._item=item
        self.to_dir=path_to
        self.db_instance=database
        self._url=url
        self._pid=pid
        self.seperate_dir=seperate_dir
    def run(self):
        while True:
            item=self._item.get()
            todir=self.to_dir
            if not item:
                self.db_instance.togglePageState(self._pid)
                return None
            else:
                tor_name=tor_rlt=tor_url=0
                try:
                    tor_url=item[1]["tor"]
                    tor_name=item[1]["tor"].split("/")[-1]
                except:
                    tor_name=Common.NO_TOR_NAME
                    tor_url=Common.NO_TOR_URL
                    if Common.DEBUG:
                        print "Warn:No TOR Found!"
                if self.seperate_dir:
                    todir=os.path.join(self.to_dir,tor_name)
                    os.mkdir(todir)
                print "[{0}/{1}]{2},{3} Pics".format(item[0],self._item.length(),tor_url,len(item[1].get('img',[])))
                url,rlt=torrent_download(tor_url,todir)
                if rlt:
                    tor_rlt=1
                Common.LOCK_DB.acquire()
                tid=self.db_instance.addTorrent(self._url,self._url.split("/")[-1],todir,int(tor_rlt),self._pid)
                Common.LOCK_DB.release()
                pic_lock=thread.allocate_lock()
                col_pic=Collect_Item(item[1].get("img",[]),pic_lock)
                thread_pic=[Thread_Pic(col_pic,todir,self.db_instance,tid,tor_name+"_") for i in range(Common.PIC_THREAD_NUM)]
                for tp in thread_pic:
                    tp.start()                 
        self.join()
        self.db_instance.close()
