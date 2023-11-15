from pysat.formula import CNF
from .util import *



def model_reconciliation(KB1, KB2, q):
	KBa_h = [list(x) for x in set(map(tuple, KB1.clauses)).intersection(set(map(tuple, KB2.clauses)))] # Hard clauses
	KBa_s = [list(x) for x in set(map(tuple, KB1.clauses)).difference(set(map(tuple, KBa_h)))] # Soft clauses
	R = Hitman(solver='m22', htype='maxsat') # Reconciliation formula
	clauses_lookup = create_clauses_lookup(KBa_s) # create lookup dictionary initialized with KBa_s

	# Restore inconsistency if KB_h \cup (KB_a \KB_h) is unsat:
	search_space = [list(x) for x in set(map(tuple, KB1.clauses)).difference(set(map(tuple, KB2.clauses)))]
	if not sat(KB2, search_space):
		to_delete = correct_KB(KB1, KB2)
		KB2 = [k for k in KB2.clauses if k not in to_delete]
	while True:
		seed = R.get() # compute mhs on R
		e_p = get_clauses_from_index(seed, clauses_lookup)  # get clauses according to index
		if skeptical_entailment(KB2, e_p, q):
			mus = get_MUS(KB2, e_p, q)
			return [m for m in mus if m not in KB2 and m not in q.negate().clauses ]
		else:
			C = get_MCS(KBa_s, KB2, q, e_p, clauses_lookup)
			R.hit(list(C))



def main():
	KB1, KB2 = CNF(), CNF()
	query = CNF()

	def test1():
		KB1.extend([[1,2], [-2,3],[-3],[-2,4],[-4]])
		KB2.extend([[-2], [-3]])
		query.append([1])

	def test2():
		KB1.extend([[-1,2], [-2,3], [-3,4], [-2,-4,5], [1]])
		KB2.extend([[-1,2], [-3,4]])
		query.append([5])

	def test3():
		KB1.extend([[1],[-2],[10],[-4], [-8,1], [-6,2], [-8,3], [2,-3,8], [-6,5],[4,-5,6],[-8,-6],[-7,10],[3,-11,9],[5,-10,7],[-9,-7]])
		KB2.extend([[1],[-2],[10],[-4],[-8,1],[-8,3], [2,-3,8]])
		query.extend([[-4], [-5]])


	# test3()
	# print(model_reconciliation(KB1, KB2, query))


# main()
