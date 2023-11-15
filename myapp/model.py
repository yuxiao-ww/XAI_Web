import os
from .util import *
from unified_planning.shortcuts import *
from unified_planning.io.pddl_reader import PDDLReader
from unified_planning.engines import CompilationKind
from .planning_utils.CNF_Encoder import Encoder
from . import main

# from MRP import *
from pysat.formula import CNF
from . import llmPlan
from . import llmExp


up.shortcuts.get_env().credits_stream = None


def CustomEncoder(userFile, userPlan):

    DOMAIN = '/Users/rachel/PycharmProjects/xaip1/llm-pddl-main/MRP/blocks/original_domain.pddl'
    # FILE = '/Users/rachel/PycharmProjects/xaip1/llm-pddl-main/MRP/blocks/prob1.pddl'
    FILE = userFile

    reader = PDDLReader()
    pddl_agent = reader.parse_problem(DOMAIN, FILE)

    with OneshotPlanner(name="pyperplan") as planner:
        result = planner.solve(pddl_agent)
        plan = result.plan
    with Compiler(problem_kind=pddl_agent.kind, compilation_kind=CompilationKind.GROUNDING) as grounder:
        grounding_result_agent = grounder.compile(pddl_agent, CompilationKind.GROUNDING)
        ground_problem_agent = grounding_result_agent.problem

    horizon = len(plan.actions)

    KBa, kba_vars = Encoder(ground_problem_agent, horizon).encode()
    solverPlan = KBa.get_plan()

    # 1. Solver generates a plan

    # 2. Why is this plan valid?
    # Why is this plan valid: 'unstack(A B)', 'putdown_A', 'pickup_B', 'stack_B_A'
    # unstack(A B), putdown_A, pickup_B, stack_B_A
    # pickup_B;stack_B_A;pickup_C;stack_C_B;
    # My plan is I first pick the block B up, then I stack the block B on the block A, and then I pick the block C up, in the end i stack the block C on the block B.

    # user = str(input())
    user = userPlan
    inputPlan = llmPlan.completion_func_gpt(user)['content'].split(', ')
    planQuery = [KBa.get_id_from_name(i) for i in inputPlan]
    planQuery2 = [KBa.get_id_from_name(i) for i in solverPlan]
    # print(solverPlan)
    print(inputPlan)

    # 3. First check if proposed plan is entailed by KB
    q = CNF(from_clauses=[[i] for i in planQuery])

    if skeptical_entailment(KBa.all_formulae(), [], q):
        # 4. If entailed, generate an explanation
        KB1 = CNF(from_clauses=KBa.all_formulae())
        KB2 = CNF()
        explanation = main.model_reconciliation(KB1, KB2, q, )
        # print(explanation)

        alltrans = []
        for e in explanation:
            trans = []
            for i in e:
                trans.append(KBa.get_name_from_id(abs(i)))
                # print(trans)
                alltrans.append(trans)
        alltrans = alltrans[::-1]
        # print(alltrans)
        explanation = llmExp.completion_func_gpt(str(alltrans))['content']
        # print(explanation)

    # If yes, then use above method to find explanation. If not, then use below method to find explanation.

    else:
        # 5. If not entailed, generate an explanation
        # Why not this plan?
        # Why not pick up B and stack B on A?
        # Why not this plan : 'pickup_B', 'stack_B_A'
        # I want to put the block A down, and pick the block B up, then I will stack the block B on the block A.
        altPlan = planQuery

        q = CNF(from_clauses=[[-i] for i in altPlan])

        KB1 = CNF(from_clauses=KBa.all_formulae())
        KB2 = CNF()

        explanation = main.model_reconciliation(KB1, KB2, q, )

        alltrans = []
        for e in explanation:
            trans = []
            for i in e:
                trans.append(KBa.get_name_from_id(abs(i)))
                alltrans.append(trans)
        alltrans = alltrans[::-1]
        # print(alltrans)
        explanation = llmExp.completion_func_gpt(str(alltrans))['content']
        # print(explanation)

    return explanation


# print(CustomEncoder())
