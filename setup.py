import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mod2doctest",
    version = "0.3.0",
    author = "Andrew Carter",
    author_email = "andrewjcarter@gmail.com",
    description = "Tools to attach filter/callback functions to functions.",
    license = "MIT",
    keywords = "debug callback profile",
    url = "http://packages.python.org/pyjack/",
    packages=['mod2doctest'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
