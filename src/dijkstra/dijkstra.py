from graph import Graph
from dijkstra.pareto_set import ParetoSet
from dijkstra.search_tree_pqd import SearchTreePQD, Node
from collections import defaultdict

def construct_path(node: Node):
    """
    Construct a path from the given node to the root.

    Parameters:
        node (Node): The current node.

    Returns:
        list: A list of states representing the path.
    """
    path = [node]
    path_ids = [node.state]
    prev_node = node.parent
    while prev_node is not None:
        path.append(prev_node)
        path_ids.append(prev_node.state)
        prev_node = prev_node.parent
    return path_ids

def dijkstra(search_graph: Graph, start_state, search_tree=SearchTreePQD):
    """
    Bi-objective Dijkstra algorithm to find Pareto-optimal solutions for each state.

    Parameters:
        search_graph (Graph): The graph to search.
        start_state: The starting state.
        search_tree (type): The type of search tree to use.

    Returns:
        tuple: Pareto-optimal solutions: {state_id:solution}
    """
    solutions = defaultdict(ParetoSet)
    g2_min = defaultdict(lambda: float('inf'))
    start_node = Node(state=start_state, g_values=(0, 0), parent=None)
    search_tree = search_tree()
    search_tree.add_to_open(start_node)

    while not search_tree.open_is_empty():
        cur_node = search_tree.get_best_node_from_open()  # Retrieve nodes in lexicographical order
        if cur_node.g2 >= g2_min[cur_node.state]:
            continue

        g2_min[cur_node.state] = cur_node.g2
        solutions[cur_node.state].add_solution(cur_node.g_values)

        for state, costs in search_graph.get_neighbors(cur_node.state):
            neighbour_g = tuple(x_g + y_g for x_g, y_g in zip(cur_node.g_values, costs))
            y = Node(state, g_values=neighbour_g, parent=cur_node)
            if y.g2 >= g2_min[state]:
                continue
            search_tree.add_to_open(y)

    return solutions
