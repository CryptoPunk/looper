import blackmamba
from urlparse import urlparse
from . import BaseTestCase

class HTTPRequest:
    '''
    Internal convenience class to generate an HTTP Request
    '''
    request_line = b"%s %s HTTP/1.1\r\n"
    headers = {}
    def __init__(self, url, method='GET', headers={},body=None):
        # parse the URL into a form we can create a GET request with
        p = urlparse(url)
        self.method = method
        self.scheme = p.scheme
        self.host = p.hostname.strip()
        self.port = 443 if self.scheme == 'https' else 80
        self.port = p.port if p.port else self.port
        self.path = p.path + '?' + p.query if p.query else p.path
        self.path = '/' if not p.path else self.path
        self.headers = dict([("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")]+self.headers.items())
        self.body = body

    def __str__(self):
        # populate all the header format strings and join everything together
        retval  = self.request_line % (self.method, self.path)
        if not self.headers.has_key("Host"):
            retval += b"Host: %s\r\n" % self.host

        retval += '\r\n'.join([b"%s: %s" % kv for kv in self.headers.items()])
        retval += '\r\n'

        if self.body is not None:
            if not self.headers.has_key("Content-Length"):
                retval += b"Content-Length: %d\r\n" % len(str(self.body))
            retval += '\r\n'
            retval += str(self.body)
        else:
            retval += '\r\n'

        return retval

class Test():
    '''
    BlackMamba HTTP test runner
    '''
    def execute(self, url, method='GET', headers={},body=None):
        request = HTTPRequest(url,method,headers,body)
        response = None
        try:
            # to resolve DNS asynchronously, call resolve() prior to connect()
            yield blackmamba.resolve(request.host)
            yield blackmamba.connect(request.host, request.port)
            yield blackmamba.write(str(request))
            response = yield blackmamba.read()
            # close the connection
            yield blackmamba.close()
        except blackmamba.SockError as e:
            response = e

        self.check(
            request=request,
            response=response
        )
    
class Check():
    '''
    Simple BlackMamba HTTP response handler
    '''
    def check(self,request,response):
        print response

class TestCase(Test,Check,BaseTestCase,object):
    '''
    blackmamba HTTP test case wrapper
    '''
    def requestGenerator(self):
        for request in self.test_cases:
            yield self.execute(**request)

    def run(self):
        blackmamba.run(self.requestGenerator())

