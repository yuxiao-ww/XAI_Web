from collections import defaultdict
from . import modifier
from . import util

from pysat.formula import IDPool, CNF



class Encoder():

	def __init__(self, ground_problem, horizon):
		self.ground_problem = ground_problem
		self.horizon = horizon
		self.modifier = modifier
		self.cnf = CNF()
		self.vpool = IDPool()
		self.var = lambda i: self.vpool.id('{0}'.format(i))
		self.checked = defaultdict()

	## Create boolean variables for boolean fluents and propositional variables for actions ids.



	def createVariables(self):
		"""
		Allocate 2 lists:
		- boolean variables
		- action variable

		Then create IDs for the variables
		"""
		self.actions = self.ground_problem.actions

		self.fluents = set()
		for g in self.ground_problem.actions:
			for p in g.preconditions:
				self.fluents.add(str(p))
			for a in g.effects:
				self.fluents.add(str(a.fluent))


		# for f in self.ground_problem
		# exit()
		# self.boolean_variables = []
		# for fluent in self.ground_problem.facts:
		# 	ground_name = utils.makeName(fluent)
			# lifted_name = utils.remove_steps([ground_name])
			# self.boolean_variables.append(ground_name)

		# self.action_variables = []
		# for action in self.actions:
		# 	ground_name = utils.makeName(action.name)
			# lifted_name = utils.remove_steps([ground_name])
			# self.action_variables.append(ground_name)

		self.actions_all_steps = set()
		self.fluents_all_steps = set()
		for t in range(self.horizon):
			for a in self.actions:
				self.actions_all_steps.add(util.make_step(a.name, t))
			for f in self.fluents:
				self.fluents_all_steps.add(util.make_step(f, t))





	def encodeInitialState(self):
		"""
		Encodes the initial states.
		"""
		inits = list(self.ground_problem._initial_value.keys())
		self.initial = []
		for i in inits:
			init = util.make_step(i, 0)
			if self.var(init) not in self.checked:
				# self.checked.add(self.vpool.id('{0}'.format(init)))
				self.checked[init] = self.vpool.id('{0}'.format(init))
			self.initial.append([self.var(init)])

		for f in self.fluents:
			v = util.make_step(f, 0)
			if self.var(v) not in self.checked:
				# self.checked.add(self.vpool.id('{0}'.format(v)))
				self.checked[v] = self.vpool.id('{0}'.format(v))
			if not [self.var(v)] in self.initial:
				self.initial.append([-self.var(v)])


	## Encode formula defining goal state
	def encodeGoalState(self):
		"""
		Encodes the initial states.
		"""
		self.goals = []
		goals = self.ground_problem.goals

		for g in goals:
			goal = util.make_step(g, self.horizon)
			if self.var(goal) not in self.checked.values():

				# self.checked.add(self.vpool.id('{0}'.format(goal)))
				self.checked[goal] = self.vpool.id('{0}'.format(goal))
			self.goals.append([self.var(goal)])


	def encodeActions(self):
		"""
		Encodes Action Axioms.
		"""

		# self.preconditions = defaultdict(list)
		# self.addition_effects = defaultdict(list)
		# self.deletion_effects = defaultdict(list)
		self.preconditions = []
		self.addition_effects = []
		self.deletion_effects = []

		for t in range(self.horizon):
			for action in self.actions:
				action_t = util.make_step(action.name, t)
				if self.var(action_t) not in self.checked.values():
					# self.checked.add(self.vpool.id('{0}'.format(action_t)))
					self.checked[action_t] = self.vpool.id('{0}'.format(action_t))




				# Encode preconditions
				for pre in action.preconditions:
					pre_t = util.make_step(pre, t)


					if self.var(pre_t) not in self.checked.values():
						# self.checked.add(self.vpool.id('{0}'.format(pre_t)))
						self.checked[pre_t] = self.vpool.id('{0}'.format(pre_t))
					# self.preconditions[lifted_name+" PRE "+lifted_pre_name].append([-self.var(ground_name_time), self.var(ground_pre_name_time)])
					self.preconditions.append([-self.var(action_t), self.var(pre_t)])


				# Encode effects
				for act in action.effects:
					if act.value.is_true(): # Encode add effects

						add_effect_t = util.make_step(act.fluent, t + 1)

						if self.var(add_effect_t) not in self.checked.values():
							# self.checked.add(self.vpool.id('{0}'.format(add_effect_t)))
							self.checked[add_effect_t] = self.vpool.id('{0}'.format(add_effect_t))
							# self.addition_effects[lifted_name+" ADD "+lifted_add_name].append([-self.var(ground_name_time), self.var(ground_add_name_time)])
						self.addition_effects.append([-self.var(action_t), self.var(add_effect_t)])

					elif act.value.is_false(): # Encode del effects
						del_effect_t = util.make_step(act.fluent, t + 1)

						if self.var(del_effect_t) not in self.checked.values():
							# self.checked.add(self.vpool.id('{0}'.format(del_effect_t)))
							self.checked[del_effect_t] = self.vpool.id('{0}'.format(del_effect_t))
							# self.deletion_effects[lifted_name+" DEL "+lifted_del_name].append([-self.var(ground_name_time), -self.var(ground_del_name_time)])
						self.deletion_effects.append([-self.var(action_t), -self.var(del_effect_t)])


	# Encode explanatory Frame Axioms:
	def encodeFrame(self):
		"""
		Encodes the Explanatory Frame Axioms
		"""
		self.frame_axioms = []

		for t in range(self.horizon):
			# Encode frame axioms for boolean fluents
			for fluent in self.fluents:
				action_with_del_fluent = []
				action_with_add_fluent = []

				for action in self.actions:
					action_t = util.make_step(action.name, t)
					add_effects = [str(a.fluent) for a in action.effects if a.value.is_true()]
					del_effects = [str(a.fluent) for a in action.effects if a.value.is_false()]
					# Check if f is in add or del effects of the actions
					if fluent in add_effects:
						# if self.var(action_t) not in self.checked:
						# 	self.checked.add(self.vpool.id('{0}'.format(action_t)))
						action_with_add_fluent.append(action_t)

					elif fluent in del_effects:
						# if self.var(action_t) not in self.checked:
						# 	self.checked.add(self.vpool.id('{0}'.format(action_t)))
						action_with_del_fluent.append(action_t)

				# Explanatory Frame Axiom:
				# If action_with_del_fluent is not zero: ((f_i & -f_i+1) -> Or(a_i))
				if len(action_with_del_fluent) != 0:
					del_actions = [self.var(a) for a in action_with_del_fluent]
					fluent_t = util.make_step(fluent, t)

					if self.var(fluent_t) not in self.checked.values():
						# self.checked.add(self.vpool.id('{0}'.format(fluent_t)))
						self.checked[fluent_t] = self.vpool.id('{0}'.format(fluent_t))

					fluent_t_1 = util.make_step(fluent, t + 1)
					if self.var(fluent_t_1) not in self.checked:
						# self.checked.add(self.vpool.id('{0}'.format(fluent_t_1)))
						self.checked[fluent_t_1] = self.vpool.id('{0}'.format(fluent_t_1))

					frame = [-self.var(fluent_t), self.var(fluent_t_1)]
					# expl_axiom = Implies(frame, del_action)
					del_expl_axiom = frame + del_actions
					self.frame_axioms.append(del_expl_axiom)

				# Else ~fluent_i or fluent_i_plus_1
				else:
					fluent_t = util.make_step(fluent, t)
					if self.var(fluent_t) not in self.checked.values():
						# self.checked.add(self.vpool.id('{0}'.format(fluent_t)))
						self.checked[fluent_t] = self.vpool.id('{0}'.format(fluent_t))
					fluent_t_1 = util.make_step(fluent, t + 1)
					if self.var(fluent_t_1) not in self.checked.values():
						# self.checked.add(self.vpool.id('{0}'.format(fluent_t_1)))
						self.checked[fluent_t_1] = self.vpool.id('{0}'.format(fluent_t_1))
					# frame = Or(Not(Bool(ground_fluent_i)), Bool(ground_fluent_i_plus_1))
					frame = [-self.var(fluent_t), self.var(fluent_t_1)]
					self.frame_axioms.append(frame)

				# If action_add_fluent is not zero: ((-f_i & f_i+1) -> Or(a_i))
				if len(action_with_add_fluent) != 0:
					add_actions = [self.var(a) for a in action_with_add_fluent]
					fluent_t = util.make_step(fluent, t)
					if self.var(fluent_t) not in self.checked.values():
						# self.checked.add(self.vpool.id('{0}'.format(fluent_t)))
						self.checked[fluent_t] = self.vpool.id('{0}'.format(fluent_t))
					fluent_t_1 = util.make_step(fluent, t + 1)
					if self.var(fluent_t_1) not in self.checked.values():
						# self.checked.add(self.vpool.id('{0}'.format(fluent_t_1)))
						self.checked[fluent_t_1] = self.vpool.id('{0}'.format(fluent_t_1))

					# frame = And(Not(Bool(ground_fluent_i)), Bool(ground_fluent_i_plus_1))
					frame = [self.var(fluent_t), -self.var(fluent_t_1)]
					# expl_axiom = Implies(frame, adCNF_Encoder.pyd_action)
					add_expl_axiom = frame + add_actions
					self.frame_axioms.append(add_expl_axiom)
				# Else fluent_i or ~fluent_i_plus_1
				else:
					fluent_t = util.make_step(fluent, t)
					if self.var(fluent_t) not in self.checked.values():
						# self.checked.add(self.vpool.id('{0}'.format(fluent_t)))
						self.checked[fluent_t] = self.vpool.id('{0}'.format(fluent_t))
					fluent_t_1 = util.make_step(fluent, t + 1)
					if self.var(fluent_t_1) not in self.checked.values():
						# self.checked.add(self.vpool.id('{0}'.format(fluent_t_1)))
						self.checked[fluent_t_1] = self.vpool.id('{0}'.format(fluent_t_1))
					# frame = Or(Bool(ground_fluent_i), Not(Bool(ground_fluent_i_plus_1)))
					frame = [self.var(fluent_t), -self.var(fluent_t_1)]
					self.frame_axioms.append(frame)


	## Encode The Execution Semantics
	def encodeExecutionSemantics(self):
		"""
		Encodes the action mutexes (linear execution). Can be modified to do parallel execution.
		"""
		# exclusions = modifier.EncodeModifier(self.actions, self.horizon)
		# if self.modifier is True:
			# return modicator.encode_parallel_modifier()
		# else:
		# return exclusions.encode_linear_modifier()
		mutexes = []

		for h in range(self.horizon):
			for a1 in self.actions:
				for a2 in self.actions:
					if a1.name != a2.name:

						A1 = util.make_step(a1.name, h)
						if self.var(A1) not in self.checked.values():

							# self.checked.add(self.vpool.id('{0}'.format(A1)))
							self.checked[A1] = self.vpool.id('{0}'.format(A1))
						A2 = util.make_step(a2.name, h)
						if self.var(A2) not in self.checked.values():
							# print('here')
							# self.checked.add(self.vpool.id('{0}'.format(A2)))
							self.checked[A2] = self.vpool.id('{0}'.format(A2))
							# print(self.var(A2))
						mutexes.append([-self.var(A1), -self.var(A2)])
		return mutexes


	## Encode The Propositional Formula
	def encode(self):
		"""
		Encode the KB.
		"""
		# Create variables
		self.createVariables()

		# Encode initial state axioms
		self.encodeInitialState()

		# # Encode goal state axioms
		self.encodeGoalState()

		# Encode universal axioms
		self.encodeActions()

		# # Encode explanatory frame axioms
		self.encodeFrame()

		# Encode execution semantics (lin/par)
		excls = self.encodeExecutionSemantics()

		# Encode causal links
		# self.encodeCausalLinks()

		KB = util.planningKB(self.horizon, self.fluents_all_steps, self.actions_all_steps, self.vpool, self.initial, self.goals, self.preconditions, self.addition_effects, self.deletion_effects,
						self.frame_axioms, excls)


		return KB, self.checked

