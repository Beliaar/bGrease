#############################################################################
#
# Copyright (c) 2012 by Karsten Bock and contributors
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT License
# A copy of the license should accompany this distribution.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
#############################################################################
"""
Modes manage the state and transition between different application modes.
Typically such modes are presented as different screens that the user can
navigate between, similar to the way a browser navigates web pages. Individual
modes may be things like:

- Title screen
- Options dialog
- About screen
- In-progress game
- Inventory interface

The modal framework provides a simple mechanism to ensure that modes are
activated and deactivated properly. An activated mode is running and receives
events. A deactivated mode is paused and does not receive events.

Modes may be managed as a *last-in-first-out* stack, or as a list, or ring
of modes in sequence, or some combination of all.

For example usage see: :ref:`the mode section of the tutorial <tut-mode-section>`.
"""

from __future__ import absolute_import
from bGrease.mode import *
import abc

class FifeManager(BaseManager):
        """Mode manager abstract base class using FIFE.
        
        The mode manager keeps a stack of modes where a single mode
        is active at one time. As modes are pushed on and popped from 
        the stack, the mode at the top is always active. The current
        active mode receives events from the manager's event dispatcher.
        """
    
        def __init__(self):
                self.modes = []

        def _pump(self):
            if self.current_mode:
                delta_time = (self.current_mode.engine.getTimeManager().
                                getTimeDelta() / 1000.0)
                self.step(delta_time)
                
        def step(self, dt):
            """Performs actions every frame"""
            if self.current_mode:
                self.current_mode.step(dt)

class Mode(BaseMode):
        """Application mode abstract base class using FIFE
    
        Subclasses must implement the :meth:`pump` method
        
        :param engine: A fife.engine instance 
        """
    
        def __init__(self, engine):
            BaseMode.__init__(self)
            self.engine = engine
