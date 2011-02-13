basicexample.py: A quick example. 
*********************************

Input Module
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		
This is the input module::
		
	if __name__ == '__main__':
	
	    # Anything inside a __name__ == '__main__' block is removed
	    
	    import mod2doctest
	    mod2doctest.convert('python', src=True, target=True, run_doctest=False)    
	
	#>Notes on documentation ..
	#>==============================================================================
	#|
	#|mod2doctest allows you to create comments that show up in the docstr 
	#|so you can easily add sphinx rest comments like this:
	#| 
	#|.. note::  
	#|
	#|   *  ``#|`` prints only to docstr
	#|   *  ``#>`` prints to docstr and stdout
	#|
	#|For example: 
	#|
	#|This is just in the docs
	#|
	#>This prints to the docs and stdout. 
	#|
	
	#>Test Setup
	#>==============================================================================
	import pickle
	import os
	
	#|Btw, you can use 'if __name__' blocks anywhere you want, it will not show
	#|up in the final docstring.  They are the mod2doctest 'comments', so to speak.
	if __name__ == '__main__':
	    import log
	
	#>Make A List
	#>==============================================================================
	alist = [1, -4, 50] + list(set([10, 10, 10]))
	alist.sort()
	print alist
	
	#>Pickle The List
	#>==============================================================================
	#|This will print the repr of the pickle string.  If this algorithm every
	#|changes -- even if one character is different -- this test will 'break'. 
	print repr(pickle.dumps(alist))
	
	#>Ellipses #1: mod2doctest can (if you want) add ellipses to memory IDs
	#>==============================================================================
	class Foo(object):
	    pass
	
	print Foo
	print Foo()
	
	#>Ellipses #2: Also, you can add ellipses to file paths
	#>==============================================================================
	#|This will ellipse the module name
	print pickle
	#|This will ellipse the current path (only the final rel path will be there). 
	os.getcwd()
	
	#>Ellipses #3: mod2doctest can (if you want) add ellipses to tracebacks
	#>==============================================================================
	print pickle.dumps(os)
	
	#>But, here's another way to exercise exceptions (that's a little cleaner IMHO).
	#>==============================================================================
	try:
	    print pickle.dumps(os)
	    print 'This is okay!'
	except TypeError, e:    
	    print 'Oh no it is not: %s' % e
	
	#> EOF
	#>==============================================================================
	print "That's all folks."
	raise SystemExit # could also do exit() on Python 2.5 or higher
	
	#> Even thought there is more ... the exit prevented this from being called.
	#>==============================================================================
	print "Hello World?  Anybody there??"


printout to stdout/stderr
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

It prints to stdout/stderr like this::

	Python 2.6.2 (r262:71605, Apr 14 2009, 22:40:02) [MSC v.1500 32 bit (Intel)] on win32
	Type "help", "copyright", "credits" or "license" for more information.
	
	
	Notes on documentation ..
	==============================================================================
	
	
	This prints to the docs and stdout. 
	
	
	Test Setup
	==============================================================================
	
	
	Make A List
	==============================================================================
	[-4, 1, 10, 50]
	
	
	Pickle The List
	==============================================================================
	'(lp0\nI-4\naI1\naI10\naI50\na.'
	
	
	Ellipses #1: mod2doctest can (if you want) add ellipses to memory IDs
	==============================================================================
	<class '__main__.Foo'>
	<__main__.Foo object at 0x02261AF0>
	
	
	Ellipses #2: Also, you can add ellipses to file paths
	==============================================================================
	<module 'pickle' from 'C:\Python26\lib\pickle.pyc'>
	'C:\\eclipse\\workspace\\GIT_MOD2DOCTEST\\tests'
	
	
	Ellipses #3: mod2doctest can (if you want) add ellipses to tracebacks
	==============================================================================
	Traceback (most recent call last):
	  File "<stdin>", line 3, in <module>
	  File "C:\Python26\lib\pickle.py", line 1366, in dumps
	    Pickler(file, protocol).dump(obj)
	  File "C:\Python26\lib\pickle.py", line 224, in dump
	    self.save(obj)
	  File "C:\Python26\lib\pickle.py", line 306, in save
	    rv = reduce(self.proto)
	  File "C:\Python26\lib\copy_reg.py", line 70, in _reduce_ex
	    raise TypeError, "can't pickle %s objects" % base.__name__
	TypeError: can't pickle module objects
	
	
	But, here's another way to exercise exceptions (that's a little cleaner IMHO).
	==============================================================================
	Oh no it is not: can't pickle module objects
	
	
	 EOF
	==============================================================================
	That's all folks.


output docstring
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The docstring -- which is put in a seperate ``_doctest.py`` file because
``target`` was set to ``'_doctest`` in the convert call -- looks like this::

	r"""
	================================================================================
	Auto generated by mod2doctest on Fri Sep 24 14:44:04 2010
	================================================================================
	Python 2.6.2 (r262:71605, Apr 14 2009, 22:40:02) [MSC v.1500 32 bit (Intel)] on win32
	Type "help", "copyright", "credits" or "license" for more information.
	
	Notes on documentation ..
	==============================================================================
	
	mod2doctest allows you to create comments that show up in the docstr 
	so you can easily add sphinx rest comments like this:
	 
	.. note::  
	
	  *  ``#|`` prints only to docstr
	  *  ``#>`` prints to docstr and stdout
	
	For example: 
	
	This is just in the docs
	
	This prints to the docs and stdout. 
	
	
	Test Setup
	==============================================================================
	 
	>>> import pickle
	>>> import os
	
	Btw, you can use 'if __name__' blocks anywhere you want, it will not show
	up in the final docstring.  They are the mod2doctest 'comments', so to speak.
	
	Make A List
	==============================================================================
	 
	>>> alist = [1, -4, 50] + list(set([10, 10, 10]))
	>>> alist.sort()
	>>> print alist
	[-4, 1, 10, 50]
	
	Pickle The List
	==============================================================================
	This will print the repr of the pickle string.  If this algorithm every
	changes -- even if one character is different -- this test will 'break'. 
	 
	>>> print repr(pickle.dumps(alist))
	'(lp0\nI-4\naI1\naI10\naI50\na.'
	
	Ellipses #1: mod2doctest can (if you want) add ellipses to memory IDs
	==============================================================================
	 
	>>> class Foo(object):
	...     pass
	... 
	>>> print Foo
	<class '__main__.Foo'>
	>>> print Foo()
	<...Foo object at 0x...>
	
	Ellipses #2: Also, you can add ellipses to file paths
	==============================================================================
	This will ellipse the module name
	 
	>>> print pickle
	<module 'pickle' from '...pickle.pyc'>
	
	This will ellipse the current path (only the final rel path will be there). 
	 
	>>> os.getcwd()
	'...tests'
	
	Ellipses #3: mod2doctest can (if you want) add ellipses to tracebacks
	==============================================================================
	 
	>>> print pickle.dumps(os)
	Traceback (most recent call last):
	    ...
	TypeError: can't pickle module objects
	
	But, here's another way to exercise exceptions (that's a little cleaner IMHO).
	==============================================================================
	 
	>>> try:
	...     print pickle.dumps(os)
	...     print 'This is okay!'
	... except TypeError, e:
	...     print 'Oh no it is not: %s' % e
	... 
	Oh no it is not: can't pickle module objects
	
	EOF
	==============================================================================
	 
	>>> print "That's all folks."
	That's all folks.
	
	"""


Using the 'automodule' directive in Sphinx to autocreate documentation
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

which looks like this when you use an ``automodule`` sphinx directive: 

.. automodule:: tests.basicexample_doctest




