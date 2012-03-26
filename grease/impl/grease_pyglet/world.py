#############################################################################
#
# Copyright (c) 2010 by Casey Duncan and contributors
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

__version__ = '$Id$'

import itertools
import pyglet
from pyglet import gl
from bGrease.world import *
from bGrease.impl.grease_pyglet import Mode

class World(Mode, BaseWorld):
	"""A coordinated collection of components, systems and entities
	
	A world is also a mode that may be pushed onto a 
	:class:`bGrease.mode.Manager`

	:param step_rate: The rate of :meth:`step()` calls per second. 

	:param master_clock: The :class:`pyglet.clock.Clock` interface used
		as the master clock that ticks the world's clock. This 
		defaults to the main pyglet clock.
	"""

	clock = None
	""":class:`pyglet.clock` interface for use by constituents
	of the world for scheduling
	"""

	time = None
	"""Current clock time of the world, starts at 0 when the world
	is instantiated
	"""

	running = True
	"""Flag to indicate that the world clock is running, advancing time
	and stepping the world. Set running to False to pause the world.
	"""

	def __init__(self, step_rate=60, master_clock=pyglet.clock,
				 clock_factory=pyglet.clock.Clock):
		Mode.__init__(self, step_rate, master_clock, clock_factory)
		BaseWorld.__init__(self)
	
	def activate(self, manager):
		"""Activate the world/mode for the given manager, if the world is already active, 
		do nothing. This method is typically not used directly, it is called
		automatically by the mode manager when the world becomes active.

		The systems of the world are pushed onto `manager.event_dispatcher`
		so they can receive system events.

		:param manager: :class:`mode.BaseManager` instance
		"""
		if not self.active:
			for system in self.systems:
				manager.event_dispatcher.push_handlers(system)
		super(World, self).activate(manager)
	
	def deactivate(self, manager):
		"""Deactivate the world/mode, if the world is not active, do nothing.
		This method is typically not used directly, it is called
		automatically by the mode manager when the world becomes active.

		Removes the system handlers from the `manager.event_dispatcher`

		:param manager: :class:`mode.BaseManager` instance
		"""
		for system in self.systems:
			manager.event_dispatcher.remove_handlers(system)
		super(World, self).deactivate(manager)

	def tick(self, dt):
		"""Tick the mode's clock, but only if the world is currently running
		
		:param dt: The time delta since the last tick
		:type dt: float
		"""
		if self.running:
			super(World, self).tick(dt)
	
	def step(self, dt):
		"""Execute a time step for the world. Updates the world `time`
		and invokes the world's systems.
		
		Note that the specified time delta will be pinned to 10x the
		configured step rate. For example if the step rate is 60,
		then dt will be pinned at a maximum of 0.1666. This avoids 
		pathological behavior when the time between steps goes
		much longer than expected.

		:param dt: The time delta since the last time step
		:type dt: float
		"""
		dt = min(dt, 10.0 / self.step_rate)
		for component in self.components:
			if hasattr(component, "step"):
				component.step(dt)
		for system in self.systems:
			if hasattr(system, "step"):
				system.step(dt)

	def on_draw(self, gl=pyglet.gl):
		"""Clear the current OpenGL context, reset the model/view matrix and
		invoke the `draw()` methods of the renderers in order
		"""
		gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
		gl.glLoadIdentity()
		BaseWorld.draw_renderers(self)
