import urllib2,urllib,httplib, re, urlparse
def get_torrent_string(url):
    """
    input:  url the html url
    return: title the file name
            string the content in torrent
    """
    ph=urlparse.urlparse(url)
    port=80 if ph.port==None else ph.port
    hhc=httplib.HTTPConnection(ph.netloc, 80)
    hhc.request("GET", ph.path,None, {})
    rst=hhc.getresponse()
    ss=rst.read()
    hhc.close()    
    param={}
    getPostPath=re.compile(r'<form.*action="(?P<action>.*?)"')
    getElse=re.compile(r'value="(?P<value>.*?)"\s*id="(?P<id>.*?)"\s*name="(?P<name>.*?)"')
    action=getPostPath.search(ss)
    print action
    if not action:
        return None
    actpath=urlparse.urlparse(urlparse.urljoin(host, action.group("action"))).path
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
    (title, content)
    return (title, content)
def torrent_download(url,filepath,name=None):
    rlt=True
    try:
        n, a=get_torrent_string(url)
        print a[:200]
        if not name:
            n=name
        with open(filepath+"/"+n, 'wb') as f:
            f.write(a)
    except:
        rlt=False
        print url
        print "Failed To Get Torrent"
    finally:
        return url,rlt
    
if __name__=="__main__":
    try:
        n, a=torrent_download('http://www3.kidown.com/bt5/file.php/MV4B1RJ.html',"d:/")
    except:
        pass
    
