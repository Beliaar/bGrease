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

from bGrease.mode import *
import abc

class FifeManager(BaseManager):

        def __init__(self):
                self.modes = []

        def _pump(self):
                if self.current_mode:
                        self.current_mode.pump(self.current_mode.engine.getTimeManager().getTimeDelta() / 1000.0)

class Mode(BaseMode):

        def __init__(self, engine):
            """Constructor
            Args: 
                engine: A fife.Engine instance
            """
            BaseMode.__init__(self)
            self.engine = engine

        @abc.abstractmethod
        def pump(self, dt):
                """Performs actions every frame"""
