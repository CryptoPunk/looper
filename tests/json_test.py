#!/usr/bin/env python
import sys,datetime,random,json
from pprint import pprint
sys.path.append('lib')
from looper import iterutil,SimpleHTTP
    
params = iterutil.chain(
    iterutil.dict_zip(
        method = iterutil.repeat('POST'),
        url = iterutil.repeat('http://seattlenetworks.com/api'),
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

test = SimpleHTTP.TestCase(params)
test.run()


