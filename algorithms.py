"""
Módulo de Algoritmos de Búsqueda
"""
import time
from collections import deque
import heapq

class SearchResult:
    def __init__(self, path_length, nodes_explored, execution_time):
        self.path_length = path_length # Largo del camino [cite: 29]
        self.nodes_explored = nodes_explored # Cantidad de nodos [cite: 30]
        self.execution_time = execution_time # Tiempo de ejecución [cite: 31]

def bfs(maze):
    start_time = time.time()
    queue = deque([(maze.start, [maze.start])])
    visited = set([maze.start])
    nodes_explored = 0

    while queue:
        current, path = queue.popleft()
        nodes_explored += 1

        if current in maze.goals:
            return SearchResult(len(path) - 1, nodes_explored, time.time() - start_time)

        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return SearchResult(0, nodes_explored, time.time() - start_time)

def dfs(maze):
    start_time = time.time()
    stack = [(maze.start, [maze.start])]
    visited = set()
    nodes_explored = 0

    while stack:
        current, path = stack.pop()
        
        if current not in visited:
            visited.add(current)
            nodes_explored += 1

            if current in maze.goals:
                return SearchResult(len(path) - 1, nodes_explored, time.time() - start_time)

            # Invertimos los vecinos para que el .pop() respete la jerarquía Arriba, Der, Abajo, Izq
            neighbors = maze.get_neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return SearchResult(0, nodes_explored, time.time() - start_time)

def a_star(maze, heuristic_func):
    start_time = time.time()
    # Priority queue: (f_cost, count, current_node, path)
    # count evita empates comparando nodos directamente
    pq = []
    count = 0 
    goal = maze.goals[0] if maze.goals else (0,0)
    
    heapq.heappush(pq, (0, count, maze.start, [maze.start]))
    g_costs = {maze.start: 0}
    nodes_explored = 0
    visited = set()

    while pq:
        f_cost, _, current, path = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        nodes_explored += 1

        if current in maze.goals:
            return SearchResult(len(path) - 1, nodes_explored, time.time() - start_time)

        for neighbor in maze.get_neighbors(current):
            tentative_g_cost = g_costs[current] + 1
            
            if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g_cost
                f = tentative_g_cost + heuristic_func(neighbor, goal)
                count += 1
                heapq.heappush(pq, (f, count, neighbor, path + [neighbor]))

    return SearchResult(0, nodes_explored, time.time() - start_time)

def greedy(maze, heuristic_func):
    start_time = time.time()
    pq = []
    count = 0
    goal = maze.goals[0] if maze.goals else (0,0)
    
    heapq.heappush(pq, (0, count, maze.start, [maze.start]))
    visited = set()
    nodes_explored = 0

    while pq:
        h_cost, _, current, path = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        nodes_explored += 1

        if current in maze.goals:
            return SearchResult(len(path) - 1, nodes_explored, time.time() - start_time)

        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited:
                count += 1
                h = heuristic_func(neighbor, goal)
                heapq.heappush(pq, (h, count, neighbor, path + [neighbor]))

    return SearchResult(0, nodes_explored, time.time() - start_time)