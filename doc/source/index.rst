.. role:: raw-html(raw)
   :format: html

.. |pyjack|  replace:: :mod:`pyjack`

pyjack
******

.. sectionauthor:: Andrew Carter <andrewjcarter@gmail.com>.

The :mod:`pyjack` is a small debug / test module that allows you to: 

* Connect a 'spy' function to almost any python function.  This spy function
  is called instead of the original function.  The original function is passed
  to the spy function along with all args, kwargs so you can call the original
  function; modify the args, kwargs first, print a debug message, then call it; 
  not call the function, just log it or print a debug message; etc. etc.   
  
* Provides a convenience function :func:`replace_all_refs` which can be used
  to replace all references to a object with references to another objects. 

Here's a quick example: 

.. automodule:: quickexample_doctest
  
Overall, the main purpose of pyjack is for debugging, unit testing, etc.  For
example: 

* using pyjack to pyjack :func:`__import__` to see what modules are 
  being imported 
  
or:  

* pyjacking :func:`time.time` to return integers for a unit test

etc. 

Basically, what does it do?
---------------------------

:func:`connect` works in two ways: 

* For functions of type :class:`types.FunctionType` or
  :class:`types.MethodType` the :attr:`func_code` of the function is altered. 
  This is done so *all* references to the function are altered. 
  
* For builtin functions, the :func:`replace_all_refs` is used.  This function
  uses the :mod:`gc` module to search for all references. This is because 
  you can't tinker with a builtin functions :attr:`func_code`.  
  
Updating the :attr:`func_code` is preferred because it is a fast, local 
operation -- :func:`replace_all_refs` has to search entire memory space. So 
the :attr:`func_code` approach is used when possible. 
  
The overall idea of pyjack is to update *all* references in memory.  For 
example, code like this::

    def faketime():
        return 0
    
    import time
    
    time.time = faketime
    
only changes the one reference -- if other references to the original functions
or objects exist, they are not updated. 

Overall, It's kind of trivial module, but it's proven a useful from time to
time. And while short, the exact mechanics of the receipe of how to replace 
*all* references to a function / object in memory might be useful for someone 
looking to do something similar. 


.. note::

   :func:`connect` and :func:`replace_all_refs` can not work on objects in 
   a :attr:`func_closure` since objects there are of :class:`cell` type and 
   cannot be modified. 

   

.. note::

   Should it be used in so called "production code"?  Well, the :mod:`inspect` 
   module and the :mod:`gc` module and used and some low level objects 
   attributes are tinkered with.  So you get the idea: use at your own risk 
   (but isn't that always the case?).  
     

Installation for Python 2.4 through 2.7
=======================================

Try::

    pip install pyjack

or::    

    easy_install pyjack 

Or, grab the windows installer, egg, or source from:

* http://pypi.python.org/pypi/pyjack/.

Or, grab the source code from: 

* https://github.com/cart0113/pyjack 


:mod:`pyjack`
=============

.. automodule:: pyjack
   :members:


Some Doctest Examples
=====================

These are unit doctests that also serve as documentation. 

.. automodule:: overview_doctest



Indices and Tables
==================
* :ref:`genindex`
* :ref:`search`
