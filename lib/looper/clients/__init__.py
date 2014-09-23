#!/usr/bin/env python
'''
A test case generation framework
'''
from . import SimpleHTTP
__all__ = ['SimpleHTTP']

try:
    from . import blackmambaHTTP
    __all__.append('blackmambaHTTP')
except ImportError as e:
    print e
    pass

try:
    from . import geventHTTP
    __all__.append('geventHTTP')
except ImportError:
    pass

