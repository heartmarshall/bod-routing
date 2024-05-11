import pytest
from bi_obj_dijkstra.dijkstra import dijkstra
from bi_obj_dijkstra.graph import Graph

@pytest.fixture
def cycle_graph():
    test_graph = Graph()
    test_graph.add_edge(1, 2, 1, 1)
    test_graph.add_edge(1, 4, 6, 6)
    test_graph.add_edge(2, 3, 1, 8)
    test_graph.add_edge(2, 1, 5, 1)
    test_graph.add_edge(3, 1, 1, 5)
    test_graph.add_edge(4, 3, 1, 1)
    return test_graph

@pytest.fixture
def graph():
    test_graph = Graph()
    test_graph.add_edge(0, 2, 1, 5)
    test_graph.add_edge(0, 4, 5, 1)
    test_graph.add_edge(2, 3, 1, 4)
    test_graph.add_edge(2, 5, 1, 2)
    test_graph.add_edge(2, 5, 2, 1)
    test_graph.add_edge(4, 3, 1, 3)
    test_graph.add_edge(3, 1, 9, 3)
    test_graph.add_edge(4, 1, 2, 1)
    test_graph.add_edge(5, 1, 1, 1)
    print(test_graph.print_graph())
    return test_graph

def test_dijkstra_base_case(graph):
    start_state = 0
    solutions = dijkstra(graph, start_state)
    assert len(solutions) == 6
    assert solutions[2].get_solutions() == {(1, 5)}

def test_dijkstra_alternative_paths(graph):
    # Проверяем случай с альтернативными путями
    start_state = 0
    solutions = dijkstra(graph, start_state)
    assert len(solutions) == 6
    assert solutions[1].get_solutions() == {(3, 8), (4, 7), (7, 2)}

def test_dijkstra_no_paths(graph):
    # Проверяем случай отсутствия путей
    start_state = 1
    solutions = dijkstra(graph, start_state)
    assert len(solutions) == 1 # Само решение

def test_dijkstra_cycle_graph(cycle_graph):
    start_state = 1
    solutions = dijkstra(cycle_graph, start_state)
    assert len(solutions) == 4
    assert solutions[3].get_solutions() == {(2, 9), (7, 7)}