#!/usr/bin/env python
import datetime,random,urllib2
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','lib'))
from looper import iterutil,clients

params = iterutil.chain(
    iterutil.dict_zip(
        method = iterutil.repeat('GET'),
        url = iterutil.concat(
            iterutil.repeat('http://'),
            iterutil.repeat('example.com'),
            ["/uri","/uri1"],
        ),
        headers = iterutil.dict_zip({
            'User-Agent': iterutil.repeat('SecurityInnovation/0.0.1/Looper'),
            'Accept': iterutil.repeat("application/json"),
            'Date': iterutil.repeat_f(lambda: datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
            'X-Request-Id': iterutil.repeat_f(lambda:"%032x" % random.getrandbits(128)),
            'Content-Type': iterutil.repeat('application/json'),
        }),
    ),
)

test = clients.SimpleHTTP.TestCase(params)

#Install a proxy before running
proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
test.run()
