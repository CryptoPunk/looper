#!/usr/bin/python2
import traceback
from .. import BaseTestCase

class Spider():
    '''
    Spider is simple multilevel response-checking mixin, perfect for scraping pages and injecting
    content from pages back in in to the input queue.
    '''

    scrapers = []
    callbacks = []

    logfile = None
    loglevel = 0

    LOG_INFO = 0
    LOG_ERROR = 1
    LOG_DEBUG = 2


    def log(self,msg,level):
        if isinstance(msg,Exception):
            msg = traceback.format_exc(msg)
        else:
            msg = str(msg).strip()
        logstr = ["!INFO!  ","!ERROR! ","!DEBUG! "]
        if level >= self.loglevel:
            msg = "\n".join([logstr[level] + line for line in msg.split("\n")])
            self.logfile.write(msg + "\n")
            self.logfile.flush()

    def install_scraper(self,scraper):
        self.scrapers.append(scraper)

    def add_callback(self,callback):
        self.callbacks.append(callback)

    def check(self,request,response):
        '''
            request:  a looper.clients.httputil.HTTPRequest style object
            response: a looper.clients.httputil.HTTPResponse style object
        '''

        self.log(request.url,ContentSpider.LOG_DEBUG)
        for scraper in self.scrapers:
            if scraper.canparse(request,response):
                try:
                    for resource in scraper(request,response):
                        for callback in self.callbacks:
                            callback(resource)
                except Exception as e:
                    if self.log is not None:
                        self.log(e,ContentSpider.LOG_ERROR)
                        self.log(request,ContentSpider.LOG_ERROR)
                        self.log(response,ContentSpider.LOG_ERROR)

