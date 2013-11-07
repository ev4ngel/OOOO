import urllib2,urllib,httplib, re, urlparse
def torrent_download(host):
    ph=urlparse.urlparse(host)
    port=80 if ph.port==None else ph.port
    print port
    hhc=httplib.HTTPConnection(ph.netloc, 80)
    hhc.request("GET", ph.path,None, {})
    rst=hhc.getresponse()
    ss=rst.read()
    hhc.close()    
    param={}
    getPostPath=re.compile(r'<form.*action="(?P<action>.*?)"')
    getElse=re.compile(r'value="(?P<value>.*?)"\s*id="(?P<id>.*?)"\s*name="(?P<name>.*?)"')
    action=getPostPath.search(ss)
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
    txt=rsp.read()
    title=rsp.getheader("content-disposition").split('"')[1]
    return (title, txt)
def write_torrent(url,filepath):
    try:
        n, a=torrent_download(url)
        with open(filepath+"/"+n, 'wb') as f:
            f.write(a)
    except:
        print "Failed to get torrent"
    
if __name__=="__main__":
    try:
        n, a=torrent_download('http://www3.kidown.com/bt5/file.php/MV4B1RJ.html')
        with open(n, 'wb') as f:
            f.write(a)
    except:
        pass
    
