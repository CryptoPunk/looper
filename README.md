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
#!/usr/bin/python
# These tests utilize the fuzzdb files
import sys,base64
from looper import *

def int_tests(maxint=sys.maxint):
    return genutil.ifilter(lambda x: x<maxint,
        genutil.imap(int,
            genutil.readfiles(
                'attack-payloads/integer-overflow/decimal_numbers.txt'
                )
            )
        )

def string_tests():
    return genutil.chain(
        genutil.readfiles(
            'attack-payloads/riak_tests',
            'attack-payloads/all-attacks/all-attacks-unix.txt',
            'attack-payloads/path-traversal/traversals-8-deep-exotic-encoding.txt',
            'attack-payloads/regex/patterns',
            ),
        genutil.imap(base64.b64decode,
            genutil.readfiles(
                'attack-payloads/regex/strings.b64'
                )
            ),
        )
```

 

