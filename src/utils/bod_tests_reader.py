from .graph import Graph

def read_graph_from_file(graph_file_path):
    with open(graph_file_path, "r") as f:
        nodes_count, edges_count = map(int, f.readline().split())
        graph = Graph()
        for _ in range(edges_count):
            n1, n2, c1, c2 = map(int, f.readline().split())
            graph.add_edge(n1, n2, c1, c2)
    return Graph