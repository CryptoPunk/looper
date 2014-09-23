import blackmamba
from urlparse import urlparse,urlunparse
from .. import BaseTestCase
from . import httputil

class Test(object):
    '''
    BlackMamba HTTP test runner
    '''
    def execute(self, url, method='GET', headers={},body=None):
        request = httputil.RawHTTPRequest(url,method,headers,body)
        response = None
        try:
            yield blackmamba.resolve(request.host)
            yield blackmamba.connect(request.host, request.port)
            yield blackmamba.write(str(request))
            response = yield blackmamba.read()
            yield blackmamba.close()
        except blackmamba.SockError as e:
            response = e
        
        self.check(
            request=request,
            response=httputil.RawHTTPResponse(response)
        )
    
class Check(object):
    '''
    Simple BlackMamba HTTP response handler
    '''
    def check(self,request,response):
        print response

class TestCase(Test,Check,BaseTestCase):
    '''
    blackmamba HTTP test case wrapper
    '''
    def requestGenerator(self):
        for request in self.test_cases:
            yield self.execute(**request)

    def run(self):
        blackmamba.run(self.requestGenerator())

