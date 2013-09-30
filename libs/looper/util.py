#!/usr/bin/env python
from itertools import *

def concat(*args):
    '''
    return a generator which concatinate all of the elements at each ordinal

    Example:
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
    for path in args:
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

def dict_zip(d=None, **kwargs):
    '''
    A version of itertools.izip for dictionaries

    this creates a generator which takes in a hash where each value is an array
      returns: a hash built by zipping of these values

    Example:
        A = {"a":[1,2],"b":['x','y']}
        r_1 = util.hash_product(A)
        r_2 = util.hash_product(a=[1,2], b=['x','y'])
        # r_1 == r_2
        
        pprint([x for x in r_1])

        #OUTPUT    
        [{'a': 1, 'b': 'x'},
         {'a': 2, 'b': 'y'}]

    '''
    if d is None:
        d = kwargs
    k = d.keys()
    for y in izip(*d.values()):
        ret = {}
        for x in range(len(k)):
            ret[k[x]] = y[x]
        yield ret

def repeat_f(f, n=0, args=[], kwargs={}):
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
    print args
    print kwargs
    i = 0
    while n == 0 or i < n:
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
