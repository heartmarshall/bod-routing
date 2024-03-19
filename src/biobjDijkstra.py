import matplotlib.pyplot as plt
from utils.graph import Graph
from utils.pareto_set import ParetoSet
from utils.pareto_set import BiObjSolution as sol
from ipywidgets import interact, widgets
from utils.search_tree_pqd import SearchTreePQD, Node
from collections import defaultdict
from heapq import heapify, heappop, heappush
from typing import Optional
from graph_visualization import visualize_graph


from utils.pareto_set import Solution


class BiObjSolution(Solution):
    def __init__(self, solution_values):
        self.solution_values = solution_values
        self.g1 = solution_values[0]
        self.g2 = solution_values[1]

    def is_dominated_by(self, other: 'BiObjSolution'):
        return not self.is_dominates(other)
    
    def is_dominates(self, other: 'BiObjSolution'):
        return (self.g1 < other.g1 and self.g2 <= other.g2) or (self.g1 <= other.g1 and self.g2 < other.g2)
    
    def __str__(self):
        return f"({self.g1}, {self.g2})"
    
    def __hash__(self) -> int:
        return hash((self.g1, self.g2))
    
    def __repr__(self) -> str:
        return f"BiObjSolution([{self.g1}, {self.g2}])"
    
    def __eq__(self, another_solution) -> bool:
        return self.g1 == another_solution.g1 and self.g2 == another_solution.g2
    



class ParetoSet:
    def __init__(self, SolutionClass=BiObjSolution):
        self.history = []
        self.solutions = set()
        self.SolutionClass = SolutionClass

        #Для визуализации
        self.max_y = 0
        self.max_x = 0
        self.all_solusions_ever = set()

    def add_solution(self, solution_values):
        solution = self.SolutionClass(solution_values)
        #Для визуализации
        self.all_solusions_ever.add(solution)

        # Проверяем, является ли новое решение недоминируемым
        self.max_x= max(self.max_x, solution.solution_values[0])
        self.max_y = max(self.max_y, solution.solution_values[1])
        non_dominated = self._is_non_dominated(solution)

        if non_dominated:
            
            # Удаляем решения, которые становятся доминированными
            self.history.append(self.solutions)
            self.solutions = set([s for s in self.solutions if not solution.is_dominates(s)])
            self.solutions.add(solution)
            return

    def del_solution(self, solution_values):
        solution = self.SolutionClass(solution_values)
        self.solutions.remove(solution)

    def _is_non_dominated(self, solution):
        """
        Проверяет, является ли solution недоминируемым по отношению к текущим решениям в множестве
        """
        for s in self.solutions:
            if s.is_dominates(solution):
                return False
        return True

    def is_non_dominated(self, solution_values):
        """
        Проверяет, является ли solution недоминируемым по отношению к текущим решениям в множестве
        """
        solution = self.SolutionClass(solution_values)
        for s in self.solutions:
            if s.is_dominates(solution):
                return False
        return True

    def get_solutions(self):
        return self.solutions
    
    def all_solutions_dominated_by(self, solution_values):
        solution = self.SolutionClass(solution_values)
        return [s for s in self.solutions if solution.is_dominates(s)]
    
    def _all_solutions_dominated_by(self, solution):
        return [s for s in self.solutions if solution.is_dominates(s)]
    
    def remove_worse(self, better_solution_values):
        """
        Удаляет из парето-множества все решения, которые доминируются better_solution
        """
        better_solution = self.SolutionClass(better_solution_values)
        for s in self._all_solutions_dominated_by(better_solution):
            self.solutions.remove(s)
    
    def visualize(self):
        solutions = self.get_solutions()
        if not solutions:
            print("Пустое Парето-множество. Нечего визуализировать.")
            return
        # Разделяем координаты решений
        x_values, y_values = [], []
        for solution in self.solutions:
            x_values.append(solution.g1)
            y_values.append(solution.g2)
            
        # Визуализация точек в Парето-множестве
        plt.scatter(x_values, y_values, label='Pareto Set', color='blue', marker='o', s=100, edgecolors='black')
        # Настройка графика
        plt.xlabel('Критерий 1')
        plt.ylabel('Критерий 2')
        plt.title('Визуализация Парето-множества')
        # Включаем грид только для местоположений точек
        plt.grid(True, linestyle='--', which='both', alpha=0.7)
        # Показываем график
        plt.show()

    def __str__(self) -> str:
        return f"({', '.join((str(sol) for sol in self.solutions))})"
    
    def __contains__(self, solution_values):
        solution = self.SolutionClass(solution_values)
        return solution in self.solutions





