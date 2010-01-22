from grease import entity

class ComponentEntityManager(object):
	"""manages components and entities. The CEM acts as a container
	for its entities. Component entity sets are exposed as attributes 
	of the CEM. Components themselves can be manipulated via the
	component map accessible through the "components" attribute.
	"""
	_entity_factory = entity.Entity

	def __init__(self, systems=(), **components):
		self._component_map = ComponentMap(self, components)
		self._entities = set()
		self.systems = tuple(systems)
		for system in self.systems:
			if hasattr(system, "set_manager"):
				system.set_manager(self)
		self._entity_id = 0
		self.time = 0
	
	def add_system(self, system):
		"""Add a new system to the manager"""
		if hasattr(system, "set_manager"):
			system.set_manager(self)
		self.systems += (system,)
	
	def remove_system(self, system):
		"""Remove a system from the manager"""
		systems = list(self.systems)
		systems.remove(system)
		self.systems = tuple(systems)
	
	def run(self, dt):
		"""Run a time step for all systems"""
		self.time += dt
		for system in self.systems:
			system.run(dt)

	@property
	def components(self):
		"""Return the component map"""
		return self._component_map
	
	def __contains__(self, entity):
		entity_id = getattr(entity, "entity_id", entity)
		return entity_id in self._entities
	
	def __len__(self):
		return len(self._entities)
	
	def __getitem__(self, entity_id):
		"""Return an entity for the given id"""
		if entity_id in self._entities:
			return self._entity_factory(self, entity_id)
		else:
			raise KeyError(entity_id)
	
	def __delitem__(self, entity):
		entity_id = getattr(entity, "entity_id", entity)
		if entity_id in self._entities:
			for com in self.components:
				try:
					del com[entity_id]
				except KeyError:
					pass
			self._entities.remove(entity_id)
		else:
			raise KeyError(entity_id)
	
	def new_entity(self):
		self._entity_id += 1
		self._entities.add(self._entity_id)
		return self._entity_factory(self, self._entity_id)
	
	def __getattr__(self, name):
		if name in self.components:
			return self.components[name].entity_set
		raise AttributeError(name)
	
	def iter_components(self, *component_names):
		"""Return an iterator of tuples containing data from each
		component specified by name for each entity in all of the
		components
		"""
		components = [self.components[name] for name in component_names]
		entity_ids = components[0].entity_id_set
		for comp in components[1:]:
			entity_ids &= comp.entity_id_set
		for id in entity_ids:
			yield [comp[id] for comp in components]


class ComponentMap(dict):
	"""Maps component names to components"""

	def __init__(self, manager, components):
		self._manager = manager
		for name, comp in components.items():
			self[name] = comp
	
	def __setitem__(self, name, component):
		dict.__setitem__(self, name, component)
		if hasattr(component, 'set_manager'):
			component.set_manager(self._manager)
	
	def __iter__(self):
		return self.itervalues()




