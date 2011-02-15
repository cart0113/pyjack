r'''
Some examples of connecting to functions
------------------------------------------------------------------------------

Prevent function from firing
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Let's say you want to 1. monitor and 2. prevent every time something is 
opening a file:
 
>>> import pyjack
>>> 
>>> def fakeopen(orgopen, *args, **kwargs):
...     print 'Here is the org open fn: %r' % orgopen
...     print 'Someone trying to open a file with args:%r kwargs%r' %(args, kwargs,)
...     return ()
... 
>>> pyjack.connect(open, proxyfn=fakeopen)
<..._PyjackFuncBuiltin object at 0x...>
>>> 
>>> for line in open('/some/path', 'r'):
...     print line
... 
Here is the org open fn: <type 'file'>
Someone trying to open a file with args:('/some/path', 'r') kwargs{}

Filtering args
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
>>> def absmin(orgmin, seq):
...     return orgmin([abs(x) for x in seq])
... 
>>> pyjack.connect(min, proxyfn=absmin)
<..._PyjackFuncBuiltin object at 0x...>
>>> 
>>> print min([-100, 20, -200, 150])
20

Works across memory space
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A major point of pyjack is that all references to the object are updated / 
pyjacked.  So notice below how :func:`time.time` is updated as well as the 
local reference :attr:`timefn`.

 
>>> import time
>>> from time import time as timefn
>>> 
>>> class MockTime(object):
...     
...     time = -1
...     
...     def __call__(self, orgtime):
...         self.time += 1
...         return self.time
... 
>>> pyjack.connect(time.time, MockTime())
<..._PyjackFuncBuiltin object at 0x...>
>>> 
>>> # So the org function is replaced:
... print time.time()
0
>>> print time.time()
1
>>> print time.time()
2
>>> print time.time()
3
>>> 
>>> # But so is the copy:
... print timefn()
4
>>> print timefn()
5
>>> print timefn()
6
>>> print timefn()
7

Works on object methods (but not slot wrappers)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 
>>> class Foobar(object):
...     
...     def say_hi(self):
...         return 'hi'
>>> 
>>> foobar = Foobar()
>>> 
>>> print foobar.say_hi()
hi
>>> 
>>> pyjack.connect(Foobar.say_hi, lambda orgfn, self: 'HI')
<...function say_hi at 0x...>
>>> 
>>> print foobar.say_hi()
HI

And restore: 
 
>>> Foobar.say_hi.restore()
>>> 
>>> print foobar.say_hi()
hi

Test that you can't remove restore again: 
 
>>> try:
...     foobar.say_hi.restore()
... except AttributeError:
...     print "'say_hi' has already been restored, so there's no more restore fn"

Cycle connect/restore to make sure everything is working
 
>>> pyjack.connect(Foobar.say_hi, lambda orgfn, self: 'HI')
<...function say_hi at 0x...>
>>> print foobar.say_hi()
HI
>>> Foobar.say_hi.restore()
>>> print foobar.say_hi()
hi
>>> pyjack.connect(Foobar.say_hi, lambda orgfn, self: 'HI')
<...function say_hi at 0x...>
>>> print foobar.say_hi()
HI
>>> Foobar.say_hi.restore()
>>> print foobar.say_hi()
hi

Does not work on slot wrappers (like builtin :func:`__init__`, etc.) 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 
>>> def in_init(orgfn, self):
...     print 'in __init__'
... 
>>> try:
...     pyjack.connect(Foobar.__init__, proxyfn=in_init)
... except pyjack.PyjackException, err:
...     print err
... 
Wrappers not supported. Make a concrete fn.

Do get around this you would need to do:

 
>>> def my_init(self):
...     pass
... 
>>> Foobar.__init__ = my_init
>>> 
>>> pyjack.connect(Foobar.__init__, proxyfn=in_init)
<...function my_init at 0x...>
>>> 
>>> Foobar()
in __init__
<...Foobar object at 0x...>

But by this point, you really don't need pyjack anymore anyway, but just 
showing for completeness. 

 

Works on callables that define :func:`__call__`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 
>>> class Adder(object):
...     
...     def __call__(self, x, y):
...         return x + y
... 
>>> adder = Adder()
>>> 
>>> print adder(-4, 3)
-1

Now connect lambda fn which takes abs of all args
 
>>> pyjack.connect(fn=adder, proxyfn=lambda self, fn, x, y: fn(abs(x), abs(y)))
<...Adder object at 0x...>
>>> 
>>> print adder(-4, 3)
7

Now restore: 
 
>>> adder.restore()
>>> 
>>> print adder(-4, 3)
-1

Remember, restore removes the :func:`restore`
 
>>> try:
...     adder.restore()
... except AttributeError:
...     print "'adder' has already been restored, so there's no more restore fn"
... 
'adder' has already been restored, so there's no more restore fn

Now, as part of unit test, just make sure you can connect / restore / connect
 
>>> pyjack.connect(fn=adder, proxyfn=lambda self, fn, x, y: fn(abs(x), abs(y)))
<...Adder object at 0x...>
>>> 
>>> print adder(-4, 3)
7
>>> 
>>> adder.restore()
>>> 
>>> print adder(-4, 3)
-1
>>> 
>>> pyjack.connect(fn=adder, proxyfn=lambda self, fn, x, y: fn(abs(x), abs(y)))
<...Adder object at 0x...>
>>> 
>>> print adder(-4, 3)
7
>>> 
>>> adder.restore()
>>> 
>>> print adder(-4, 3)
-1

Using :func:`replace_all_refs`
------------------------------------------------------------------------------

This is just to show how :func:`replace_all_refs` works across a large, 
nested memory space. 

Let's take a simple iterable
 
>>> iterable = [1, 2, 3, 4]

And to make it weird, make it circular: 

 
>>> iterable.append({'theiterable': iterable})

Now create a closure: 

 
>>> def myfun(iterable):
...     
...     myiterable = iterable
...     
...     anotheriterable = (iterable, 'x', 'y', 'z')
...     
...     def innerfun():
...         yield myiterable
...         yield anotheriterable
...     
...     return innerfun

And stick it in a class, too: 

 
>>> class SomeCls(object):
...     
...     iscls = True
...     
...     someiterable = iterable
...     anotheriterable = (iterable, 'x', 'y', 'z', {'innerref': someiterable})

Now let's gander at some results: 
 
>>> innerfun = myfun(iterable)

So look at the org results
 
>>> print "iterable:", iterable
iterable: [1, 2, 3, 4, {'theiterable': [...]}]
>>> print "SomeCls.someiterable:", SomeCls.someiterable
SomeCls.someiterable: [1, 2, 3, 4, {'theiterable': [...]}]
>>> print "SomeCls.anotheriterable:", SomeCls.anotheriterable
SomeCls.anotheriterable: ([1, 2, 3, 4, {'theiterable': [...]}], 'x', 'y', 'z', {'innerref': [1, 2, 3, 4, {'theiterable': [...]}]})
>>> print "Contents of innerfun:"
Contents of innerfun:

And inner fun: 
 
>>> innerfun_gen = innerfun()
>>> print "First yield:", innerfun_gen.next()
First yield: [1, 2, 3, 4, {'theiterable': [...]}]
>>> print "Second yield:", innerfun_gen.next()
Second yield: ([1, 2, 3, 4, {'theiterable': [...]}], 'x', 'y', 'z')

Now, let's replace iterable with some new data
 
>>> new_iterable = ('new', 'data', 'set',)
>>> org_iterable = pyjack.replace_all_refs(iterable, new_iterable)

Then look at the new results
 
>>> print "iterable:", iterable
iterable: ('new', 'data', 'set')
>>> print "SomeCls.someiterable:", SomeCls.someiterable
SomeCls.someiterable: ('new', 'data', 'set')
>>> print "SomeCls.anotheriterable:", SomeCls.anotheriterable
SomeCls.anotheriterable: (('new', 'data', 'set'), 'x', 'y', 'z', {'innerref': ('new', 'data', 'set')})

And inner fun, notice the function closure was updated:
 
>>> innerfun_gen = innerfun()
>>> print "First yield:", innerfun_gen.next()
First yield: ('new', 'data', 'set')
>>> print "Second yield:", innerfun_gen.next()
Second yield: (('new', 'data', 'set'), 'x', 'y', 'z')

Then, reverse:
 
>>> new_iterable = pyjack.replace_all_refs(new_iterable, org_iterable)

Then look at the new results
 
>>> print "iterable:", iterable
iterable: [1, 2, 3, 4, {'theiterable': [...]}]
>>> print "SomeCls.someiterable:", SomeCls.someiterable
SomeCls.someiterable: [1, 2, 3, 4, {'theiterable': [...]}]
>>> print "SomeCls.anotheriterable:", SomeCls.anotheriterable
SomeCls.anotheriterable: ([1, 2, 3, 4, {'theiterable': [...]}], 'x', 'y', 'z', {'innerref': [1, 2, 3, 4, {'theiterable': [...]}]})

And inner fun, notice the function closure was updated:
 
>>> innerfun_gen = innerfun()
>>> print "First yield:", innerfun_gen.next()
First yield: [1, 2, 3, 4, {'theiterable': [...]}]
>>> print "Second yield:", innerfun_gen.next()
Second yield: ([1, 2, 3, 4, {'theiterable': [...]}], 'x', 'y', 'z')

Test sets / frozen sets
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

sets
 
>>> x = (10, 20, 30,)
>>> 
>>> y = set([x, -1, -2])
>>> 
>>> org_x = pyjack.replace_all_refs(x, ('proxy', 'data',))
>>> 
>>> print x
('proxy', 'data')
>>> print y
set([('proxy', 'data'), -2, -1])

Frozen sets
 
>>> x = (10, 20, 30,)
>>> 
>>> y = frozenset([x, -1, -2])
>>> 
>>> org_x = pyjack.replace_all_refs(x, ('proxy', 'data',))
>>> 
>>> print x
('proxy', 'data')
>>> print y
frozenset([('proxy', 'data'), -2, -1])

Test dictionary
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 
>>> x = (10, 20, 30,)
>>> 
>>> y = {x: [1, 2, 3, {x: [1, x]}]}
>>> 
>>> org_x = pyjack.replace_all_refs(x, ('proxy', 'data',))
>>> 
>>> print x
('proxy', 'data')
>>> print y
{('proxy', 'data'): [1, 2, 3, {('proxy', 'data'): [1, ('proxy', 'data')]}]}

Some bigger examples to make sure :mod:`gc` does not implode
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
>>> import random
>>> 
>>> random = random.Random(0)
>>> 
>>> obj = {'x': 10, 'y': [10, 20, 30,]}
>>> 
>>> mylist = []
>>> 
>>> for i in xrange(100000):
...     
...     if i % 10000 == 0:
...         mylist.append(obj)
...     elif i % 10000 == 1:
...         mylist.append((obj, obj,))
...     else:
...         mylist.append(random.randint(0, 1e6))

Org list:
 
>>> print mylist[10000]
{'y': [10, 20, 30], 'x': 10}
>>> print mylist[10001]
({'y': [10, 20, 30], 'x': 10}, {'y': [10, 20, 30], 'x': 10})
>>> print mylist[10002]
618969
>>> print mylist[50000]
{'y': [10, 20, 30], 'x': 10}
>>> print mylist[50001]
({'y': [10, 20, 30], 'x': 10}, {'y': [10, 20, 30], 'x': 10})
>>> print mylist[50002]
357697
>>> 
>>> obj = pyjack.replace_all_refs(obj, [])

New list:
 
>>> print mylist[10000]
[]
>>> print mylist[10001]
([], [])
>>> print mylist[10002]
618969
>>> print mylist[50000]
[]
>>> print mylist[50001]
([], [])
>>> print mylist[50002]
357697

And final check:
 
>>> print obj
{'y': [10, 20, 30], 'x': 10}

'''

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=268)

