import geventhttpclient
from urlparse import urlparse
from .. import BaseTestCase
from . import httputil

class Test(object):
    '''
    geventhttpclient HTTP test runner
    '''

    def execute(self, url, method='GET', headers={},body=None):
        request = httputil.HTTPRequest(url,method,headers,body)
        http = geventhttpclient.HTTPClient(request.host,request.port)
        response = http.request(request.method, request.path, body=request.body, headers=request.headers)

        self.check(
            request=request,
            response=response
        )
    
class Check(object):
    '''
    geventhttpclient HTTP response handler
    '''

    def check(self,request,response):
        print response

class TestCase(Test,Check,BaseTestCase):
    '''
    geventhttpclient test case wrapper
    '''

    def run(self):
        for request in self.test_cases:
            pool.spawn(self.execute, **request)
            self.execute(**request)

