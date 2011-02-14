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
>>> pyjack.connect(open, spyfn=fakeopen)
<..._PyjackFuncBuiltin object at 0x...>
>>> 
>>> for line in open('/some/path', 'r'):
...     print line
... 
Here is the org open fn: <built-in function open>
Someone trying to open a file with args:('/some/path', 'r') kwargs{}

Filtering args
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
>>> def absmin(orgmin, seq):
...     return orgmin([abs(x) for x in seq])
... 
>>> pyjack.connect(min, spyfn=absmin)
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

Works on objects (but not slot wrappers)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 
>>> class Foobar(object):
...     
...     def say_hi(self):
...         return 'hi'
>>> 
>>> foobar = Foobar()
>>> 
>>> foobar.say_hi()
'hi'
>>> 
>>> pyjack.connect(Foobar.say_hi, lambda orgfn, self: 'HI')
<...function say_hi at 0x...>
>>> 
>>> foobar.say_hi()
'HI'
>>> 
>>> Foobar.say_hi.restore()
>>> 
>>> foobar.say_hi()
'hi'

Does not work on slot wrappers (like builtin :func:`__init__`, etc.) 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 
>>> def in_init(orgfn, self):
...     print 'in __init__'
... 
>>> try:
...     pyjack.connect(Foobar.__init__, spyfn=in_init)
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
>>> pyjack.connect(Foobar.__init__, spyfn=in_init)
<...function my_init at 0x...>
>>> 
>>> Foobar()
in __init__
<...Foobar object at 0x...>

But by this point, you really don't need pyjack anymore anyway, but just 
showing for completeness. 

 

Using :func:`replace_all_refs`
------------------------------------------------------------------------------

This is just to show how :func:`replace_all_refs` works across a large, 
nested memory space. 

.. note::
 
  Currently, pyjack does not work within function closures that use the
  :class:`cell` readonly data structure. At this time, this is the only 
  known exception. 

Let's take a simple iterable

 
>>> iterable = [1, 2, 3, 4]

And to really make it weird, make it circular: 

 
>>> iterable.append({'theiterable': iterable})

Now create a closure (pyjack can't work on closures, and we'll show that): 

 
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
...     anotheriterable = (iterable, 'x', 'y', 'z',)

Now let's gander at some results: 
 
>>> innerfun = myfun(iterable)

So look at the org results
 
>>> print "iterable:", iterable
iterable: [1, 2, 3, 4, {'theiterable': [...]}]
>>> print "SomeCls.someiterable:", SomeCls.someiterable
SomeCls.someiterable: [1, 2, 3, 4, {'theiterable': [...]}]
>>> print "SomeCls.anotheriterable:", SomeCls.anotheriterable
SomeCls.anotheriterable: ([1, 2, 3, 4, {'theiterable': [...]}], 'x', 'y', 'z')
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
SomeCls.anotheriterable: (('new', 'data', 'set'), 'x', 'y', 'z')

And inner fun, notice pyjack here does not work: 
 
>>> innerfun_gen = innerfun()
>>> print "First yield:", innerfun_gen.next()
First yield: [1, 2, 3, 4, {'theiterable': ('new', 'data', 'set')}]
>>> print "Second yield:", innerfun_gen.next()
Second yield: ([1, 2, 3, 4, {'theiterable': ('new', 'data', 'set')}], 'x', 'y', 'z')

Some bigger examples to make sure :mod:`gc` does not implode
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
>>> import random
Traceback (most recent call last):
    ...
NameError: name 'OverflowWarning' is not defined
>>> 
>>> random = random.Random(0)
Traceback (most recent call last):
    ...
NameError: name 'random' is not defined
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
... 
Traceback (most recent call last):
    ...
NameError: name 'random' is not defined

Org list:
 
>>> print mylist[10000]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[10001]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[10002]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[50000]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[50001]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[50002]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> 
>>> obj = pyjack.replace_all_refs(obj, [])

New list:
 
>>> print mylist[10000]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[10001]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[10002]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[50000]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[50001]
Traceback (most recent call last):
    ...
IndexError: list index out of range
>>> print mylist[50002]
Traceback (most recent call last):
    ...
IndexError: list index out of range

And final check:
 
>>> print obj
{'y': [10, 20, 30], 'x': 10}

'''

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=268)

