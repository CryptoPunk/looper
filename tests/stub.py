#!/usr/bin/env python

from pprint import pprint
import sys
sys.path.append('libs')

from looper import *

import urllib2,ssl,httplib,socket,json,random,base64

proxy = "127.0.0.1:8080"
USER_AGENT = "Looper/0.0.0.1/TestingFramework"

proxy = urllib2.ProxyHandler({'http': proxy, 'https': proxy})
opener = urllib2.build_opener(proxy)

urllib2.install_opener(opener)

def testcase(params,run,check):
    return util.izip(
            params,
            util.repeat(run),
            util.repeat(check))


## MAIN ##
import datetime
import commonTests

def userid_tests():
    return iter([0,1,2,3,4,5,6])

def response_check(params,resp):
    if resp['code'] != 200:
        print "X-Request-Id: %s got HTTP Error %d" % (params['headers']["X-Request-Id"], resp['code'])
        print params['message']
        return False

    pprint(resp)
    result_code = True

    #Do Check

    return result_code

def make_request(params):
    formatted_url = params['host']+params['uri']
    headers = params['headers']
    message = params['message']
    method = params['method']
    postData = None


    if method == "POST":
        if   headers["Content-Type"] == "application/x-protobuf":
            postData = message.SerializeToString()
        elif headers["Content-Type"] == "application/json":
            postData = json.dumps(pb2json(message))
        else:
            next

    urlreq = urllib2.Request(formatted_url, headers=headers)

    if method is not None:
        urlreq.get_method = lambda: method

    if postData is not None:
        urlreq.add_data(postData)

    try:
        resp = urllib2.urlopen(urlreq)
        retval = {
            'code': resp.getcode(),
            'headers': resp.headers.dict,
            'body': resp.read() }
        return retval

    except urllib2.URLError, resp:
        retval = {
            'code': resp.getcode(),
            'headers': resp.headers.dict,
            'body': resp.read() }
        return retval

    #TODO: Throw major error!
    return None


host = "https://example.com"

test_cases = testcase(
    util.chain(
        util.hash_zip(
            method = util.repeat('GET'),
            host = util.repeat(host),
            uri = ["/uri","/uri1"],
            headers = util.hash_zip({
                'User-Agent': util.repeat(USER_AGENT),
                'Accept': util.repeat("application/json"),
                'Date': util.repeat_f(lambda: datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
                'X-Request-Id': util.repeat_f(lambda:"%032x" % random.getrandbits(128)),
                'Content-Type': util.repeat('application/x-protobuf'),
                }),
            message=util.repeat(None),
            ),
        ),
    make_request,
    response_check,
    )

for (params,run,check) in test_cases:
    result = run(params)
    check(params,result)
