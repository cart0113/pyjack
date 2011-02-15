import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyjack",
    version = "0.3.1",
    author = "Andrew Carter",
    author_email = "andrewjcarter@gmail.com",
    description = ("Tools to reversibly replace functions / objects with "
                   "proxy functions / objects for debug, testing, "
                   "monkey-patching."),
    license = "MIT",
    keywords = "debug callback test monkey monkey-patch",
    url = "http://packages.python.org/pyjack/",
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    py_modules=['pyjack'],
    zip_safe=True,
)
