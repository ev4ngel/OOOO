import urllib2,urllib,httplib, re, urlparse,os
from lib_common import *
def mknetshortcut(url,fname,path):
    if not fname.endswith(".url"):
        fname+=".url"
    with open(os.path.join(path,fname),'w') as f:
        f.write("[internetShortCut]\n")
        f.write("url=%s"%url)
def get_torrent_string(url):
    """
    input:  url the html url
    return: title the file name
            string the content in torrent
    """
    cxt=""
    title=""
    getPostPath=re.compile(r'<form.*action="(?P<action>.*?)"')
    getElse=re.compile(r'value="(?P<value>.*?)"\s*id="(?P<id>.*?)"\s*name="(?P<name>.*?)"')
    try:
        request=urllib2.Request(url,headers=Common.HEADER)
        cxt=urllib2.urlopen(request,timeout=5).read()
        print len(cxt)
        #del request
    except:
        if Common.DEBUG:
            print "Error:Get Tor Page %s"%url
        return (None,None)

    action=getPostPath.search(cxt)
    if not action:
        if Common.DEBUG:
            print "Error:No Action Found in %s"%url
        return (None,None)
    _actpath=urlparse.urlparse(urlparse.urljoin(url, action.group("action"))).path
    print _actpath
    param={}
    for s in re.findall(r'<input\stype="hidden".*?>', cxt, re.S):
        g=getElse.search(s)
        param[g.group("name")]= g.group("value")
    _cparam=urllib.urlencode(param)
    del param
    
    _header={}
    _header['user-agent']=Common.HEADER["user-agent"]
    _header['content-type']="application/x-www-form-urlencoded"
    _header['host']=urlparse.urlparse(url).netloc
    _header['connection']='keep-alive'
#try:
    hhc=httplib.HTTPConnection(header['host'], 80)
    hhc.request("POST", _actpath, _cparam, _header)
    rsp=hhc.getresponse()
    cxt=rsp.read()
    print '*'*10
    print len(cxt)
    title=rsp.getheader("content-disposition").split('"')[1]
    #del rsp
    #del hhc
#except:
    if Common.DEBUG:
        print "Error:Getting Tor Content %s"%_actpath
    #title=cxt=None
    return (title, cxt)

def torrent_download(url,filepath):
    rlt=True
    if url.find("suwpan")>0:
        mknetshortcut(url,url.split("/")[-1],filepath)
    else:
        try:
            n, a=get_torrent_string(url)
            absname=os.path.join(filepath,n)
            if os.path.exists(absname):
                if Common.DEBUG:
                    print "Warn:Exist TOR %s"%absname
                return url,rlt
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            with open(absname, 'wb') as f:            
                f.write(a)
        except:
            rlt=False
            if Common.DEBUG:
                print "Error:Getting Tor "+url
    return url,rlt
def img_download(url,to_path,prefix=""):
    fname=os.path.join(to_path,prefix+url.split("/")[-1])
    state=False
    if  os.path.exists(fname):
        if Common.DEBUG:
            print "Warn:Exist IMG %s"%fname
        state=True
    else:
        if not os.path.exists(to_path):
            os.makedirs(to_path)
        try:
            text=urllib2.urlopen(urllib2.Request(url,headers=Common.HEADER),timeout=10).read()
            with open(fname,'wb') as f:
                f.write(text)
            state=True
        except:
            if Common.DEBUG:
                print "Error:Reading IMG %s"%url
    return (fname,url,state)
if __name__=="__main__":
    pass
    
