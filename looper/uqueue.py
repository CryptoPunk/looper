import Queue

class UniqueQueue(Queue.Queue):
    history = set()
    buf = []
    log = None

    def __init__(self, maxsize=0, log=None):
        Queue.Queue.__init__(self,maxsize=maxsize)
        if log is not None:
            self.log = open(log,"w")

    def seen(self,item):
        self.history.add(item)

    def seen_many(self,items):
        history.union(set(items))

    def put(self,item):
        if item not in self.history:
            self.buf.append(item)
            self.history.add(item)
            if self.log is not None:
                self.log.write(repr(item)+"\n")

    def put_many(self,items):
        items = set(items)
        unseen = items - self.history
        self.history = self.history.union(unseen)
        for item in items:
            Queue.Queue.put(self,item)
            if self.log is not None:
                self.log.write(repr(item)+"\n")

    def break_threadlock(self):
        '''Must be overridden as something which will break the threadlock, allowing more data to come in.'''
        raise RuntimeWarning("Override me to prevent locking conditions")
        #yield blackmamba.timer(0) 

    def next(self):
        while True:
            try:
                item = self.get_nowait()
                return item
            except Queue.Empty as e:
                if len(self.buf) == 0 and self.unfinished_tasks == 0:
                    break
                self.put_many(self.buf)
                self.buf = []
            self.enter_loop()
        raise StopIteration()

    def __iter__(self):
        return self