class Node:
    def __init__(self, state, g=[0, 0], h=[0, 0], parent=None, s=None):
        self.state = state
        self.g = tuple(g)
        self.h = tuple(h)
        self.f = tuple(x + y for x, y in zip(g, h))
        self.parent = parent
        self.s = s
        self.g2 = self.g[1]
        
    def __eq__(self, other: 'Node'):
        # Т.к у нас multi-objective вариант, то у одного и того-же стейта могут быть разные g значения. Поэтому нужно проверять и по ним
        if self.state == other.state and \
           self.g == other.g and \
           self.h == other.h:
            return True
        return False

    def __hash__(self) -> int:
        return hash((self.state, self.g, self.h))

    def __lt__(self, other: 'Node'):
        # Это проверка именно на f значения, не на доминантность!
        return self.f < other.f
    
    def is_dominates(self, other: 'Node'):
        return (self.f < other.f and self.f <= other.f) or (self.f <= other.f and self.f < other.f)
    
    def __str__(self) -> str:
        return f"{self.state, self.g}"


class SearchTreePQD:

    def __init__(self):
        self._open = []
        self._closed = {}
        self._enc_open_dublicates = 0

    def __len__(self) -> int:
        return len(self._open) + len(self._closed)

    def open_is_empty(self) -> bool:
        return not self._open

    def add_to_open(self, item: Node):
        heappush(
            self._open, item
        )

    def get_best_node_from_open(self) -> Optional[Node]:
        while self._open:
            best_node = heappop(self._open)
            if not self.was_expanded(best_node):
                return best_node
        return None
    
    def remove_worse_nodes(self, better_node: 'Node'):
        """
        Убирает из дерева поиска все ноды, которые доминируются other (по значению f)
        """
        self._open = [node for node in self._open if not better_node.is_dominates(node)] 
        heapify(self._open)

    def remove_worse_opened(self, state, better_f):
        """
        Очищает opened от всех state, у которых f-значение доминируется f-значением у better_node
        """
        better_node = Node(state, better_f)
        new_open = []
        for node in self._open:
            if node.state != better_node.state:
                new_open.append(node)
                continue
            else:
                if not not better_node.is_dominates(node):
                    new_open.append(node)
        self._open =  new_open
        heapify(self._open)
        
    def add_to_closed(self, item: Node):
        self._closed[item] = item

    def was_expanded(self, item: Node) -> bool:
        return item in self._closed

    @property
    def opened(self):
        return self._open

    @property
    def expanded(self):
        return self._closed.values()

    @property
    def number_of_open_dublicates(self):
        return self._enc_open_dublicates
    

def construct_path(node: Node):
    path = [node]
    path_ids = [node.state]
    prev_node = node.parent
    while prev_node is not None:
        path.append(prev_node)
        path_ids.append(prev_node.state)
        prev_node = prev_node.parent
    return path_ids

def BDijkstra(search_graph: Graph,  start_state, search_tree=SearchTreePQD,):
    sols = defaultdict(ParetoSet)
    g2_min = defaultdict(lambda: float('inf'))
    start_node = Node(state=start_state, g=(0, 0), parent=None, s=start_state)
    discarded_paths = defaultdict(list)
    good_paths = defaultdict(list)
    search_tree = SearchTreePQD()
    search_tree.add_to_open(start_node)

    while not search_tree.open_is_empty():
        x = search_tree.get_best_node_from_open()
        if x.g2 >= g2_min[x.state]:
            discarded_paths[x.state].append(construct_path(x))
            continue
        
        g2_min[x.state] = x.g2
        sols[x.state].add_solution(x.g)
        good_paths[x.state].append(construct_path(x))

        for state, costs in search_graph.get_neighbors(x.state):
            neighbour_g = tuple(x + y for x, y in zip(x.g, costs))
            y = Node(state, g=neighbour_g, parent=x)
            if y.g2 >= g2_min[state]:
                discarded_paths[state].append(construct_path(y))
                continue
            search_tree.add_to_open(y)

    return sols, good_paths, discarded_paths

