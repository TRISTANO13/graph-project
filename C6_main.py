import os
import numpy as np
from collections import defaultdict, deque

# Function to read constraints from a given file path
def read_constraints(file_path):
    with open(file_path, "r"):
        # Check if the file exists
        if not os.path.isfile(file_path):
            return "File not found"
        
        # Open and read lines from the file
        with open(file_path, "r") as file:
            lines = file.readlines()

        constraints = []
        # Process each line to extract task constraints
        for line in lines:
            parts = line.strip().split()
            # Ensure every task has at least one predecessor (even if it's '0')
            if len(parts) == 2:
                parts.append(0)
            constraints.append(tuple(map(int, parts)))

        return constraints
    
# Function to create an adjacency matrix from task constraints
def create_adjacency_matrix(constraints):
    num_tasks = len(constraints)
    matrix_size = num_tasks + 1
    # Initialize the matrix with '*'
    adjacency_matrix = np.full((matrix_size, matrix_size), '*', dtype='<U2')
    
    # Populate the matrix based on the constraints
    for task in constraints:
        task_num = task[0]
        task_duration = str(task[1])
        if len(task) > 2:
            for predecessor in task[2:]:
                adjacency_matrix[task_num][predecessor] = task_duration

    return adjacency_matrix

# Function to print the adjacency matrix
def print_adjacency_matrix(matrix):
    num_tasks = matrix.shape[0]
    print("      ", end="")
    # Print column headers
    print(f"{'α':1}", end="")
    for col in range(1, num_tasks - 1):
        print(f"{col:3}", end="")
    print(f"{'  ω':3}", end="")  
    print()
    
    # Print row of dashes for separation
    print("    ", end="")
    for col in range(num_tasks):
        print(f"---", end="")
    print()
    
    # Print the first row of the matrix
    print(f"{'  α':3}", end=" ")
    print(f"|", end=" ")
    for col in range(num_tasks):
        print(f"{matrix[0, col]:3}", end="")
    print()
    # Print the matrix rows
    for row in range(1, num_tasks - 1):
        print(f"{row:3}", end=" ") 
        print(f"|", end=" ")
        for col in range(num_tasks):
            print(f"{matrix[row, col]:3}", end="")
        print()
    # Print the last row of the matrix
    print(f"{'  ω':3}", end=" ")
    print(f"|", end=" ")    
    for col in range(num_tasks):
        print(f"{matrix[num_tasks - 1, col]:3}", end="")
    print()

# Function to create an alternative matrix representation
def create_matrix_alt(constraints):
    num_tasks = max(max(tasks) for tasks in constraints)
    matrix_size = num_tasks + 2
    matrix_alt = np.zeros((matrix_size, matrix_size), dtype=int)
    
    # Populate the alternative matrix based on task durations and predecessors
    for task in constraints:
        task_num = task[0]
        task_duration = task[1]
        if len(task) > 2:
            for predecessor in task[2:]:
                matrix_alt[predecessor][task_num] = task_duration
        else:
            matrix_alt[0][task_num] = task_duration
    
    # Ensure each task without successors points to an end node
    for task_num in range(1, num_tasks + 1):
        if not any(task_num in row for row in constraints):
            matrix_alt[task_num][num_tasks + 1] = 0 
    
    return matrix_alt

# Function to recursively visit nodes to detect cycles
def node_visit(node, matrix_alt, visited, stack):
    visited[node] = True
    stack[node] = True 

    for neighbour, weight in enumerate(matrix_alt[node]):
        if weight > 0:
            if not visited[neighbour]:
                if node_visit(neighbour, matrix_alt, visited, stack):
                    return True
            elif stack[neighbour]:
                return True

    stack[node] = False
    return False

# Function to detect cycles in the graph
def detect_cycles(matrix_alt):
    num_nodes = len(matrix_alt)
    visited = [False] * num_nodes
    stack = [False] * num_nodes

    for node in range(num_nodes):
        if not visited[node]:
            if node_visit(node, matrix_alt, visited, stack):
                return True

    return False

