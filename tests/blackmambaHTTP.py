#!/usr/bin/python
import datetime,random
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','lib'))
from looper import iterutil,clients

params = iterutil.chain(
    iterutil.dict_zip(
        method = iterutil.repeat('GET'),
        url = iterutil.concat(
            iterutil.repeat('http://'),
            iterutil.repeat('127.0.0.1'),
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

class Check(object):
    '''
    A simple HTTP response check
    '''
    def check(self,request,response):
        print response

class MyTestCase(Check,clients.blackmambaHTTP.TestCase):
    pass

test = MyTestCase(params)
test.run()
