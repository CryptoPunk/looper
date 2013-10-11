#!/usr/bin/env python
'''
A test case generation framework
'''
from . import iterutil
__all__ = ['iterutil','BaseTestCase']
try:
    from . import SimpleHTTP
    __all__.append('SimpleHTTP')
except Exception:
    pass
try:
    from . import blackmambaHTTP
    __all__.append('blackmambaHTTP')
except Exception:
    pass

class BaseTestCase():
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

