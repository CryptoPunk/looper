#!/usr/bin/env python
import sys,datetime,random,urllib2
from pprint import pprint
sys.path.append('libs')
from looper import *

    
params = iterutil.chain(
    iterutil.dict_zip(
        method = iterutil.repeat('GET'),
        url = iterutil.concat(
            iterutil.repeat('http://facebook.com/'),
            ['/login','/admin']
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

#LoggingHTTPTestCase must subclass object in order to use super()
class LoggingHTTPTestCase(SimpleHTTPTest, SimpleHTTPCheck, TestCase, object):
    def __init__(self,file_name,*args,**kwargs):
        self.fh = open(file_name,'w')
        #Continue with the next mixin
        super(LoggingHTTPTestCase, self).__init__(*args,**kwargs) 

    def check(self, req_url, req_method, req_headers, req_body, resp_code, resp_headers, resp_body):
        #Continue with the next mixin
        super(LoggingHTTPTestCase, self).check(req_url, req_method, req_headers, req_body, resp_code, resp_headers, resp_body)

        if resp_headers.has_key('set-cookie'):
            self.fh.write(resp_headers['set-cookie']+"\n")
        else:
            #pprint(resp_headers)
            self.fh.write("!!!\n")


test = LoggingHTTPTestCase('tests/cookie.log',params)

test.run()