# Function to calculate ranks of nodes in a graph
def calculate_rank(graph):
    indegree = defaultdict(int)
    for node in graph:
        for successor in graph[node]:
            indegree[successor] += 1

    rank = {node: -1 for node in graph}
    queue = deque([node for node in graph if indegree[node] == 0])
    current_rank = 0

    while queue:
        next_queue = deque()

        while queue:
            node = queue.popleft()
            rank[node] = current_rank

            for successor in graph[node]:
                indegree[successor] -= 1
                if indegree[successor] == 0:
                    next_queue.append(successor)
        
        queue = next_queue
        current_rank += 1

    for node in indegree:
        if rank[node] == -1:
            rank[node] = 0

    return rank

# Function to compute the latest possible start dates for tasks
def compute_latest_dates(adjacency_matrix, earliest_dates):
    latest_dates = [earliest_dates[-1]] * len(adjacency_matrix)
    for i in range(len(adjacency_matrix) - 2, -1, -1):
        for j in range(len(adjacency_matrix)):
            if adjacency_matrix[i][j] != '*':
                latest_dates[i] = min(latest_dates[i], latest_dates[j] - int(adjacency_matrix[i][j]))
    return latest_dates

# Main loop to handle user input and execute the program
choice = 0
while choice != 1:

    table = input("Enter the table number (between 1 and 14) :")

    match table:
        case "1":
            file_path = 'src/table 1.txt'
        case "2":
            file_path = 'src/table 2.txt'
        case "3":
            file_path = 'src/table 3.txt'
        case "4":
            file_path = 'src/table 4.txt'
        case "5":
            file_path = 'src/table 5.txt'
        case "6":
            file_path = 'src/table 6.txt'
        case "7":
            file_path = 'src/table 7.txt'
        case "8":
            file_path = 'src/table 8.txt'
        case "9":
            file_path = 'src/table 9.txt'
        case "10":
            file_path = 'src/table 10.txt'
        case "11":
            file_path = 'src/table 11.txt'
        case "12":
            file_path = 'src/table 12.txt'
        case "13":
            file_path = 'src/table 13.txt'
        case "14":
            file_path = 'src/table 14.txt'
        case "test":
            file_path = 'src/test.txt'

    # Read data from the specified file and build the constraints table
    data = []  # This will hold each line of data from the file as a list of integers
    liste = ()  # This will collect all predecessors from all tasks for later checks
    compteur = 0  # Counter to keep track of the number of tasks read from the file
    
    # Open and read from the file specified in file_path
    with open(file_path, 'r') as file:
        for line in file:
            compteur += 1  # Increment task counter for each line
            # Convert each line to a list of integers
            task_data = list(map(int, line.split()))
            data.append(task_data)
            # Add all predecessors (from index 2 onwards) to the tuple
            liste = liste + tuple(task_data[2:])
    
    # Create an artificial 'end' task with no successors
    end = [len(data) + 1, 0]
    # Check which tasks are not in the list of predecessors and add them to 'end'
    for i in range(1, compteur + 1):
        if i not in liste:
            end.append(i)
    
    data.append(end)  # Append the 'end' task
    data.insert(0, [0, 0])  # Insert a starting task at the beginning
    
    # Re-read constraints from the file for clean data processing
    constraints = read_constraints(file_path)
    constraints.insert(0, (0, 0))  # Insert a starting task into constraints for uniformity
    
    # Prepare a tuple to be added at the end of constraints to handle end tasks
    end = ()
    end = end + (len(constraints),)  # Include the total number of tasks as a terminator
    end = end + (0,)  # Add a '0' to indicate no successors
    for i in range(1, compteur + 1):
        if i not in liste:
            end = end + (i,)  # Include tasks that are not any task's predecessor
    constraints.append(end)  # Append this to the constraints
    print('\n')
    
    # Create a graph from constraints using defaultdict
    graph = defaultdict(list)
    for task in constraints:
        task_id = task[0]
        predecessors = task[2:]
        for predecessor in predecessors:
            graph[predecessor].append(task_id)  # Append task_id to the list of predecessors
    
    graph_conv = []  # To store converted graph data for matrix generation
    
    # Print selected table and display the graph structure
    print('You chose table', table)
    print('\n')
    print('Here is the graph:')
    print('\n')
    print('Node N° -> [Successors]')
    print('(duration)')
    print('----------------------')
    
    # Print each node and its successors
    for node in graph:
        new_entry = list(constraints[node][:2]) + list(graph[node])
        graph_conv.append(new_entry)
        if node == 0:  # Print 'α' for the starting node
            print(f"Node α -> {graph[node]}")
            print(constraints[node][1:2])
        else:
            print(f"Node {node} -> {graph[node]}")
            print(constraints[node][1:2])
    print('\n')
    
    print('Here is the adjacency matrix:')
    print('\n')
    
    # Generate and print the adjacency matrix
    adjacency_matrix = create_adjacency_matrix(graph_conv)
    print_adjacency_matrix(adjacency_matrix)
    print('\n')
    
    # Create an alternative matrix and check for cycles
    matrix_alt = create_matrix_alt(constraints)
    has_cycle = detect_cycles(matrix_alt)
    
    # Notify user if the graph has a cycle
    print(f"Has cycle: {has_cycle}")
    
    # If a cycle is detected, prompt the user with options
    if has_cycle == True:
        print("The graph has a cycle and cannot be ranked.")
        choice = int(input("Enter 1 to exit or any other number to continue: "))
        print('\n')
    else:  # If no cycle, proceed with further analysis
        print('\n')
        ranks = calculate_rank(graph)  # Calculate ranks of each node
    
        # Print the ranks of each node
        print('Here are the ranks for each node:')
        print('\n')
        for node in ranks:
            if node == 0:
                print(f"Rank of node α: {ranks[node]}")
            elif node == len(constraints) - 1:
                print(f"Rank of node ω: {ranks[node]}")
            else:
                print(f"Rank of node {node}: {ranks[node]}")
        print('\n')
    
        # Determine the earliest start times for tasks using a topological sort-like approach
        tasks = {task[0]: {'duration': task[1], 'predecessors': task[2:], 'earliest_start': 0} for task in data}
        no_predecessors = [task for task, info in tasks.items() if not info['predecessors']]
    
        while no_predecessors:
            current_task = no_predecessors.pop(0)
            current_end = tasks[current_task]['earliest_start'] + tasks[current_task]['duration']
            for successor in tasks:
                if current_task in tasks[successor]['predecessors']:
                    tasks[successor]['earliest_start'] = max(tasks[successor]['earliest_start'], current_end)
                    tasks[successor]['predecessors'].remove(current_task)
                    if not tasks[successor]['predecessors']:
                        no_predecessors.append(successor)
    
        earliest_start_times = {task: info['earliest_start'] for task, info in tasks.items()}
    
        # Print the earliest start times
        print('Here are the earliest start times for each task:')
        print('\n')
        for task in earliest_start_times:
            if task == 0:
                print(f"Task α: {earliest_start_times[task]}")
            elif task == len(constraints) - 1:
                print(f"Task ω: {earliest_start_times[task]}")
            else:
                print(f"Task {task}: {earliest_start_times[task]}")
        print('\n')
    
        # Calculate the latest start times for each task
        earliest_dates = list(earliest_start_times.values())
        latest_dates = compute_latest_dates(adjacency_matrix, earliest_dates)
    
        # Print the latest start times
        print('Here are the latest start times for each task:')
        print('\n')
        for i in range(len(earliest_dates)):
            if i == 0:
                print(f"Task α: {latest_dates[i]}")
            elif i == len(constraints) - 1:
                print(f"Task ω: {latest_dates[i]}")
            else:
                print(f"Task {i}: {latest_dates[i]}")
        print('\n')
    
        # Calculate and print the total margins for each task
        print('Here are the total margins for each task:')
        print('\n')
        for i in range(len(earliest_dates)):
            total_margin = latest_dates[i] - earliest_dates[i]
            if i == 0:
                print(f"Task α: {total_margin}")
            elif i == len(constraints) - 1:
                print(f"Task ω: {total_margin}")
            else:
                print(f"Task {i}: {total_margin}")
    
        print('\n')
        # Determine and print the critical path
        print('Here is the critical path:')
        print('\n')
        critical_path = []
        for i in range(len(adjacency_matrix)):
            if latest_dates[i] == earliest_dates[i]:
                if i == 0:
                    critical_path.append('α')
                elif i == len(constraints) - 1:
                    critical_path.append('ω')
                else:
                    critical_path.append(i)
        print(critical_path)
        print('\n')
    
        # User input to continue or exit the loop
        choice = int(input("Enter 1 to exit or any other number to continue: "))
    
    