#!/usr/bin/env python
'''
A test case generation framework
'''
from . import iterutil
import urllib2


__all__ = ['iterutil','SimpleHTTPTest','SimpleHTTPCheck','TestCase', 'SimpleHTTPTestCase']

class TestCase():
    '''
    The base test case
    '''
    def __init__(self,test_cases):
        '''
        test_cases must be an iterable, which returns a dict, this dict is used as the keyword
        '''
        self.test_cases = test_cases

    def run(self):
        '''
        Run the execute method on each item in the iterable applying the params as kwargs.
        Run the check method applying the result from the execute method as kwargs
        '''
        for params in self.test_cases:
            result = self.execute(**params)
            self.check(**result)

    def execute(self,**kwargs):
        '''
        Stub execute method. Raises an Exception
        '''
        raise Exception('BaseTest.execute() must be overriden')

    def check(self,**kwargs):
        '''
        Stub check method. Raises an Exception
        '''
        raise Exception('BaseTest.check() must be overriden')

class SimpleHTTPTest():
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

class SimpleHTTPCheck():
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

class SimpleHTTPTestCase(SimpleHTTPTest,SimpleHTTPCheck,TestCase):
    '''
    A simple HTTP test case framework
    '''
    pass
