r'''
>>> 
>>> import pyjack
>>> 
>>> def fakeimport(orgopen, *args, **kwargs):
...     
...     print 'Trying to import %s' % args[0]
...     
...     return 'MODULE_%s' % args[0]
... 
>>> pyjack.connect(__import__, spyfn=fakeimport)
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

'''

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=524)

