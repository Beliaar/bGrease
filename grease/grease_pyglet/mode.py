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

__version__ = '$Id$'

import abc
import pyglet
from bGrease.mode import *

class PygletManager(BaseManager):
	"""Mode manager abstract base class using pyglet.
	
	The mode manager keeps a stack of modes where a single mode
	is active at one time. As modes are pushed on and popped from 
	the stack, the mode at the top is always active. The current
	active mode receives events from the manager's event dispatcher.
	"""

	event_dispatcher = None
	""":class:`pyglet.event.EventDispatcher` object that the
	active mode receive events from.
	"""
	
	def activate_mode(self, mode):
		"""Perform actions to activate a node
		
		:param mode: The :class: 'Mode' object to activate
		"""
		BaseManager.activate_mode(self, mode)
		self.event_dispatcher.push_handlers(mode)
		
	def deactivate_mode(self, mode):
		"""Perform actions to deactivate a node
		
		:param mode: The :class: 'Mode' object to deactivate
		"""
		BaseManager.deactivate_mode(self, mode)
		self.event_dispatcher.remove_handlers(mode)

class Manager(PygletManager):
	"""A basic mode manager that wraps a single
	:class:`pyglet.event.EventDispatcher` object for use by its modes.
	"""

	def __init__(self, event_dispatcher):
		self.modes = []
		self.event_dispatcher = event_dispatcher


class ManagerWindow(PygletManager, pyglet.window.Window):
	"""An integrated mode manager and pyglet window for convenience.
	The window is the event dispatcher used by modes pushed to
	this manager.

	Constructor arguments are identical to :class:`pyglet.window.Window`
	"""
	
	def __init__(self, *args, **kw):
		super(ManagerWindow, self).__init__(*args, **kw)
		self.modes = []
		self.event_dispatcher = self

	def on_key_press(self, symbol, modifiers):
		"""Default :meth:`on_key_press handler`, pops the current mode on ``ESC``"""
		if symbol == pyglet.window.key.ESCAPE:
			self.pop_mode()

	def on_last_mode_pop(self, mode):
		"""Hook executed when the last mode is popped from the manager.
		When the last mode is popped from a window, an :meth:`on_close` event
		is dispatched.

		:param mode: The :class:`Mode` object just popped from the manager
		"""
		self.dispatch_event('on_close')


class Mode(BaseMode):
	"""Application mode abstract base class using pyglet

	Subclasses must implement the :meth:`step` method
	
	:param step_rate: The rate of :meth:`step()` calls per second. 

	:param master_clock: The :class:`pyglet.clock.Clock` interface used
		as the master clock that ticks the world's clock. This 
		defaults to the main pyglet clock.
	"""
	clock = None
	"""The :class:`pyglet.clock.Clock` instance used as this mode's clock.
	You should use this clock to schedule tasks for this mode, so they
	properly respect when the mode is active or inactive

	Example::

		my_mode.clock.schedule_once(my_cool_function, 4)
	"""

	def __init__(self, step_rate=60, master_clock=pyglet.clock, 
		         clock_factory=pyglet.clock.Clock):
		BaseMode.__init__(self)
		self.step_rate = step_rate
		self.time = 0.0
		self.master_clock = master_clock
		self.clock = clock_factory(time_function=lambda: self.time)
		self.clock.schedule_interval(self.step, 1.0 / step_rate)
	
	def on_activate(self):
		"""Being called when the Mode is activated"""
		self.master_clock.schedule(self.tick)
	
	def on_deactivate(self):
		"""Being called when the Mode is deactivated"""
		self.master_clock.unschedule(self.tick)
		
	def tick(self, dt):
		"""Tick the mode's clock.

		:param dt: The time delta since the last tick
		:type dt: float
		"""
		self.time += dt
		self.clock.tick(poll=False)
	
	@abc.abstractmethod
	def step(self, dt):
		"""Execute a timestep for this mode. Must be defined by subclasses.
		
		:param dt: The time delta since the last time step
		:type dt: float
		"""

class Multi(BaseMulti, Mode):
	"""A mode with multiple submodes. One submode is active at one time.
	Submodes can be switched to directly or switched in sequence. If
	the Multi is active, then one submode is always active.

	Multis are useful when modes can switch in an order other than
	a LIFO stack, such as in "hotseat" multiplayer games, a
	"wizard" style ui, or a sequence of slides.

	Note unlike a normal :class:`Mode`, a :class:`Multi` doesn't have it's own
	:attr:`clock` and :attr:`step_rate`. The active submode's are used
	instead.
	"""
	
	def __init__(self, submodes):
		BaseMulti.__init__(self, submodes)
		self.time = 0.0

	
	def _set_active_submode(self, submode):
		BaseMulti._set_active_submode(self, submode)
		self.master_clock = submode.master_clock
		self.clock = submode.clock

	def clear_subnode(self):
		"""Clear any subnmode data"""
		BaseMulti.clear_subnode(self)
		self.master_clock = None
		self.clock = None

	def tick(self, dt):
		"""Tick the active submode's clock.

		:param dt: The time delta since the last tick
		:type dt: float
		"""
		self.time += dt
		if self.active_submode is not None:
			self.active_submode.clock.tick(poll=False)

