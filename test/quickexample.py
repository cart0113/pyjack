
if __name__ == '__main__':
    import mod2doctest
    mod2doctest.convert(r'C:\Python24\python.exe', src=True,
                        add_autogen=False, target='_doctest',
                        run_doctest=False,)
    
# START


import pyjack

def fakeimport(orgopen, *args, **kwargs):
    
    print 'Trying to import %s' % args[0]
    
    return 'MODULE_%s' % args[0]
    
pyjack.connect(__import__, proxyfn=fakeimport)

import time
print time

__import__.restore()

import time
print time



