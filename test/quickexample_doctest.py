r'''
The import:
 
>>> import pyjack

Show the "connect" function:
 
>>> def fakeimport(orgopen, *args, **kwargs):
...     print 'Trying to import %s' % args[0]
...     return 'MODULE_%s' % args[0]
... 
>>> pyjack.connect(__import__, proxyfn=fakeimport)
<..._PyjackFuncBuiltin object at 0x...>
>>> 
>>> import time
Trying to import time
>>> print time
MODULE_time
>>> 
>>> __import__.restore()
>>> 
>>> import time
>>> print time
<module 'time' (built-in)>

Show the "replace all refs" function:
 
>>> item = (100, 'one hundred')
>>> data = {item: True, 'itemdata': item}
>>> 
>>> class Foobar(object):
...     the_item = item
... 
>>> def outer(datum):
...     def inner():
...         return ("Here is the datum:", datum,)
...     
...     return inner
... 
>>> inner = outer(item)
>>> 
>>> print item
(100, 'one hundred')
>>> print data
{'itemdata': (100, 'one hundred'), (100, 'one hundred'): True}
>>> print Foobar.the_item
(100, 'one hundred')
>>> print inner()
('Here is the datum:', (100, 'one hundred'))

Then replace them:
 
>>> new = (101, 'one hundred and one')
>>> org_item = pyjack.replace_all_refs(item, new)
>>> 
>>> print item
(101, 'one hundred and one')
>>> print data
{'itemdata': (101, 'one hundred and one'), (101, 'one hundred and one'): True}
>>> print Foobar.the_item
(101, 'one hundred and one')
>>> print inner()
('Here is the datum:', (101, 'one hundred and one'))

But you still have the org data:
 
>>> print org_item
(100, 'one hundred')

So the process is reversible: 
 
>>> new = pyjack.replace_all_refs(new, org_item)
>>> 
>>> print item
(100, 'one hundred')
>>> print data
{'itemdata': (100, 'one hundred'), (100, 'one hundred'): True}
>>> print Foobar.the_item
(100, 'one hundred')
>>> print inner()
('Here is the datum:', (100, 'one hundred'))

'''

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=268)

