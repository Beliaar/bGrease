#!/usr/bin/env python

# $Id$

from builtins import range
import os
import sys
import shutil
from distutils.core import setup, Extension

srcdir = os.path.dirname(__file__)

def read(fname):
    return open(os.path.join(srcdir, fname)).read()

# Copy the blasteroids example scripts to the tutorial dir
# Ideally they would just live there, but inflexibility in
# distutils wrt packaging data makes this necessary
for i in range(1, 4):
    shutil.copyfile(
        os.path.join(srcdir, 'examples', 'blasteroids%s.py' % i),
        os.path.join(srcdir, 'doc', 'tutorial', 'blasteroids%s.py' % i))

setup(
    name='bGrease',
    version='0.3', # *** REMEMBER TO UPDATE __init__.py ***
    description='BasicGrease: The highly extensible game engine framework for Python',
    long_description=read('README.txt'),
    author='Casey Duncan',
    author_email='casey.duncan@gmail.com',
    # url='',
    license='MIT',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        ],

    package_dir={'bGrease': 'grease', 
                 'bGrease.controller': 'grease/controller',
                 'bGrease.component': 'grease/component',
                 'bGrease.renderer': 'grease/renderer',
                 'bGrease.grease_pyglet': 'grease/grease_pyglet',
                 'bGrease.grease_fife': 'grease/grease_fife',
                 'bGrease.test': 'test',
                 'bGrease.examples': 'examples'},
    package_data={'bGrease.examples': ['font/*', 'sfx/*']},
    packages=['bGrease', 
              'bGrease.controller', 
              'bGrease.component', 
              'bGrease.renderer', 
              'bGrease.grease_pyglet',
              'bGrease.grease_fife',
              'bGrease.test',
              'bGrease.examples'],
)
