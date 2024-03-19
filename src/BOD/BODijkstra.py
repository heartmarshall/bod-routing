from utils.graph import Graph
from utils.pareto_set import ParetoSet
from utils.search_tree_pqd import SearchTreePQD, Node
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

def BODijkstra(search_graph: Graph, start_state, search_tree=SearchTreePQD):
    """
    Bi-objective Dijkstra algorithm to find Pareto-optimal paths.

    Parameters:
        search_graph (Graph): The graph to search.
        start_state: The starting state.
        search_tree (type): The type of search tree to use.

    Returns:
        tuple: Pareto-optimal solutions, all paths, and discarded paths.
    """
    solutions = defaultdict(ParetoSet)
    g2_min = defaultdict(lambda: float('inf'))
    start_node = Node(state=start_state, g_values=(0, 0), parent=None)
    search_tree = search_tree()
    search_tree.add_to_open(start_node)

    # For visualization
    discarded_paths = defaultdict(list)  # Vertex: all paths rejected at this vertex
    all_paths = defaultdict(list)  # Vertex: all paths that ever entered the solution and lead to it

    while not search_tree.open_is_empty():
        x = search_tree.get_best_node_from_open()  # Retrieve nodes in lexicographical order
        if x.g2 >= g2_min[x.state]:
            discarded_paths[x.state].append(construct_path(x))
            continue

        g2_min[x.state] = x.g2
        solutions[x.state].add_solution(x.g_values)
        all_paths[x.state].append(construct_path(x))

        for state, costs in search_graph.get_neighbors(x.state):
            neighbour_g = tuple(x + y for x, y in zip(x.g_values, costs))
            y = Node(state, g_values=neighbour_g, parent=x)
            if y.g2 >= g2_min[state]:
                discarded_paths[state].append(construct_path(y))
                continue
            search_tree.add_to_open(y)

    return solutions, all_paths, discarded_paths
