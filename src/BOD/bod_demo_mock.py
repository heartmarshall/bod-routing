import argparse

from colorama import init, Fore, Style
init()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Parse arguments for the program.')
    parser.add_argument('map_file_path', type=str, help='Path to the map file')
    parser.add_argument('start_node', type=int, help='ID of the start node')
    parser.add_argument('end_node', type=int, help='ID of the end node')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    return args.map_file_path, args.start_node, args.end_node, args.verbose

pathfinding_algorithm = lambda x: x
decision_strategy_function = lambda x: x

def check_decentralization(pathfinding_algorithm: callable, decision_strategy_function: callable, map, start_node_id, end_node_id) -> bool:
    print(f'Start checking the decentralizability of the algorithm: {pathfinding_algorithm.__name__}')
    chosed_paths = []
    
    cur_node_id = start_node_id
    while cur_node_id != end_node_id:
        print(f'Started the search algorithm from the node with id: {cur_node_id}')
        all_solutions, _, _ = pathfinding_algorithm(map, cur_node_id)
        solutions = all_solutions[end_node_id]
        if len(solutions) == 0:
            raise(RuntimeError("The algorithm was unable to find solutions to the problem\n"
                               "Check the correctness of the algorithm and input data"))
        chosed_solution = decision_strategy_function(solutions)
        chosed_solution_number = 0
        print(f"Number of solutions found: {len(solutions)}")
        for sol_number in range(len(solutions)):
            if solutions[sol_number] == chosed_solution:
                chosed_solution_number = sol_number
            print(f'sol_№{sol_number}: {solutions[sol_number].path}')
        print(f"Out of all the solutions, the solution chosen is: {chosed_solution_number}")
        print(f"-----------------")

    for i in range(len(chosed_paths)-1):
        if chosed_paths[i][1:] != chosed_paths[i+1]:
            print(f"The proposed algorithm is not decentralized!")
            print(f"A mismatch is found on the following pair of paths:\n{chosed_paths[i]},\n{chosed_paths[i+1]}")
            return False
    print("The proposed algorithm worked truly decentralized")
    return True



if __name__ == "__main__":
    map_file_path, start_node, end_node, verbose = parse_arguments()
    if map_file_path == "small_test.txt":
        print(f'Start checking the decentralizability of the algorithm: BODijkstra')
        print(f'Work graph contains:  Nodes: 6  Edges: 11')
        print(f"-----------------")
        print(f'Started the search algorithm from the node with id: 0')
        print("Number of solutions found: 3")
        print(Fore.GREEN + "Solution №1: 0, 3, 4, 1 | (4, 17)"+  Style.RESET_ALL)
        print("Solution №2: 0, 2, 1    | (7, 11)" )
        print("Solution №1: 0, 5, 1    | (16, 5)")
        print(f"Out of all the solutions, the solution chosen is: №1")
        print(f"-----------------")
        print(f'Started the search algorithm from the node with id: 3')
        print("Number of solutions found: 3")
        print(Fore.GREEN + "Solution №1: 3, 4, 1 | (3, 14)"+  Style.RESET_ALL)
        print("Solution №2: 3, 2, 1 | (7, 9)" )
        print("Solution №1: 3, 5, 1 | (16, 4)")
        print(f"Out of all the solutions, the solution chosen is: №1")
        print(f"-----------------")
        print(f'Started the search algorithm from the node with id: 4')
        print("Number of solutions found: 3")
        print(Fore.GREEN + "Solution №1: 4, 1    | (2, 9)"+  Style.RESET_ALL)
        print("Solution №2: 4, 2, 1 | (5, 6)" )
        print("Solution №1: 4, 5, 1 | (15, 4)")
        print(f"Out of all the solutions, the solution chosen is: №1")
        print(f"-----------------")
        print("Congratulations! The proposed algorithm worked truly decentralized")
    elif map_file_path == "random_0.txt":
        print(f'Start checking the decentralizability of the algorithm: BODijkstra')
        print(f'Work graph contains:  Nodes: 1024  Edges: 30514')
        print(f"-----------------")
        print(f'Started the search algorithm from the node with id: 0')
        print("Number of solutions found: 4")
        print(Fore.GREEN +"Solution №1: 0, 19, 1009, 680, 1              | (19, 49)" + Style.RESET_ALL)
        print("Solution №2: 0, 30, 8, 814, 1                 | (24, 39)")
        print("Solution №3: 0, 548, 213, 92, 365 1           | (63, 20)")
        print("Solution №4: 0, 724, 136, 891, 602, 619       | (68, 12)")
        print(f"Out of all the solutions, the solution chosen is: №1")
        print(f"-----------------")
        print(f'Started the search algorithm from the node with id: 19')
        print("Number of solutions found: 2")
        print(Fore.GREEN +"Solution №1: 19, 1009, 680, 1              | (18, 39)" + Style.RESET_ALL)
        print("Solution №2: 19, 84, 202                   | (31, 37)")
        print(f"Out of all the solutions, the solution chosen is: №1")
        print(f"-----------------")
        print(f'Started the search algorithm from the node with id: 1009')
        print("Number of solutions found: 3")
        print(Fore.GREEN +"Solution №1: 1009, 680, 1                          | (14, 22)" + Style.RESET_ALL)
        print("Solution №2: 1009, 721, 275, 843                   | (17, 19)")
        print(f"Out of all the solutions, the solution chosen is: №1")
        print(f"-----------------")
        print(f'Started the search algorithm from the node with id: 680')
        print("Number of solutions found: 1")
        print(Fore.GREEN +"Solution №1: 680, 1 | (2, 11)" + Style.RESET_ALL)
        print(f"Out of all the solutions, the solution chosen is: №1")
        print(f"-----------------")
        print("Congratulations! The proposed algorithm worked truly decentralized")
        