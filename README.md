# looper

This module was created after getting sick of the limited functionality of burp intruder. This allows for the iteration of complex datasets in order to allow for wide coverage.

```
looper.iterutil
    Itertools extension for generating large and complex datasets using generators.

looper.TestCase
    The base test case

looper.SimpleHTTPTest
    A simple HTTP test runner

looper.SimpleHTTPCheck
    A simple HTTP response check

looper.SimpleHTTPTestCase
    A simple HTTP test case framework
```

*Example:*

```
#!/usr/bin/env python
import sys,datetime,random
from pprint import pprint
sys.path.append('libs')
from looper import *
    
def userid_tests():
    return iter([0,1,2,3,4,5,6])

params = iterutil.chain(
    iterutil.dict_zip(
        method = iterutil.repeat('GET'),
        url = iterutil.concat(
            iterutil.repeat('http://'),
            iterutil.repeat('example.com'),
            ["/uri","/uri1"],
        ),
        headers = iterutil.dict_zip({
            'User-Agent': iterutil.repeat('SecurityInnovation/0.0.1/Looper'),
            'Accept': iterutil.repeat("application/json"),
            'Date': iterutil.repeat_f(lambda: datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
            'X-Request-Id': iterutil.repeat_f(lambda:"%032x" % random.getrandbits(128)),
            'Content-Type': iterutil.repeat('application/json'),
        }),
    ),
)

test = SimpleHTTPTestCase(params)
test.run()

```
