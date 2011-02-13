
import pyjack

def hi(x, y):
    return x + y

print hi(1, 2)


def spy(x, y):
    print 'filter', x, y
    return (x, y,), {}

pyjack.connect(hi, filter=spy)
    
print hi(1, 2)
print hi(1, 2)

pyjack.restore(hi)

print hi(1, 2)

def foo(fn, *args, **kwargs):
    print 'First, I stop you'

def bar(fn, *args, **kwargs):
    print 'Then, I return "baz"'
    return "baz"

pyjack.connect(__import__, filter=foo, callback=bar, block=True, passfn=True)

import time
print time
import os
print os

__import__.restore()

import time
print time

    
    