import urllib2,urllib,httplib, re, urlparse,os
def get_torrent_string(url):
    """
    input:  url the html url
    return: title the file name
            string the content in torrent
    """
##    ph=urlparse.urlparse(url)
##    port=80 if ph.port==None else ph.port
##    hhc=httplib.HTTPConnection(ph.netloc, port)
##    hhc.request("GET", ph.path,None, {})
##    rst=hhc.getresponse()
##    ss=rst.read()
##      hhc.close()  
    request=urllib2.Request(url,headers={"user-agent":"Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0"})
    ss=urllib2.urlopen(request).read()  
    param={}
    getPostPath=re.compile(r'<form.*action="(?P<action>.*?)"')
    getElse=re.compile(r'value="(?P<value>.*?)"\s*id="(?P<id>.*?)"\s*name="(?P<name>.*?)"')
    action=getPostPath.search(ss)
    if not action:
        return None
    actpath=urlparse.urlparse(urlparse.urljoin(url, action.group("action"))).path
    for s in re.findall(r'<input\stype="hidden".*?>', ss, re.S):
        g=getElse.search(s)
        param[g.group("name")]= g.group("value")
    cparam=urllib.urlencode(param)
    header={}
    header['user-agent']="Mozilla/4.0"
    header['content-type']="application/x-www-form-urlencoded"
    header['host']=ph.netloc
    header['connection']='keep-alive'
    hhc=httplib.HTTPConnection(ph.netloc, 80)
    hhc.request("POST", actpath, cparam, header)
    rsp=hhc.getresponse()
    content=rsp.read()
    title=rsp.getheader("content-disposition").split('"')[1]
    return (title, content)
def torrent_download(url,filepath,name=None,debug=False):
    rlt=True
    try:
        n, a=get_torrent_string(url)
        if name:
            n=name
        absname=os.path.join(filepath,n)
        if os.path.exists(absname):
            return url,rlt
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(absname, 'wb') as f:            
            f.write(a)
    except:
        rlt=False
        if debug:
            print "Failed To Get Torrent"+url
    finally:
        return url,rlt
def img_download(url,to_path,affix=""):
    fname=os.path.join(to_path,affix+url.split("/")[-1])
    state=False
    if  os.path.exists(fname):
       return  (fname,url,True)
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    try:
        text=urllib2.urlopen(urllib2.Request(url,headers={"user-agent":"Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0"})
    ).read()
        with open(fname,'wb') as f:
            f.write(text)
        state=True    
    finally:
        return (fname,url,state)
if __name__=="__main__":
##    try:
##        n, a=torrent_download('http://www3.kidown.com/bt5/file.php/MV4B1RJ.html',"d:\\sdxffd")
##    except:
##        pass
    print img_download("http://img789.com/images/2013/09/13/092G6bQ.jpg","d:\\oxx","a_")
    
