from urlparse import urlparse

class HTTPRequest(object):
    host = None
    url = None
    version = None
    port = None
    scheme = None
    method = None
    path = None
    headers = []
    body = None

    def __init__(self):
        raise NotImplemented("interface description")

class HTTPResponse(object):
    version = None
    status = None
    reason = None
    headers = []
    body = None

    def __init__(self):
        raise NotImplemented("Base Implementation")

    def get_header(self,header,caseinsensitive=True):
        raise NotImplemented("Base Implementation")

class RawHTTPRequest(HTTPRequest):
    def __init__(self,data):
        pos = self.readStatusLine(data,0)
        pos = self.readHeaders(data,pos)
        content_length = filter(lambda x: x[0].lower() == "content-length", self.headers)
        if len(content_length) == 1:
            length = int(content_length[0][1])
            self.body = data[pos:pos+length]
            pos = pos+length
        if len(content_length) > 1:
            raise ValueError("Too many content-length headers!")

        self.remainder = data[pos:]

    def __str__(self):
        buf = "%s %s HTTP/%s\r\n" % (self.method,self.path,self.version)
        for k,v in self.headers:
            if self.body is not None and self.body != "":
                buf += "%s: %s\r\n" % (k,v) 
        buf += "\r\n"
        buf += self.body
        return buf

    version = None
    port = 80
    scheme = 'http'
    method = None
    path = None
    headers = []
    body = None

    @property
    def host(self):
        self.get_header('host')

    @property
    def url(self):
        netloc = None
        host = self.host if (self.host.find(':') == -1) else "[%s]" % self.host

        if (('https' == self.scheme and 443 == self.port) or
           ('http' == self.scheme and 80 == self.port)):
            netloc = host
        else:
            netloc = "%s:%d" % (self.host,self.port)
        return urlunsplit((self.scheme,netloc,self.path,None,None))

    def readStatusLine(self,data,pos):
        # HTTP-Version SP Status-Code SP Reason-Phrase CRLF
        pos = self.readMethod(data,pos)
        pos = self.readPath(data,pos)
        pos = self.readVersion(data,pos)
        return pos

    def readMethod(self,data,pos):
        end = data[pos:].find(" ")
        self.method = int(data[pos:pos+end])
        return pos+end+1

    def readPath(self,data,pos):
        end = data[pos:].find(" ")
        self.path = data[pos:pos+end]
        return pos+end+2

    def readVersion(self,data,pos):
        if "HTTP/" != data[pos:pos+5]:
            raise ValueError("Not HTTP-Version string at %d" % pos)
        self.version = data[pos+5:pos+8]
        return pos+9


    def readHeaders(self,data,pos):
        cur = pos
        end = data[cur:].find("\r\n")
        while end != 0:
            header = data[cur:cur+end]
            cur = cur+end+2
            end = data[cur:].find("\r\n")
            while data[cur] in (" ","\t"):
                header += self.data[cur:cur+end]
                cur = cur+end+2
                end = data[cur:].find("\r\n")
            self.headers.append(header.split(': ',1))
        return cur+2           

    def get_header(self,header,caseinsensitive=True):
        for k,v in self.headers:
            if caseinsensitive:
                if k.lower() == header.lower():
                    return v
            else:
                if k.lower() == header.lower():
                    return v


class RawHTTPResponse(HTTPResponse):
    def __init__(self,data):
        pos = self.readStatusLine(data,0)
        pos = self.readHeaders(data,pos)
        content_length = filter(lambda x: x[0].lower() == "content-length", self.headers)
        if len(content_length) == 1:
            length = int(content_length[0][1])
            self.body = data[pos:pos+length]
            pos = pos+length
        if len(content_length) > 1:
            raise ValueError("Too many content-length headers!")

        self.remainder = data[pos:]

    def __str__(self):
        buf = "HTTP/%s %s %s\r\n" % (self.version,self.status,self.reason)
        for k,v in self.headers:
            buf += "%s: %s\r\n" % (k,v) 
        buf += "\r\n"
        buf += self.body
        return buf


    def readStatusLine(self,data,pos):
        # HTTP-Version SP Status-Code SP Reason-Phrase CRLF
        pos = self.readVersion(data,pos)
        pos = self.readStatusCode(data,pos)
        pos = self.readReasonPhrase(data,pos)
        return pos

    def readStatusCode(self,data,pos):
        self.status = int(data[pos:pos+4])
        return pos+4

    def readVersion(self,data,pos):
        if "HTTP/" != data[pos:pos+5]:
            raise ValueError("Not HTTP-Version string at %d" % pos)
        self.version = data[pos+5:pos+8]
        return pos+9

    def readReasonPhrase(self,data,pos):
        end = data[pos:].find("\r\n")
        self.reason = data[pos:pos+end]
        return pos+end+2

    def readHeaders(self,data,pos):
        self.headers = []
        cur = pos
        end = data[cur:].find("\r\n")
        while end != 0:
            header = data[cur:cur+end]
            cur = cur+end+2
            end = data[cur:].find("\r\n")
            while data[cur] in (" ","\t"):
                header += self.data[cur:cur+end]
                cur = cur+end+2
                end = data[cur:].find("\r\n")
            self.headers.append(header.split(': ',1))
        return cur+2           

    def get_header(self,header,caseinsensitive=True):
        for k,v in self.headers:
            if caseinsensitive:
                if k.lower() == header.lower():
                    return v
            else:
                if k.lower() == header.lower():
                    return v


class ParamHTTPRequest(HTTPRequest):
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

