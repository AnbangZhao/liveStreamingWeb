import urllib
import urllib2

def sendReq (uri, params):
    url = "https://p2p-meta-server.appspot.com/" + uri
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    rsp = urllib2.urlopen(req)
    retCode = rsp.getcode()
    content = rsp.read()
    rsp.close()
    print 'return code', retCode
    return (retCode, content)