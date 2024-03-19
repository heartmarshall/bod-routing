from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class Solution(ABC):
    """
    Abstract base class for solutions in multi-objective optimization.

    Parameters:
    - solution_values (list): List of objective values.

    Returns:
    - None
    """
    @abstractmethod
    def __init__(self, solution_values):
        pass

    @abstractmethod
    def dominates(self, other):
        """
        Check if this solution dominates another.

        Parameters:
        - other (BiObjSolution): Another bi-objective solution.

        Returns:
        - bool: True if this solution dominates the other, False otherwise.
        """
        pass

class BiObjSolution(Solution):
    """
    Class representing a bi-objective solution.
    """
    def __init__(self, solution_values):
        """
        Initialize a bi-objective solution with the given values.

        Parameters:
        - solution_values (list): List of objective values.
        """
        self.solution_values = tuple(solution_values)
        self.g1 = solution_values[0]
        self.g2 = solution_values[1]

    def dominates(self, other: 'BiObjSolution'):
        """
        Check if this solution dominates another.

        Parameters:
        - other (BiObjSolution): Another bi-objective solution.

        Returns:
        - bool: True if this solution dominates the other, False otherwise.
        """
        return (self.g1 < other.g1 and self.g2 <= other.g2) or (self.g1 <= other.g1 and self.g2 < other.g2)
    
    def is_dominated_by(self, other: 'BiObjSolution'):
        return not self.dominates(other)

    def __str__(self):
        return f"({self.g1}, {self.g2})"

    def __hash__(self) -> int:
        return hash((self.g1, self.g2))

    def __repr__(self) -> str:
        return f"BiObjSolution([{self.g1}, {self.g2}])"

    def __eq__(self, other: 'BiObjSolution') -> bool:
        return isinstance(other, BiObjSolution) and self.g1 == other.g1 and self.g2 == other.g2


class ParetoSet:
    """
    Class representing a Pareto set in multi-objective optimization.
    """
    def __init__(self, SolutionClass=BiObjSolution):
        """
        Initialize a Pareto set.

        Parameters:
        - SolutionClass (class): Class representing the type of solutions in the Pareto set.
        """
        self.solutions = set()
        self.SolutionClass = SolutionClass

        #Для визуализации
        self.max_y = 0
        self.max_x = 0
        self.all_solusions_ever = set()


    def add_solution(self, solution_values):
        """
        Add a solution to the Pareto set.

        Parameters:
        - solution_values (list): List of objective values for the new solution.
        """
        solution = self.SolutionClass(solution_values)
        non_dominated = self._is_non_dominated(solution)

        #Для визуализации
        self.all_solusions_ever.add(solution)
        self.max_x= max(self.max_x, solution.solution_values[0])
        self.max_y = max(self.max_y, solution.solution_values[1])

        if non_dominated:
            
            self.solutions = {s for s in self.solutions if not solution.dominates(s)}
            self.solutions.add(solution)

    def remove_solution(self, solution_values):
        """
        Remove a solution from the Pareto set.

        Parameters:
        - solution (BiObjSolution): The solution to be removed.
        """
        solution = self.SolutionClass(solution_values)
        self.solutions.remove(solution)

    def _is_non_dominated(self, solution):
        """
        Check if a solution is non-dominated by the current solutions in the set.

        Parameters:
        - solution (BiObjSolution): The solution to check.

        Returns:
        - bool: True if the solution is non-dominated, False otherwise.
        """
        return not any(s.dominates(solution) for s in self.solutions)

    def is_non_dominated(self, solution_values):
        """
        Check if a solution with given objective values is non-dominated by the current solutions in the set.

        Parameters:
        - solution_values (list): List of objective values for the solution.

        Returns:
        - bool: True if the solution is non-dominated, False otherwise.
        """
        solution = self.SolutionClass(solution_values)
        return not any(s.dominates(solution) for s in self.solutions)

    def get_solutions(self,values=True):
        """
        Get the current solutions in the Pareto set.

        Parameters:
        - values (bool): If True, return a set of solution values. If False, return a set of solution objects.
        Default is True.

        Returns:
        - set: Set of solutions in the Pareto set. If values is True, it contains tuples of solution values.
        If values is False, it contains solution objects.
        """
        if values:
            return {s.solution_values for s in self.solutions}
        return self.solutions

    def solutions_dominated_by(self, solution_values):
        """
        Get solutions in the Pareto set that are dominated by a given solution.

        Parameters:
        - solution_values (list): List of objective values for the dominating solution.

        Returns:
        - list: List of solutions dominated by the given solution.
        """
        solution = self.SolutionClass(solution_values)
        return [s for s in self.solutions if solution.dominates(s)]

    def _solutions_dominated_by(self, solution):
        """
        Get solutions in the Pareto set that are dominated by a given solution.

        Parameters:
        - solution (BiObjSolution): The dominating solution.

        Returns:
        - list: List of solutions dominated by the given solution.
        """
        return [s for s in self.solutions if solution.dominates(s)]

    def remove_worse(self, better_solution_values):
        """
        Remove solutions from the Pareto set that are dominated by a better solution.

        Parameters:
        - better_solution_values (list): List of objective values for the better solution.
        """
        better_solution = self.SolutionClass(better_solution_values)
        self.solutions.difference_update(self._solutions_dominated_by(better_solution))

    def visualize(self, color='blue', marker='o'):
        """
        Visualize the current Pareto set.

        Parameters:
        - color (str): Color of the scatter plot (default is 'blue').
        - marker (str): Marker style for the scatter plot (default is 'o').
        """
        if not self.solutions:
            print("Empty Pareto set. Nothing to visualize.")
            return
        x_values, y_values = zip(*[(sol.g1, sol.g2) for sol in self.solutions])
        plt.scatter(x_values, y_values, label='Pareto Set', color=color, marker=marker, s=100, edgecolors='black')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.title('Pareto Set Visualization')
        plt.grid(True, linestyle='--', which='both', alpha=0.7)
        plt.show()

    def __str__(self) -> str:
        return f"({', '.join(str(sol) for sol in self.solutions)})"

    def __contains__(self, solution_values):
        """
        Check if a solution with given objective values is in the Pareto set.

        Parameters:
        - solution_values (list): List of objective values for the solution.

        Returns:
        - bool: True if the solution is in the Pareto set, False otherwise.
        """
        solution = self.SolutionClass(solution_values)
        return solution in self.solutions
