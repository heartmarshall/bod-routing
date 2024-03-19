from heapq import heapify, heappop, heappush
from typing import Optional


class Node:
    """
    Represents a node in the search tree.

    Attributes:
        state: The state represented by the node.
        g1, g2: Values of the cost function g from two sources.
        g_values: Tuple containing the g values.
        h1, h2: Values of the heuristic function h from two sources.
        h_values: Tuple containing the h values.
        f: Tuple containing the sum of g and h values from both sources.
        parent: The parent node in the search tree.
    """

    def __init__(self, state, g_values, h_values, parent=None):
        """
        Initializes a node in the search tree.

        Parameters:
        - state: The state represented by the node.
        - g_values: Tuple containing two values of the cost function g.
        - h_values: Tuple containing two values of the heuristic function h.
        - parent: The parent node in the search tree.
        """
        self.state = state
        self.g1, self.g2 = g_values
        self.g_values = g_values
        self.h1, self.h2 = h_values
        self.h_values = h_values
        self.f = (self.g1 + self.h1, self.g2 + self.h2)
        self.parent = parent
        
    def __eq__(self, other: 'Node'):
        """
        Checks if two nodes are equal.

        Parameters:
        - other (Node): The other node to compare.

        Returns:
        - bool: True if the nodes are equal, False otherwise.
        """
        return (
            self.state == other.state and
            self.g_values == other.g_values and
            self.h_values == other.h_values and
            self.parent == other.parent
        )

    def __hash__(self) -> int:
        """
        Returns the hash value of the node.

        Returns:
        - int: The hash value.
        """
        return hash((self.state, self.g_values, self.h_values, self.parent))

    def __lt__(self, other: 'Node'):
        """
        Compares two nodes based on their total cost values.

        Parameters:
        - other (Node): The other node to compare.

        Returns:
        - bool: True if the current node has a lower total cost than the other, False otherwise.
        """
        return self.f < other.f
    
    def is_dominates(self, other: 'Node'):
        """
        Checks if the current node dominates another node.

        Parameters:
        - other (Node): The other node to compare.

        Returns:
        - bool: True if the current node dominates the other, False otherwise.
        """
        return self.f <= other.f
    
    def __str__(self) -> str:
        """
        Returns a string representation of the node.

        Returns:
        - str: A string representation of the node.
        """
        return f"{self.state, self.f}"


class SearchTreePQD:
    """
    Represents a priority queue-based search tree.

    Attributes:
        _open: A list representing the open set in the search tree.
        _closed: A dictionary representing the closed set in the search tree.
    """

    def __init__(self):
        """
        Initializes an empty search tree.
        """
        self._open = []
        self._closed = {}

    def __len__(self) -> int:
        """
        Returns the total number of nodes in the search tree.

        Returns:
        - int: The total number of nodes.
        """
        return len(self._open) + len(self._closed)

    def open_is_empty(self) -> bool:
        """
        Checks if the open set is empty.

        Returns:
        - bool: True if the open set is empty, False otherwise.
        """
        return not self._open

    def add_to_open(self, item: Node):
        """
        Adds a node to the open set.

        Parameters:
        - item (Node): The node to be added.
        """
        heappush(self._open, item)

    def get_best_node_from_open(self) -> Optional[Node]:
        """
        Gets and removes the best node from the open set.

        Returns:
        - Node or None: The best node or None if the open set is empty.
        """
        while self._open:
            best_node = heappop(self._open)
            if not self.was_expanded(best_node):
                return best_node
        return None
    
    def remove_worse_nodes(self, better_node: 'Node'):
        """
        Removes nodes from the search tree that are dominated by the specified node.

        Parameters:
        - better_node (Node): The node dominating others.
        """
        self._open = [node for node in self._open if not better_node.is_dominates(node)] 
        heapify(self._open)

    def remove_worse_opened(self, state, better_f):
        """
        Clears the open set from nodes with states dominated by the specified state and f value.

        Parameters:
        - state: The state to compare.
        - better_f: The f value dominating other f values.
        """
        better_node = Node(state, better_f)
        new_open = [node for node in self._open if node.state != better_node.state or not better_node.is_dominates(node)]
        self._open = new_open
        heapify(self._open)
        
    def add_to_closed(self, item: Node):
        """
        Adds a node to the closed set.

        Parameters:
        - item (Node): The node to be added.
        """
        self._closed[item] = item

    def was_expanded(self, item: Node) -> bool:
        """
        Checks if a node has been expanded.

        Parameters:
        - item (Node): The node to check.

        Returns:
        - bool: True if the node has been expanded, False otherwise.
        """
        return item in self._closed

    @property
    def opened(self):
        """
        Gets the open set of the search tree.

        Returns:
        - list: The open set.
        """
        return self._open
