#!/usr/bin/env python
'''
Itertools extension for generating large and complex datasets using generators.

    Infinite iterators:
    count([n]) --> n, n+1, n+2, ...
    cycle(p) --> p0, p1, ... plast, p0, p1, ...
    repeat(elem [,n]) --> elem, elem, elem, ... endlessly or up to n times
    repeat_f(f, n=None, args=[], kwargs={}) -> f(*args,**kwargs), f(*args,**kwargs), ... endlessly or up to n times
    
    Iterators terminating on the shortest input sequence:
    chain(p, q, ...) --> p0, p1, ... plast, q0, q1, ... 
    compress(data, selectors) --> (d[0] if s[0]), (d[1] if s[1]), ...
    dropwhile(pred, seq) --> seq[n], seq[n+1], starting when pred fails
    groupby(iterable[, keyfunc]) --> sub-iterators grouped by value of keyfunc(v)
    ifilter(pred, seq) --> elements of seq where pred(elem) is True
    ifilterfalse(pred, seq) --> elements of seq where pred(elem) is False
    islice(seq, [start,] stop [, step]) --> elements from
           seq[start:stop:step]
    imap(fun, p, q, ...) --> fun(p[0], q[0]), fun(p[1], q[1]), ...
    kwimap(fun, p, foo=q) -> fun(p[0], foo=q[0]), fun(p[0], foo=q[0]), ...
    starmap(fun, seq) --> fun(*seq[0]), fun(*seq[1]), ...
    tee(it, n=2) --> (it1, it2 , ... itn) splits one iterator into n
    takewhile(pred, seq) --> seq[0], seq[1], until pred fails
    izip(p, q, ...) --> (p[0], q[0]), (p[1], q[1]), ... 
    izip_longest(p, q, ...) --> (p[0], q[0]), (p[1], q[1]), ... 
    concat(p,q,...) --> (p[0]+q[0]), (p[1]+q[1]), ... 
    dict_zip(foo=p,bar=q) {"foo": p[0], "bar": q[0]}, {"foo": p[1], "bar": q[1]}, ... 
    
    Combinatoric generators:
    product(p, q, ... [repeat=1]) --> cartesian product
    dict_product(foo=p,bar=q) --> cartesian product: {"foo": p[x], "bar": q[y]}
    permutations(p[, r])
    combinations(p, r)
    combinations_with_replacement(p, r)

    Utility generators:
    readfiles(file_a,file_b,...) --> reads file_a line by line, then file_a line by line...
'''
from itertools import *
__all__ = '''
chain
combinations
combinations_with_replacement
compress
count
cycle
dropwhile
groupby
ifilter
ifilterfalse
imap
islice
izip
izip_longest
permutations
product
starmap
repeat
takewhile
concat
readfiles
dict_product
dict_zip
kwimap
repeat_f
'''.strip().split('\n')


def concat(*args):
    '''
    return a generator which concatinate all of the elements at each ordinal

    Example::
        A = ['1','2']
        B = ['a','b']
        r = util.concat(A,B)

        print [x for x in r]

        #OUTPUT
        ['1a', '2b']
    '''
    cont = True
    iterators = [arg.__iter__() for arg in args] 
    while cont:
         try:
            retval = None
            for arg in iterators:
                if retval is None:
                    retval = arg.next()
                else:
                    retval = retval + arg.next()
            yield retval
                
         except StopIteration:
            cont = False

def readfiles(*filenames):
    '''
    Create a generator to return each line of the specified files in order
    Example:
        files = readfiles("/path/to/file1","/path/to/file2")
        for line in files:
            print line

        #prints file1, then file2
    '''
    for path in filenames:
        for line in open(path,"rb"):
            yield line.strip()

def dict_product(d=None,**kwargs):
    '''
    A version of itertools.product for dictionaries

    this creates a generator which takes in a hash where each value is an array
      returns: a hash built using the product of these values

    can also take kwargs as the source dictionary

    Example:
        A = {"a":[1,2],"b":['x','y']}
        r_1 = util.hash_product(A)
        r_2 = util.hash_product(a=[1,2], b=['x','y'])
        # r_1 == r_2

        pprint([x for x in r_1])

        #OUTPUT    
        [{'a': 1, 'b': 'x'},
         {'a': 1, 'b': 'y'},
         {'a': 2, 'b': 'x'},
         {'a': 2, 'b': 'y'}]

    '''
    if d is None:
        d = kwargs
    k = d.keys()
    for y in product(*d.values()):
        ret = {}
        for x in range(len(k)):
            ret[k[x]] = y[x]
        yield ret

