from TorCtl import TorCtl
import urllib2

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}

def request(url):
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http": "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
    _set_urlproxy()
    request = urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()

def renew_connection():
    conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="Password12")
    conn.send_signal("NEWNYM")
    conn.close()

if __name__ == '__main__':
    renew_connection()
    print request("http://curlmyip.com/")
