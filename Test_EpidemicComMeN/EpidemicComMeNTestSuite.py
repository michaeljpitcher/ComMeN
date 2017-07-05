#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import unittest
import imp
import os

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')
INIT = '__init__'


def package_contents(package_name):
    file_, pathname, description = imp.find_module(package_name)
    if file_:
        raise ImportError('Not a package: %r', package_name)
    # Use a set because some may be both source and compiled.
    return set([os.path.splitext(found_module)[0] for found_module in os.listdir(pathname) if
                found_module.endswith(MODULE_EXTENSIONS) and not found_module.startswith(INIT)])

test_modules = []

packages = os.walk(".").next()[1]

for p in packages:
    modules = package_contents(p)
    for m in modules:
        test_modules.append(p + "." + m)

suite = unittest.TestSuite()

for t in test_modules:
    print "Running: " + t
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)