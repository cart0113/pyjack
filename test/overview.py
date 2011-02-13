if __name__ == '__main__':
    import mod2doctest
    mod2doctest.convert(r'C:\Python26\python.exe', src=True,
                        add_autogen=False, target='_doctest',
                        run_doctest=False,)
    
    
#>Basic idea: pyjacking a function
#>------------------------------------------------------------------------------

#|A couple of quick examples is probably best -- just note 'filters' are called
#|before a function executes, 'callbacks' are called after a function executes
#|(unless ``block`` is set ``True``, than the function is never called): 

#|Let's say you want to 1. monitor and 2. prevent every time something is 
#|opening a file:
import pyjack

def fakeopen(*args, **kwargs):
    print 'Someone is trying to open a file with:', args, kwargs
    return ()
    
pyjack.connect(open, callback=fakeopen, block=True)

for line in open('/some/path', 'r'):
    print line

#|Or you don't want to block:
import time

def hitime(*args, **kwargs):
    print 'Hi, here is the time in seconds since 1970:',

pyjack.connect(time.time, filter=hitime)

print time.time()

#|Of course, this works on user function / class methods, too:
def mysort(x, y, z=10):
    return sorted([x, y, z])

def no_negs(x, y, z):
    # "filter" functions can return args, kwargs
    return [abs(x), abs(y), abs(z)], {}
    
pyjack.connect(mysort, filter=no_negs)

mysort(-100, 20, 50)

#>So, there you have it: ``filter`` functions are called before orginal 
#>function execution and can alter args, kwargs.  ``callbacks`` are called 
#>after and, if they return non ``None`` values, set the return value. 


print    





