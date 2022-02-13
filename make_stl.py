#!/usr/bin/python

import regex
import sys, os

import tempfile
# OpenSCAD needs a main file, so we'll use a blank one
blank = tempfile.NamedTemporaryFile()

import multiprocessing as mp
from multiprocessing.queues import Queue
from threading import Thread

RERANGE = "\[\s*(\d+)\s*:\s*(\d+)\s*\]"
RELIST = "\[(\s*(\"?[^\s\"]+\"?)\s*,)*\s*(\"?[^\s\"]+\"?)\s*,?\s*\]"

RE = f"^module\s+([\w]+)\([^)]*\)\s*//\s*AUTO_MAKE_STL\s*({RERANGE}|{RELIST})*.*$"

modules = []


        
def build_module(q, file, module, params):
    q.put(f"{file}: {module}({', '.join(params)})\n")
    e = f"openscad -o {module}{'-' if len(params) else ''}{'-'.join(params)}.stl -D 'use <{os.path.realpath(file)}>; {module}({', '.join(params)});' '{blank.name}'"
    q.put(e+"\n")
    os.system(e)

    return True

waitlist = []

def iterate_model(file, module, parameterization, params):

    if len(parameterization) == 0:
        print(f"Queueing {file}/{module}/{params}")
        r = pool.apply_async(build_module, args=(q, file, module, params))
        waitlist.append(r)
    else:
        pop_param = parameterization[0]
        
        rangematch = regex.match(RERANGE, pop_param)
        listmatch = regex.match(RELIST, pop_param)
        
        if rangematch:
            pop_param = [int(rangematch.captures(1)[0]), int(rangematch.captures(2)[0])+1]
            for p in range(*pop_param):
                iterate_model(
                    file, module, parameterization[1:], params + [str(p)])
        elif listmatch:
            l = listmatch.captures(2) + listmatch.captures(3)

            for p in l:
                iterate_model(
                    file, module, parameterization[1:], params + [str(p)])
            


for f in sys.argv[1:]:
    fo = open(f, "rb")
    l = [regex.match(RE, l.decode("utf-8")) for l in fo.readlines()]
    modules += [(f,
                 m.captures(1)[0],
                 m.captures(2) ) for m in l if m != None]
    fo.close()


def text_catcher(queue):
    while True:
        g = queue.get()

        if g == None:
            return

        sys.stdout.write("Pool: " + g)

if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    pool = mp.Pool(mp.cpu_count())
    m = mp.Manager()

    q = m.Queue()

    print(modules)
    monitor = Thread(target=text_catcher,args=(q,))
    monitor.daemon = True
    monitor.start()

    for m in modules:

        iterate_model(*m, params=[])

    while len(waitlist) != 0:
        waitlist[0].wait()
        waitlist.pop(0)

    pool.close()

    q.put(None)
    while not q.empty():
        pass

