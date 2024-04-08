import pytest
from dijkstra.pareto_set import BiObjSolution, ParetoSet

@pytest.fixture
def pareto_set():
    return ParetoSet()

def test_bi_obj_solution():
    solution1 = BiObjSolution([6, 3])
    solution2 = BiObjSolution([4, 2])

    assert solution1.dominates(solution2) is False
    assert solution2.dominates(solution1) is True
    assert solution1.is_dominated_by(solution2) is True
    assert solution2.is_dominated_by(solution1) is False
    assert solution1 != solution2

def test_pareto_set_add_solution(pareto_set):
    pareto_set.add_solution([1, 2])
    pareto_set.add_solution([3, 4])
    pareto_set.add_solution([2, 3])
    pareto_set.add_solution([5, 1])

    solutions = pareto_set.get_solutions()
    assert len(solutions) == 2

def test_pareto_set_remove_solution(pareto_set):
    solution1 = (1, 4)
    solution2 = (3, 2)
    pareto_set.add_solution(solution1)
    pareto_set.add_solution(solution2)
    pareto_set.remove_solution(solution1)

    solutions = pareto_set.get_solutions()
    assert solution1 not in solutions
    assert solution2 in solutions

def test_pareto_set_contains(pareto_set):
    solution1 = [1, 7]
    solution2 = [2, 5]

    pareto_set.add_solution(solution1)
    pareto_set.add_solution(solution2)

    assert solution1 in pareto_set
    assert solution2 in pareto_set
    assert [5, 6] not in pareto_set

def test_pareto_set_remove_non_existent(pareto_set):
    solution = [1, 1]
    with pytest.raises(KeyError):
        pareto_set.remove_solution(solution)
