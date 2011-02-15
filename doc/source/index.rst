.. role:: raw-html(raw)
   :format: html

.. |pyjack|  replace:: :mod:`pyjack`

pyjack
******

.. sectionauthor:: Andrew Carter <andrewjcarter@gmail.com>.

pyjack is a debug/test/monkey-patching toolset that allows you to reversibly
replace *all* references to a function or object in memory with a 
proxy function or object. pyjack's has two major functions: 

* :func:`connect` can connect a 'proxy' function to almost 
  any python function/method.  This proxy function is called instead of the 
  original function.  However, the original function is passed to the proxy 
  function along with all args, kwargs so you can do things like:
  
  - Modify the args, kwargs first, print a debug message, then call the original
    function
  - Not call the function, rather just log it and print a debug message
   
  etc. etc. -- it's all up to you. 
  
* :func:`replace_all_refs` can be used to replace all 
  references to a object with references to another object. This replaces all 
  references in the _entire_ memory space. 

Here's a quick example: 

.. automodule:: quickexample_doctest
  
Overall, the main purpose of pyjack is for debugging, unit testing, general
purpose monkey-patching, etc.  For example: 
a
* using pyjack to pyjack :func:`__import__` to see what modules are 
  being imported 
  
or:  

* pyjacking :func:`time.time` to return integers for a unit test

Basically, what does it do?
---------------------------

:func:`connect` works in two ways: 

* For functions of type :class:`types.FunctionType` or
  :class:`types.MethodType` the :attr:`func_code` of the function is altered. 
  This is done so *all* references to the function are altered. 
  
* For builtin functions, the :func:`replace_all_refs` is used.  This function
  uses the :mod:`gc` module to search for all references in the entire memory
  space. This is because you can't tinker with a builtin function's 
  :attr:`func_code`.  
  
Updating the :attr:`func_code` is preferred because it is a fast, local 
operation -- :func:`replace_all_refs` has to call out to :mod:`gc`. So 
the :attr:`func_code` approach is used whenever possible. 
  
The overall idea of pyjack is to update *all* references in memory.  For 
example, code like this::

    def faketime():
        return 0
    
    import time
    
    time.time = faketime
    
only changes the one reference -- if other references to the original function
or object exist, they are not updated. 

Overall, it's a bit of a experimental tool, but it's proven a useful from time 
to time. And while short, the exact mechanics of the recipe of how to replace 
all references to a function / object in memory might be useful for someone 
looking to do something similar. 
   

.. note::

   Should it be used in so called "production code"?  Well, the :mod:`inspect` 
   module and the :mod:`gc` module are used and some low level object 
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
    