from collections import defaultdict


class Graph:
    """
    Represents an undirected graph with weighted edges.

    Attributes:
        adjacency_list: A defaultdict containing vertices as keys and dictionaries of neighbors and their costs as values.
        vertices: A set containing all vertices in the graph.
    """

    def __init__(self):
        """
        Initializes an empty graph.
        """
        self.adjacency_list = defaultdict(dict)
        self.vertices = set()
    
    def reset(self):
        self.adjacency_list = defaultdict(dict)
        self.vertices = set()

    def add_edge(self, vertex1, vertex2, cost1, cost2):
        """
        Adds an edge to the graph.

        Parameters:
        - vertex1: The first vertex of the edge.
        - vertex2: The second vertex of the edge.
        - cost1: The cost associated with the edge from vertex1 to vertex2.
        - cost2: The cost associated with the edge from vertex2 to vertex1.
        """
        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1][vertex2] = []
            
        self.adjacency_list[vertex1][vertex2].append((cost1, cost2))
        self.vertices.update([vertex1, vertex2])

    def read_from_file(self, file_path):
        """
        Reads graph data from a file and updates the graph.

        Parameters:
        - file_path: The path to the file containing graph data in the format: vertex1 vertex2 cost1 cost2
        """
        self.adjacency_list = defaultdict(defaultdict(list))
        self.vertices = set()
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    vertex1, vertex2, cost1, cost2 = map(int, line.split())
                    self.add_edge(vertex1, vertex2, cost1, cost2)
        except FileNotFoundError:
            print(f"File {file_path} not found.")

    def print_graph(self):
        """
        Prints the graph in the format: V1 -> V2 : C1, C2
        """
        print("  V1 -> V2  :  C1, C2")
        for vertex, edges in self.adjacency_list.items():
            for neighbor, costs in edges.items():
                for cost in costs:
                    print(f"{vertex:>4} -> {neighbor:<4}: {cost[0]:>3}, {cost[1]}")

    def get_neighbors(self, vertex):
        """
        Gets the neighbors (vertex_id, costs) of a given vertex.

        Parameters:
        - state: The vertex for which neighbors are requested.

        Returns:
        - list: A list of tuples containing neighbors and their costs.
        """
        if vertex in self.adjacency_list:
            return list(self.adjacency_list[vertex].items())
        return []

    @property
    def graph(self):
        """
        Gets the adjacency list representation of the graph.

        Returns:
        - dict: The adjacency list of the graph.
        """
        return self.adjacency_list