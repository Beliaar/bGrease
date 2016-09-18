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
"""Worlds are environments described by a configuration of components, systems and 
renderers. These parts describe the data, behavioral and presentation aspects
of the world respectively.

The world environment is the context within which entities exist. A typical
application consists of one or more worlds containing entities that evolve
over time and react to internal and external interaction.

See :ref:`an example of world configuration in the tutorial <tut-world-example>`.
"""

from __future__ import absolute_import
from bGrease.world import *
from bGrease.component import Component
from bGrease.grease_fife.mode import Mode

class World(Mode, BaseWorld):
    """A coordinated collection of components, systems and entities
    
    A world is also a mode that may be pushed onto a 
    :class:`bGrease.mode.Manager`

    :param engine: A fife.engine instance 
    """
    
    def __init__(self, engine):
        Mode.__init__(self, engine)
        BaseWorld.__init__(self)
            
    def step(self, dt):
        for component in self.components:
            if hasattr(component, "step"):
                component.step(dt)
        for system in self.systems:
            if hasattr(system, "step"):
                system.step(dt)
