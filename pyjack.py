import sys as _sys
import gc as _gc
import types as _types


_WRAPPER_TYPES = (type(object.__init__), type(object().__init__),)


class Exception(Exception): pass


def connect(fn, filter=None, callback=None, block=False, passfn=False):    
    """
    :summary:         Connects a filter/callback function to a function/method.
                      
    :param fn:        The function which to connect.  Omitted when used as 
                      a decorator. 
        
    :param filter:    A filter function that is called *before* the ``fn`` 
                      function is called.  This function must return an 
                      ``(args, kwargs,)`` tuple that will be the args, kwargs 
                      passed to the original ``fn``. This way, you either 
                      pass the args, kwargs to the ``fn`` untouched or you 
                      can first 'filter' the arguments passed to ``fn``.
    :type filter:     callable. 

    :param callback:  A callback function that will be called *after* the ``fn`` 
                      function is called.  Finally, if this callback function 
                      returns anything other than ``None``, it's value will be 
                      returned instead of the value of the original ``fn`` 
                      function. 
    :type callback:   callable
    
    :param block:     If ``True``, this will block the original ``fn`` 
                      from being called.         
    :type block:      ``True`` or ``False``

    :param passfn:    If ``True``, the org fn will be passed to filter/callback.      
    :type passfn:     ``True`` or ``False``
        
    :returns:         The new function. 
                      
    :raises:          :class:`PyjackError`

    """
    
    fn_type = type(fn)

    if issubclass(fn_type, _types.FunctionType):
        newfn = _PyjackFuncCode(fn, filter, callback, block, passfn)
    elif issubclass(fn_type, _types.MethodType):
        newfn = _PyjackFuncCode(fn.im_func)
    elif issubclass(fn_type, (_types.BuiltinFunctionType, 
                              _types.BuiltinMethodType,)):
        newfn = _PyjackFuncBuiltin(fn, filter, callback, block, passfn)
    elif issubclass(fn_type, _WRAPPER_TYPES):
        raise Exception("Wrappers not supported. Make a concrete fn.")
    else:
        raise Exception("'r' not supported" % fn_type)
    
    return newfn.fn


def restore(fn):
    fn.restore()


def replace_all_refs(org_obj, new_obj):

    _gc.collect()

    hit = False    
    for referrer in _gc.get_referrers(org_obj):

        # DICTS
        if isinstance(referrer, dict):
            for key, value in referrer.iteritems():
                if value is org_obj:
                    hit = True
                    referrer[key] = new_obj
        
        # LISTS
        elif isinstance(referrer, list):
            for i, value in enumerate(referrer):
                if value is fn:
                    hit = True
                    referrer[i] = new_obj
        
        # SETS
        elif isinstance(referrer, set):
            referrer.remove(org_obj)
            referrer.add(new_obj)
            hit = True

    if hit is False:
        raise AttributeError("Object '%r' not found" % org_obj)

    return org_obj


_func_code_map = {}
def _get_self():

    global _func_code_map
    
    frame = _sys._getframe()
    code = frame.f_back.f_code
    return _func_code_map[code]


class _PyjackFunc(object):

    def __init__(self, fn, filter, callback, block, passfn):
                
        self.fn = fn
        self._filter = filter
        self._callback = callback
        self._block = block
        self._passfn = passfn

    @staticmethod    
    def _call(fn, filter, callback, block, passfn, args, kwargs):
        if passfn:
            args = [fn] + list(args)
        if filter:
            args, kwargs = filter(*args, **kwargs) or (args, kwargs)
        value = None
        if not block:
            value = fn(*args, **kwargs)
        if callback:
            newvalue = callback(*args, **kwargs)
            return newvalue if newvalue is not None else value
        else:
            return value

    
class _PyjackFuncCode(_PyjackFunc):
            
    def __init__(self, fn, filter, callback, block, passfn):

        global _func_code_map
                
        _PyjackFunc.__init__(self, fn, filter, callback, block, passfn)
              
        def proxy(*args, **kwargs):
            import pyjack
            self = pyjack._get_self()
            return self._process_fn(args, kwargs)

        _func_code_map[proxy.func_code] = self
        self._org_func_code = fn.func_code
        self._proxy_func_code = proxy.func_code
        fn.func_code = proxy.func_code

        fn.restore = self.restore

    def _process_fn(self, args, kwargs):
        self.fn.func_code = self._org_func_code
        value = self._call(
            self.fn, self._filter, self._callback, self._block, self._passfn, 
            args, kwargs)
        self.fn.func_code = self._proxy_func_code
        return value 
    
    def restore(self):
        self.fn.func_code = self._org_func_code
        

class _PyjackFuncBuiltin(_PyjackFunc):
        
    def __init__(self, fn, filter, callback, block, passfn):
        _PyjackFunc.__init__(self, fn, filter, callback, block, passfn)
        self.fn = replace_all_refs(fn, self)

    def __call__(self, *args, **kwargs):
        return self._call(
            self.fn, self._filter, self._callback, self._block, self._passfn, 
            args, kwargs)
                
    def restore(self):
        replace_all_refs(self, self.fn)
        



