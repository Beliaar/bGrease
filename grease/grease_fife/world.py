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

from bGrease.world import *
from bGrease.component import Component
from bGrease.grease_fife.mode import Mode

class World(Mode, BaseWorld):

    def __init__(self):
        Mode.__init__(self)
        BaseWorld.__init__(self)
            
    def pump(self, dt):
        for component in self.components:
            if hasattr(component, "step"):
                component.step(dt)
        for system in self.systems:
            if hasattr(system, "step"):
                system.step(dt)