def dict_zip(**kwargs):
    '''
    A version of itertools.izip for dictionaries

    this creates a generator which takes in a hash where each value is an array
      returns: a hash built by zipping of these values

    Example:
        A = {"a":[1,2],"b":['x','y']}
        r = util.hash_product(a=[1,2], b=['x','y'])
        
        pprint([x for x in r])

        #OUTPUT    
        [{'a': 1, 'b': 'x'},
         {'a': 2, 'b': 'y'}]

    '''
    k = kwargs.keys()
    for v in izip(*kwargs.values()):
        yield dict([(k[x],v[x]) for x in range(len(k))])

def kwimap(f, *args, **kwargs):
    '''
    like imap, but pass kwargs as well.

    Example:
        def test(*args,**kwargs):
            return "args: %s, kwargs: %s" % (repr(args),repr(kwargs))
            
        generator = iterutil.kwimap(test,
            [1,2,3],
            [4,5,6],
            foo=['a','b','c'],
            bar=['x','y','z'])

        for result in generator:
            print result

        #OUTPUT

        args: (1, 4), kwargs: {'foo': 'a', 'bar': 'x'}
        args: (2, 5), kwargs: {'foo': 'b', 'bar': 'y'}
        args: (3, 6), kwargs: {'foo': 'c', 'bar': 'z'}
    '''
    k = kwargs.keys()
    for v in izip(*args+tuple(kwargs.values())):
        map_ar = [v[x] for x in range(len(args))]
        map_kw = dict([(k[x-len(args)],v[x]) for x in range(len(args),len(args)+len(k))])
        yield f(*map_ar,**map_kw)
    

def repeat_f(f, n=None, args=[], kwargs={}):
    '''
    repeatedly calls function f, up to n times with arguments *args and **kwargs
    Like map, but repetitive

    Example:
        import string,random

        rand_string = lambda c,n: ''.join(random.choice(c) for x in range(n))
        r = repeat_f(rand_string,args=[string.uppercase,32])
        for x in r:
            print x

        #OUTPUT    
        NUQGMQEGKUMOKELVWUXIEPCPDWXCVOIN
        ZLBQPKDLOSGMEVTBWTLYOSIOIVIWONKR
        CSQKLSJTWRXNHJVPBQIAJWUYKURVTGWE
        ZYEDVFKMTXTRXDOYJUWKOXDZJPLEHUYW
        RHNIOVLVNTPTAHSZLXCVQAPJESGNJQTA
        UZAXQBXXVZOCOFATSFVUSACLDOXBNTCJ
        PDWRURNHFYFQCFDUEDWMYAIQDMRPYQPT
        IVFAINVWSOCADGIGGDEOHXWNGKDISYSY
        LWUOYSPQHMMLTUQUCSDBGKKUDRQKQFFW
        IMPMQNAYSONYKZYIKCIINWHVEOYGRGSG
        LTVJTDLYNBCVECPCAYCAKXTWQRSWMNGQ
        LBVJCKCAOOUNYNFLGUUAHKFDNEGBSOPS
        GNYNJIWLUVESIFARNZCWZWKQUYIRLCFT
        OTVNJFKURUPMDXOJRNKWNLKMIPKUSZOC
        EUXOURTZYYCJSHSAOCIYKVXXHQKBAKKM
        NYCGNDFLKFWPADZYEARDUHPCSHMZJCDB
        ...

    '''
    i = 0
    while n is None or i < n:
        i+=1
        yield f(*args, **kwargs)

if __name__ == "__main__":
    import string,random
    rand_string = lambda c,n: ''.join(random.choice(c) for x in range(n))
    r = repeat_f(rand_string,args=[string.uppercase,32])
    for x in r:
        print x

#    for f in dict_zip({"a":[1,2,3],"b":repeat(2),"c":repeat(3)}):
#        print f
