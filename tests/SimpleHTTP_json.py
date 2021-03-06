#!/usr/bin/env python
import datetime,random,json
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','lib'))
from looper import iterutil,clients
    
params = iterutil.chain(
    iterutil.dict_zip(
        method = iterutil.repeat('POST'),
        url = iterutil.repeat('http://127.0.0.1/api'),
        headers = iterutil.dict_zip({
            'User-Agent': iterutil.repeat('SecurityInnovation/0.0.1/Looper'),
            'Accept': iterutil.repeat("application/json"),
            'Date': iterutil.repeat_f(lambda: datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
            'Content-Type': iterutil.repeat('application/json'),
        }),
        body = iterutil.imap(
            json.dumps,
            iterutil.dict_zip({
                'int': range(10),
                'rand_str': iterutil.repeat_f(lambda:"%032x" % random.getrandbits(128)),
            })
        )
    ),
)

test = clients.SimpleHTTP.TestCase(params)
test.run()
