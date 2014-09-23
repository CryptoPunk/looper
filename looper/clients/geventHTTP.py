import geventhttpclient
import gevent
import gevent.pool
from urlparse import urlparse
from .. import BaseTestCase
from .. import iterutil
from . import httputil

class geventHTTPResponse(httputil.HTTPResponse): #TODO: geventhttpclient parser does not keep data integrity
    def __init__(self,response):
        self.status = response.status_code
        self.version = response.version
        self.reason = None # missing in geventhttpclient
        self.headers = response.items()
        self.body = response.read()
        self.remainder = None
    def __repr__(self):
        return "geventResponse(%s)" % repr(self.__dict__)

class TestCase(BaseTestCase):
    '''
    geventhttpclient test case wrapper
    '''

    def execute(self, test_cases,concurrency):
        default_params = {"method":'GET', "headers":{},"body":None}.items()
        for params in test_cases:
            p = dict(default_params + params.items())
            request = httputil.ParamHTTPRequest(p['url'],p['method'],p['headers'],p['body'])
            enable_ssl = request.scheme.lower() == "https"
            ssl_options = None
            if enable_ssl == True:
                ssl_options = {'ssl_version':3}
            client = geventhttpclient.HTTPClient(
                request.host,
                port=request.port,
                ssl=enable_ssl,
                ssl_options=ssl_options
                )
            response = client.request(request.method, request.path, body=request.body, headers=request.headers)
            client.close()

            self.check(
                request=request,
                response=geventHTTPResponse(response)
            )

    def run(self, workers=20):
        pool = gevent.pool.Pool(workers)
        for i in range(workers):
            pool.spawn(self.execute, iterutil.gevent_iterlock(self.test_cases), concurrency=workers)
        pool.join()
