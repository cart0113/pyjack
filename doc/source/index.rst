.. role:: raw-html(raw)
   :format: html

.. |pyjack|    replace:: :mod:`mod2doctest`

pyjack
******

What's New
==========

*  2/12/2011 -- Version 0.3.0 out.  Pretty big rewrite.  In general, much
   cleaner and simpler.  Also, dropped support for wrapper functions. 

What is mod2doctest?
====================

|mod2doctest| takes a runnable python script as input and creates a nicely 
formatted triple quoted docstring.  This docstring can then be used as: 

*  A test fixture since it's runnable within doctest
    
*  Source code documentation as it can be handed to sphinx with a 
   ``.. automodule`` command (see examples below).

It's similiar in concept to copying and pasting the script/module contents
into the interactive interpreter.  However, among other features, |mod2doctest|:

*  Provides several formatting tools.  In particular, ``#>`` and ``#|`` 
   are special |mod2doctest| comments that allow you to control the output
   format of the docstr (and what gets printed to stdout).  In general, 
   the output docstring from |mod2doctest| is much more nicely formatted
   than if you copy/paste directly. 
   
*  Fixes problems with whitespace that don't allow you to directly copy
   a module source into the interpreter (modules can have blanklines 
   within a suite; the interpreter does not allow this).    
   
It's also similar to writing docstrings directly.  However, among other things, 
by using |mod2doctest| you: 

*  Take advantage of writing python code in your normal IDE / editor (as 
   opposed to writing within the triple quoted string) so things like
   code completion, etc will still work. 
   
*  Don't need to worry about creating program output -- |mod2doctest|
   adds this for you. 

The goal of |doctest| itself is to greatly reduce the burden of writing test 
fixtures and documentation.  |mod2doctest| attempts to build on these goals. 
By following a few conventions, you can create permanent test fixtures and 
nicely formatted documentation in as much time as you'd spend creating those 
quick throw away test scripts you need to develop your code against. 

Quick Example
================================================================================

A module that looks like this::

	if __name__ == '__main__':
	
	    # All __name__ == '__main__' blocks are removed, serving as mod2doctest 
	    # comments
	    
	    import mod2doctest
	    mod2doctest.convert('python', src=True, target='_doctest', run_doctest=False, 
	                        add_testmod=False, add_autogen=False)    
	
	#>Welcome to mod2doctest
	#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	#|
	#|Just enter in some python
	#| 
	#|.. warning::  
	#|   make sure to examine your resulting docstr to make sure output is as 
	#|   expected!
	
	#|The basics: 
	print 'Hello World!'
	
	#>Extended Example
	#>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	#|A little more:
	somelist = [100, 2, -20, 340, 0, 0, 10, 10, 88, -3, 100, 2, -99, -1]
	sorted(set(somelist))

Will print to stdout (when run) like this::
	
	Python 2.6.2 (r262:71605, Apr 14 2009, 22:40:02) [MSC v.1500 32 bit (Intel)] on win32
	Type "help", "copyright", "credits" or "license" for more information.
	
	
	Welcome to mod2doctest
	++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	Hello World!
	
	
	Extended Example
	++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	[-99, -20, -3, -1, 0, 2, 10, 88, 100, 340]

Also, a docstring like this is created::

	r"""
	Welcome to mod2doctest
	++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	Just enter in some python
	 
	.. warning::  
	  make sure to examine your resulting docstr to make sure output is as 
	  expected!
	
	The basics: 
	 
	>>> print 'Hello World!'
	Hello World!
	
	Extended Example
	++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	A little more:
	 
	>>> somelist = [100, 2, -20, 340, 0, 0, 10, 10, 88, -3, 100, 2, -99, -1]
	>>> sorted(set(somelist))
	[-99, -20, -3, -1, 0, 2, 10, 88, 100, 340]
	
	"""


Which, when included in sphinx documentation looks like this:

.. automodule:: tests.intro_doctest


Installation for Python 2.x
===========================

Try::

	easy_install mod2doctest
	
	or 
	
	pip mod2doctest

If that does not work go to http://pypi.python.org/pypi/mod2doctest/.

There you can grab the windows installer, egg, or source directly. 

Also, go to http://github.com/cart0113/mod2doctest to grab the latest repo.

API
===

.. automodule:: mod2doctest
.. autofunction:: mod2doctest.convert


Examples
========

One great thing about |doctest| is that your tests can easily be converted
to webpages using :mod:`sphinx`.  Even for large test programs the linear 
webpage output is a great tool to understand the test setup and overall
test structure. 

By using the special ``#>`` and ``#|`` special |mod2doctest| comments, it 
is easy to create documentation at the same time as you are constructing your 
test.  

The following tests below were generated using these techniques. 

.. note::

   In this case, to best understand what's going on, look in mod2doctest.tests 
   package.  And, if you want, go to http://github.com/cart0113/mod2doctest, 
   clone the repo, and check out how those modules are used in the Sphinx 
   documentation. 

.. toctree::
   :maxdepth: 1
	
   basicexample
   extendedexample

How Does |mod2doctest| Work?
============================

	*  Basically, |mod2doctest| takes your input, fixes any whitespace problems, 
	   and then pipes it to an interpreter using the :mod:`subprocess` module.  
	   
	*  Then, the output is collected and some processing is done to line up the 
	   original module code with the output from subprocess (basically lining 
	   up the '>>>' and '...' which is tricker than it sounds).  
	   
	*  Then, a bunch of post processing is done to process the special 
	   |mod2doctest| comments and nicely format the final docstring. 

This is why the output from mod2doctest is more formatted and readable than 
if you were to just paste a module into the intrepreter yourself. 

Some Notes
==========

A Word Of Warning
-----------------

Here's the warning: **make sure to carefully inspect the output docstring or
final sphinx webpage generated by mod2doctest**. 

|mod2doctest| basically provides a 'snapshot' of the current module run.  
Since it automatically copies the output to the docstring, it can be easy to 
skip the step of actually checking the output and have wrong output in the 
docstring.  That is, just because the test ran does not mean it is what you 
really want. 

To be a useful test fixture that can be used for, say regression testing you
need to make sure the 'snapshot' contains the intended results. 


mod2doctest normally exits at the end of :func:`convert`
--------------------------------------------------------

If a target is given, :func:`convert` calls exit.  This is to stop your 
code being run again since it's already been piped to an interactive 
interpreter once (and that output printed to stdout/stderr for you).


mod2doctest can run your script up to two times
-----------------------------------------------

Just a quick note -- :mod:`mod2doctest` can run your script up to two times
if the ``run_doctest`` parameter is set to ``True``. 

For the example script::

	if __name__ == '__main__':
		import mod2doctest
		mod2doctest.convert(src=True, target='_doctest', run_doctest=True)
	
	print 'Foobar'   

will be execute two times: once when the script is piped to a shell and once
by doctest itself (to check if the doctest does in fact pass)

The script::

	if __name__ == '__main__':
		import mod2doctest
		mod2doctest.convert(src=True, target='_doctest', run_doctest=False)
	
	print 'Foobar'   

will run only once (this one is not run in doctest).

will run once -- just when the module code is piped to the shell.    

.. note:: 

   You may notice this if you have sleep / delay / blocking in your test and 
   your test is slow to run.   If you run mod2doctest like the first example it 
   takes two times longer to run than you might have been expecting.  


Indices and Tables
==================
* :ref:`genindex`
* :ref:`search`
