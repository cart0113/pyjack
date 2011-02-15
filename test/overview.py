if __name__ == '__main__':
    import mod2doctest
    mod2doctest.convert(r'C:\Python24\python.exe', src=True,
                        add_autogen=False, target='_doctest',
                        run_doctest=False,)
    
    
#>Some examples of connecting to functions
#>------------------------------------------------------------------------------

#>Prevent function from firing
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#>Let's say you want to 1. monitor and 2. prevent every time something is 
#>opening a file:
import pyjack

def fakeopen(orgopen, *args, **kwargs):
    print 'Here is the org open fn: %r' % orgopen
    print 'Someone trying to open a file with args:%r kwargs%r' %(args, kwargs,)
    return ()

pyjack.connect(open, proxyfn=fakeopen)

for line in open('/some/path', 'r'):
    print line

#>Filtering args
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def absmin(orgmin, seq):
    return orgmin([abs(x) for x in seq])
    
pyjack.connect(min, proxyfn=absmin)

print min([-100, 20, -200, 150])

#>Works across memory space
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#>A major point of pyjack is that all references to the object are updated / 
#>pyjacked.  So notice below how :func:`time.time` is updated as well as the 
#>local reference :attr:`timefn`.

import time
from time import time as timefn

class MockTime(object):
    
    time = -1
    
    def __call__(self, orgtime):
        self.time += 1
        return self.time
    
pyjack.connect(time.time, MockTime())

# So the org function is replaced:
print time.time()
print time.time()
print time.time()
print time.time()


# But so is the copy:
print timefn()
print timefn()
print timefn()
print timefn()


#>Works on object methods (but not slot wrappers)
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Foobar(object):
    
    def say_hi(self):
        return 'hi'
    

foobar = Foobar()

print foobar.say_hi()

pyjack.connect(Foobar.say_hi, lambda orgfn, self: 'HI')

print foobar.say_hi()

#>And restore: 
Foobar.say_hi.restore()

print foobar.say_hi()

#>Test that you can't remove restore again: 
try:
    foobar.say_hi.restore()
except AttributeError: 
    print "'say_hi' has already been restored, so there's no more restore fn"

#>Cycle connect/restore to make sure everything is working
pyjack.connect(Foobar.say_hi, lambda orgfn, self: 'HI')
print foobar.say_hi()
Foobar.say_hi.restore()
print foobar.say_hi()
pyjack.connect(Foobar.say_hi, lambda orgfn, self: 'HI')
print foobar.say_hi()
Foobar.say_hi.restore()
print foobar.say_hi()

#>Does not work on slot wrappers (like builtin :func:`__init__`, etc.) 
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def in_init(orgfn, self):
    print 'in __init__'

try: 
    pyjack.connect(Foobar.__init__, proxyfn=in_init)
except pyjack.PyjackException, err:
    print err

#>Do get around this you would need to do:

def my_init(self):
    pass

Foobar.__init__ = my_init

pyjack.connect(Foobar.__init__, proxyfn=in_init)

Foobar()

#>But by this point, you really don't need pyjack anymore anyway, but just 
#>showing for completeness. 


#>Works on callables that define :func:`__call__`
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Adder(object):
    
    def __call__(self, x, y):
        return x + y

adder = Adder()

print adder(-4, 3)

#>Now connect lambda fn which takes abs of all args
pyjack.connect(fn=adder, proxyfn=lambda self, fn, x, y: fn(abs(x), abs(y)))

print adder(-4, 3)

#>Now restore: 
adder.restore()

print adder(-4, 3)

#>Remember, restore removes the :func:`restore`
try:
    adder.restore()
except AttributeError: 
    print "'adder' has already been restored, so there's no more restore fn"

#>Now, as part of unit test, just make sure you can connect / restore / connect
pyjack.connect(fn=adder, proxyfn=lambda self, fn, x, y: fn(abs(x), abs(y)))

print adder(-4, 3)

