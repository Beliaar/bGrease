bGrease Overview
================

bGrease is a fork of Grease that makes it possible to use grease with other modules than pyglet and a few other modifications.
Note that this will NOT add any other new functionality to Grease.

Grease is a pluggable and highly extensible 2D game engine and framework for
Python.

The intent of this project is to provide a fresh approach to Python game
development. The component-based architecture allows games to be constructed
bit by bit with built-in separation of concerns. The engine acknowledges that
all game projects are unique and have different requirements. Thus bGrease does
not attempt to provide one-size-fits-all solutions. Instead it provides
pluggable components and systems than can be configured, adapted and extended
to fits the particular needs at hand.

The goals of the project include:

* Making Python game development faster and more fun by allowing the developer
  to focus on creating their game rather than getting bogged down in
  architecture, low-level apis and adapting ill-fitting tools together.

* To provide pluggable and extensible parts that implement first-class
  techniques and algorithms that can be leveraged for many projects.

* To fully document the engine and provide examples that demonstrate best
  practices for others to base their projects on.

* To facilitate outside contribution of parts and ideas into the framework
  that have proven useful in the wild.

* To provide optional native-code optimized parts for maximum performance,
  but also provide equivalent parts coded in pure Python for ease
  of installation and distribution.

Not all of these goals have been realized yet, but I feel the project is well
on their path.

License
-------

bGrease is distributed under a permissive MIT-style open source license. This
license permits you to use grease for commercial or non-commercial purposes
free of charge. It makes no demands on how, or whether, you license, or
release the code derived from or built upon bGrease, other than preservation of
copyright notice.

For a complete text of the license see the ``LICENSE.txt`` file in the source
distrbution.

Requirements
------------

bGrease is platform-independent and should run on any operating system
supporting Python and Pyglet.

The following are required to build and install bGrease:

* Python 2.6 or higher(http://www.python.org/)

If using the pyglet modules:
* Pyglet 1.1 (http://www.pyglet.org/) 

Downloading bGrease
-------------------

You can clone the github repository to get the very latest code:

	git clone git@github.com:Beliaar/bGrease.git

Although there is no guarantee that the latest master branch code will work
perfectly, or even make it to release, efforts are made to ensure bGrease is
functional at each push.

Installation
------------

To install bGrease from the source distribution or repository use::

    python2.6 setup.py install

Once installed you can try it out by running the unit tests and the
included example game, but make sure you leave the grease source directory
first or they will not work properly::

	cd
	python2.6 -m grease.test.run_all
	python2.6 -m grease.examples.blasteroids3

Note on some platforms, such as MacOS X, you will need to use ``pythonw2.6``
to run the tests and example game.

Note, you can also try out bGrease without installing it by setting your
``PYTHONPATH`` to the source directory::

	export PYTHONPATH=`pwd`
	python2.6 test/run_all.py
	python2.6 examples/blasteroids3.py

Documentation
-------------

You can browse the original grease documentation online at:

* http://packages.python.org/grease/

This does, however, not include changes made by bGrease.

The documentation, with changes by bGrease, is also available for offline viewing in the
``doc/build/html`` subdirectory for the source distribution.

Development Status
------------------

Grease is alpha software under active development. The APIs may change in
future releases, however efforts will be made to minimize breakage between
releases.

Contributing and Getting Support
--------------------------------
Note that this section mainly applies to Grease and not bGrease.
I don't read the google users group, for example.

Come visit us at the Grease users google group to get help, moral support,
lavish praise, complain bitterly, report a bug, or contribute ideas:

* http://groups.google.com/group/grease-users

If you would like to contribute to Grease, feel free to fork the git
repository and make a pull request to have your changes reviewed. Note that
bug fixes must be accompanied by unit tests, and features must also be
documented.  I am happy to help with these tasks if I can, so don't be afraid
to ask!

