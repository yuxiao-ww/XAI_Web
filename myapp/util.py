from pysat.solvers import Solver
from pysat.examples.hitman import Hitman
from pysat.formula import WCNF
from pysat.examples.musx import MUSX
from pysat.examples.lbx import LBX
from collections import defaultdict


def skeptical_entailment(KB, seed, q):
	# Check if KB entails a query

	s = Solver(name='g4')
	for k in KB:
		s.add_clause(k)
	for k in seed:
		s.add_clause(k)
	# add negation of query
	s.append_formula(q.negate().clauses)
	if s.solve() == False:
		return True
	else: return False



def sat(KB_clauses, seed):
	# Check if a formula is satisfiable
	s = Solver(name='g4')
	for k in KB_clauses:
		s.add_clause(k)

	for k in seed:
		s.add_clause(k)

	if s.solve():
		return True
	else:
		return False



def get_HS(KB_clauses, clauses_dict):
	# Compute minimal hitting set

	h = Hitman(solver='m22', htype='lbx')
	# Add sets to hit
	for c in KB_clauses:
		h.hit(c)
	while True:
		mhs = h.get()
		if mhs == None:
			return []
		else:
			mhs = [h.get()]
			clauses = get_clauses_from_index(mhs, clauses_dict)
			if sat(clauses, []):
				return [h.get()]
			else:
				h.block(mhs[0])



def get_MUS(KB, e, q):
	# Compute minimal unsatisfiable set
	wcnf2 = WCNF()
	for k in e:
		if any(isinstance(el, list) for el in k):
			for ks in k:
				wcnf2.append(ks, weight=1)
		else:
			wcnf2.append(k, weight=1)

	if KB:
		for c in KB.clauses:
			wcnf2.append(c, weight=1)
	wcnf2.extend((q.negate().clauses))
	mmusx = MUSX(wcnf2, verbosity=0)
	mus = mmusx.compute()
	return [list(wcnf2.soft[m - 1]) for m in mus]



def get_MCS(KBa_s, KBa_h, q, seed, clauses_dict):
	# Compute minimal hitting set
	wcnf = WCNF()
	for c in KBa_s:
		if c not in seed:	# don't add to the soft clauses those in the seed
			wcnf.append(c, weight=1)
	for c in KBa_h:
		wcnf.append(c)

	for c in seed: # add clauses in the seed as hard
		if any(isinstance(el, list) for el in c):
			for cs in c:
				wcnf.append(cs)
		else:
			wcnf.append(c)

	wcnf.extend(q.negate().clauses)

	lbx = LBX(wcnf, use_cld=True, solver_name='g3')

	# Compute mcs and return the clauses indexes
	mcs = lbx.compute()
	# Current mcs is computed w.r.t. the soft clauses excluding the seed. Below we find the corresponding indexes of these clauses in KBa_s
	temp_cl_lookup = create_clauses_lookup(wcnf.soft)
	clauses = get_clauses_from_index(mcs, temp_cl_lookup)
	mcs = get_index_from_clauses(clauses, clauses_dict)

	return mcs



def create_clauses_lookup(clasues):
	Dict = defaultdict()
	for i, k in enumerate(clasues):
		Dict[i + 1] = k
	return Dict


def get_clauses_from_index(seed, clauses_dict):
	cls = []
	if seed:
		# seed = [item for sublist in seed for item in sublist]
		for s in seed:
			# print(s,'la')
			# print(clauses_dict[s])
			cls.append(clauses_dict[s])
	return cls



def get_index_from_clauses(seed, clauses_dict):
	idx = []
	for s in seed:
		for key, val in clauses_dict.items():
			if val == s:
				idx.append(key)
	return idx


def negate_clause(clause):
	neg_cl = []
	if any(isinstance(el, list) for el in clause):
		clause = [item for sublist in clause for item in sublist]
		neg_cl.append([-c for c in clause])
	else:
		for c in clause:
			neg_cl.append([-c])
	return neg_cl


def correct_KB(KB1, KB2):
	Diff = [list(x) for x in set(map(tuple, KB1.clauses)).difference(set(map(tuple, KB2.clauses)))]
	KB2_s = [list(x) for x in set(map(tuple, KB2.clauses)).difference(set(map(tuple, KB1.clauses)))]
	KB2_h = [list(x) for x in set(map(tuple, KB2.clauses)).intersection(set(map(tuple, KB1.clauses)))]

	wcnf = WCNF()
	for c in KB2_s:
		wcnf.append(c, weight=1)
	for c in KB2_h:
		wcnf.append(c)
	for c in Diff:
		wcnf.append(c)

	lbx = LBX(wcnf, use_cld=True, solver_name='g3')

	# Compute mcs and return the clauses indexes
	mcs = lbx.compute()
	temp_cl_lookup = create_clauses_lookup(wcnf.soft)
	clauses = get_clauses_from_index(mcs, temp_cl_lookup)
	return clauses
