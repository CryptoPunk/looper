#!/usr/bin/env python
'''
A test case generation framework
'''
from . import BaseTestCase,iterutil
import urllib2

class Test():
    '''
    A simple HTTP test runner
    '''
    def execute(self,url,method='GET',headers={},body=None):
        urlreq = urllib2.Request(url, headers=headers)
        urlreq.get_method = lambda: method
        if body is not None:
            urlreq.add_data(body)

        retval = None
        try:
            resp = urllib2.urlopen(urlreq)
            retval = {
                'req_url': url,
                'req_method': method,
                'req_headers': headers,
                'req_body': body,
                'resp_code': resp.getcode(),
                'resp_headers': resp.headers.dict,
                'resp_body': resp.read()
            }
        except urllib2.URLError as resp:
            retval = {
                'req_url': url,
                'req_method': method,
                'req_headers': headers,
                'req_body': body,
                'resp_code': resp.getcode(),
                'resp_headers': resp.headers.dict,
                'resp_body': resp.read()
            }
        
        return retval

class Check():
    '''
    A simple HTTP response check
    '''
    def check(self,
        req_url,req_method,req_headers,req_body,
        resp_code,resp_headers,resp_body):
        if resp_code != 200:
            print "Request to %s got HTTP Error %d" % (req_url, resp_code)
            print req_body
            return False
        return True

class TestCase(Test,Check,BaseTestCase):
    '''
    A simple HTTP test case framework
    '''
    pass
