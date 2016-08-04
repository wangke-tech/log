#coding=utf-8
import urllib
import urllib2
import re
from collections import defaultdict
import time
import logging
import logging.handlers

def timeit(args):
    def _timeit(func):
        def __timeit():
            print args
            start_time = time.time()
            func()
            print time.time() - start_time
        return __timeit
    return _timeit

def getResult():
    try:
        with open('/home/michael/0.flow.log') as f:
            text = f.read()
            pattern = re.compile('|time=(.*?).*?sql=\"select.*?from (.*?) .*?',re.S)
            items = re.findall(pattern,text)
            result = defaultdict(list)
            count = defaultdict(list)
            time = defaultdict(int)

            for item in items:
                print item
                count[item[1].strip()] += 1
                time[item[1]].append(item[0])
                #print item
            #for k1,c,k2,t in count.iteritems(),time.iteritems():
            #    print k1==k2
            #    print c,t
            #    result.append({'name':k1,'count':c,'time':max(t)})
                
            #result = sorted(result.iteritems(),key=lambda d:d['time'],reverse=True)
            #print result
            print count,time
    except Exception as e:
        print e 
        

@timeit('single processing ...')
def test_single():
    getResult()


@timeit('multiply processing ...')
def test_multiply():
    from multiprocessing import Process
    p = Process(target=getResult)
    p.start()
    p.join()

@timeit('m2 ...')
def test_multiply2():
    from multiprocessing import Pool as ThreadPool
    pool = ThreadPool(processes=2)
    pool.apply_async(getResult)
    pool.close()
    pool.join()

        
    
if '__main__' == __name__:
    test_single()
    #test_multiply()
    #test_multiply2()
    
    
    
