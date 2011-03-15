
if __name__ == '__main__':
    import mod2doctest
    mod2doctest.convert(r'C:\Python24\python.exe', src=True,
                        add_autogen=False, target='_doctest',
                        run_doctest=False,)
    


#>The import:
import pyjack

#>Show the "connect" function:
def fakeimport(orgopen, *args, **kwargs):    
    print 'Trying to import %s' % args[0]
    return 'MODULE_%s' % args[0]
    
pyjack.connect(__import__, proxyfn=fakeimport)

import time
print time

__import__.restore()

import time
print time

#>Show the "replace all refs" function:
item = (100, 'one hundred')
data = {item: True, 'itemdata': item}

class Foobar(object):
    the_item = item

def outer(datum):
    def inner():
        return ("Here is the datum:", datum,)
    return inner
    
inner = outer(item)

print item
print data
print Foobar.the_item
print inner()

#>Then replace them:
new = (101, 'one hundred and one')
org_item = pyjack.replace_all_refs(item, new)

print item
print data
print Foobar.the_item
print inner()

#>But you still have the org data:
print org_item

#>So the process is reversible: 
new = pyjack.replace_all_refs(new, org_item)

print item
print data
print Foobar.the_item
print inner()















