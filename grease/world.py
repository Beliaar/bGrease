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

from __future__ import absolute_import
__version__ = '$Id$'

import itertools
from bGrease import mode
from bGrease.component import ComponentError
from bGrease.entity import Entity, ComponentEntitySet


class BaseWorld(object):
	"""A coordinated collection of components, systems and entities
	
	A world is also a mode that may be pushed onto a 
	:class:`bGrease.mode.Manager`
	"""

	components = None
	""":class:`ComponentParts` object containing all world components.
	:class:`bGrease.component.Component` objects define and contain all entity data
	"""

	systems = None
	""":class:`Parts` object containing all world systems. 
	:class:`bGrease.System` objects define world and entity behavior
	"""

	renderers = None
	""":class:`Parts` object containing all world renderers. 
	:class:`bGrease.Renderer` objects define world presentation
	"""

	entities = None
	"""Set of all entities that exist in the world"""

	def __init__(self):
		self.components = ComponentParts(self)
		self.systems = Parts(self)
		self.renderers = Parts(self)
		self.new_entity_id = lambda x=itertools.count(): next(x)
		self.new_entity_id() # skip id 0
		self.entities = WorldEntitySet(self)
		self._full_extent = EntityExtent(self, self.entities)
		self._extents = {}
		self.configure()

	def configure(self):
		"""Hook to configure the world after construction. This method
		is called immediately after the world is initialized. Override
		in a subclass to configure the world's components, systems,
		and renderers.

		The default implementation does nothing.
		"""
	
	def __getitem__(self, entity_class):
		"""Return an :class:`EntityExtent` for the given entity class. This extent
		can be used to access the set of entities of that class in the world
		or to query these entities via their components. 

		Examples::

			world[MyEntity]
			world[...]

		:param entity_class: The entity class for the extent.

			May also be a tuple of entity classes, in which case
			the extent returned contains union of all entities of the classes
			in the world.

			May also be the special value ellipsis (``...``), which
			returns an extent containing all entities in the world.  This allows
			you to conveniently query all entities using ``world[...]``.
		"""
		if isinstance(entity_class, tuple):
			entities = set()
			for cls in entity_class:
				if cls in self._extents:
					entities |= self._extents[cls].entities
			return EntityExtent(self, entities)
		elif entity_class is Ellipsis:
			return self._full_extent
		try:
			return self._extents[entity_class]
		except KeyError:
			extent = self._extents[entity_class] = EntityExtent(self, set())
			return extent
	
	def draw_renderers(self):
		"""Draw all renderers"""
		for renderer in self.renderers:
			renderer.draw()

class WorldEntitySet(set):
	"""Entity set for a :class:`World`"""

	def __init__(self, world):
		self.world = world
	
	def add(self, entity):
		"""Add the entity to the set and all necessary class sets
		Return the unique entity id for the entity, creating one
		as needed.
		"""
		super(WorldEntitySet, self).add(entity)
		for cls in entity.__class__.__mro__:
			if issubclass(cls, Entity):
				self.world[cls].entities.add(entity)

	def remove(self, entity):
		"""Remove the entity from the set and, world components,
		and all necessary class sets
		"""
		super(WorldEntitySet, self).remove(entity)
		for component in self.world.components:
			try:
				del component[entity]
			except KeyError:
				pass
		for cls in entity.__class__.__mro__:
			if issubclass(cls, Entity):
				self.world[cls].entities.discard(entity)
	
	def discard(self, entity):
		"""Remove the entity from the set if it exists, if not,
		do nothing
		"""
		try:
			self.remove(entity)
		except KeyError:
			pass


class EntityExtent(object):
	"""Encapsulates a set of entities queriable by component. Extents
	are accessed by using an entity class as a key on the :class:`World`::

		extent = world[MyEntity]
	"""

	entities = None
	"""The full set of entities in the extent""" 

	def __init__(self, world, entities):
		self.__world = world
		self.entities = entities

	def __getattr__(self, name):
		"""Return a queriable :class:`ComponentEntitySet` for the named component 

		Example::

			world[MyEntity].movement.velocity > (0, 0)

		Returns a set of entities where the value of the :attr:`velocity` field
		of the :attr:`movement` component is greater than ``(0, 0)``.
		"""
		component = getattr(self.__world.components, name)
		return ComponentEntitySet(component, self.entities & component.entities)


class Parts(object):
	"""Maps world parts to attributes. The parts are kept in the
	order they are set. Parts may also be inserted out of order.
	
	Used for:
	
	- :attr:`World.systems`
	- :attr:`World.renderers`
	"""

	_world = None
	_parts = None
	_reserved_names = ('entities', 'entity_id', 'world')

	def __init__(self, world):
		self._world = world
		self._parts = []
	
	def _validate_name(self, name):
		if (name in self._reserved_names or name.startswith('_') 
			or hasattr(self.__class__, name)):
			raise ComponentError('illegal part name: %s' % name)
		return name

	def __setattr__(self, name, part):
		if not hasattr(self.__class__, name):
			self._validate_name(name)
			if not hasattr(self, name):
				self._parts.append(part)
			else:
				old_part = getattr(self, name)
				self._parts[self._parts.index(old_part)] = part
			super(Parts, self).__setattr__(name, part)
			if hasattr(part, 'set_world'):
				part.set_world(self._world)
		elif name.startswith("_"):
			super(Parts, self).__setattr__(name, part)
		else:
			raise AttributeError("%s attribute is read only" % name)
	
	def __delattr__(self, name):
		self._validate_name(name)
		part = getattr(self, name)
		self._parts.remove(part)
		super(Parts, self).__delattr__(name)

	def insert(self, name, part, before=None, index=None):
		"""Add a part with a particular name at a particular index.
		If a part by that name already exists, it is replaced.
			
		:arg name: The name of the part.
		:type name: str

		:arg part: The component, system, or renderer part to insert
	
		:arg before: A part object or name. If specified, the part is
			inserted before the specified part in order.

		:arg index: If specified, the part is inserted in the position
			specified. You cannot specify both before and index.
		:type index: int
		"""
		assert before is not None or index is not None, (
			"Must specify a value for 'before' or 'index'")
		assert before is None or index is None, (
			"Cannot specify both 'before' and 'index' arguments when inserting")
		self._validate_name(name)
		if before is not None:
			if isinstance(before, str):
				before = getattr(self, before)
			index = self._parts.index(before)
		if hasattr(self, name):
			old_part = getattr(self, name)
			self._parts.remove(old_part)
		self._parts.insert(index, part)
		super(Parts, self).__setattr__(name, part)
		if hasattr(part, 'set_world'):
			part.set_world(self._world)

	def __iter__(self):
		"""Iterate the parts in order"""
		return iter(tuple(self._parts))
	
	def __len__(self):
		return len(self._parts)


class ComponentParts(Parts):
	"""Maps world components to attributes. The components are kept in the
	order they are set. Components may also be inserted out of order.

	Used for: :attr:`World.components`
	"""

	def join(self, *component_names):
		"""Join and iterate entity data from multiple components together.

		For each entity in all of the components named, yield a tuple containing
		the entity data from each component specified.

		This is useful in systems that pull data from multiple components.
		
		Typical Usage::

			for position, movement in world.components.join("position", "movement"):
				# Do something with each entity's position and movement data
		"""
		if component_names:
			components = [getattr(self, self._validate_name(name)) 
				for name in component_names]
			if len(components) > 1:
				entities = components[0].entities & components[1].entities
				for comp in components[2:]:
					entities &= comp.entities
			else:
				entities = components[0].entities
			for entity in entities:
				yield tuple(comp[entity] for comp in components)