adder.restore()

print adder(-4, 3)

pyjack.connect(fn=adder, proxyfn=lambda self, fn, x, y: fn(abs(x), abs(y)))

print adder(-4, 3)

adder.restore()

print adder(-4, 3)


#>Using :func:`replace_all_refs`
#>------------------------------------------------------------------------------

#>This is just to show how :func:`replace_all_refs` works across a large, 
#>nested memory space. 

#>Let's take a simple iterable
iterable = [1, 2, 3, 4]

#>And to make it weird, make it circular: 

iterable.append({'theiterable': iterable})

#>Now create a closure: 

def myfun(iterable):
    
    myiterable = iterable
    
    anotheriterable = (iterable, 'x', 'y', 'z')
    
    def innerfun():
        yield myiterable
        yield anotheriterable
            
    return innerfun

#>And stick it in a class, too: 

class SomeCls(object):
    
    iscls = True
    
    someiterable = iterable
    anotheriterable = (iterable, 'x', 'y', 'z', {'innerref': someiterable})


#>Now let's gander at some results: 
innerfun = myfun(iterable)

#>So look at the org results
print "iterable:", iterable
print "SomeCls.someiterable:", SomeCls.someiterable
print "SomeCls.anotheriterable:", SomeCls.anotheriterable
print "Contents of innerfun:"

#>And inner fun: 
innerfun_gen = innerfun()
print "First yield:", innerfun_gen.next()
print "Second yield:", innerfun_gen.next()

#>Now, let's replace iterable with some new data
new_iterable = ('new', 'data', 'set',)
org_iterable = pyjack.replace_all_refs(iterable, new_iterable)

#>Then look at the new results
print "iterable:", iterable
print "SomeCls.someiterable:", SomeCls.someiterable
print "SomeCls.anotheriterable:", SomeCls.anotheriterable

#>And inner fun, notice the function closure was updated:
innerfun_gen = innerfun()
print "First yield:", innerfun_gen.next()
print "Second yield:", innerfun_gen.next()

#>Then, reverse:
new_iterable = pyjack.replace_all_refs(new_iterable, org_iterable)

#>Then look at the new results
print "iterable:", iterable
print "SomeCls.someiterable:", SomeCls.someiterable
print "SomeCls.anotheriterable:", SomeCls.anotheriterable

#>And inner fun, notice the function closure was updated:
innerfun_gen = innerfun()
print "First yield:", innerfun_gen.next()
print "Second yield:", innerfun_gen.next()



#>Test sets / frozen sets
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#>sets
x = (10, 20, 30,)

y = set([x, -1, -2])

org_x = pyjack.replace_all_refs(x, ('proxy', 'data',))

print x
print y

#>Frozen sets
x = (10, 20, 30,)

y = frozenset([x, -1, -2])

org_x = pyjack.replace_all_refs(x, ('proxy', 'data',))

print x
print y

#>Test dictionary
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

x = (10, 20, 30,)

y = {x: [1, 2, 3, {x: [1, x]}]}

org_x = pyjack.replace_all_refs(x, ('proxy', 'data',))

print x
print y

#>Some bigger examples to make sure :mod:`gc` does not implode
#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import random

random = random.Random(0)

obj = {'x': 10, 'y': [10, 20, 30,]}
       
mylist = []

for i in xrange(100000):

    if i % 10000 == 0:
        mylist.append(obj)
    elif i % 10000 == 1:
        mylist.append((obj, obj,))
    else:
        mylist.append(random.randint(0, 1e6))
        
#>Org list:
print mylist[10000]
print mylist[10001]
print mylist[10002]
print mylist[50000]
print mylist[50001]
print mylist[50002]

obj = pyjack.replace_all_refs(obj, [])

#>New list:
print mylist[10000]
print mylist[10001]
print mylist[10002]
print mylist[50000]
print mylist[50001]
print mylist[50002]

#>And final check:
print obj


