"""
Módulo de Algoritmos de Búsqueda
"""
import time
from collections import deque
import heapq

class SearchResult:
    def __init__(self, path_length, nodes_explored, execution_time):
        self.path_length = path_length
        self.nodes_explored = nodes_explored
        self.execution_time = execution_time

def bfs(maze):
    start_time = time.time()
    queue = deque([(maze.start, [maze.start])])
    visited_set = set([maze.start])
    visited_ordered = []

    while queue:
        current, path = queue.popleft()
        visited_ordered.append(current)

        if current in maze.goals:
            res = SearchResult(len(path) - 1, len(visited_ordered), time.time() - start_time)
            return res, visited_ordered, path

        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    res = SearchResult(0, len(visited_ordered), time.time() - start_time)
    return res, visited_ordered, []

def dfs(maze):
    start_time = time.time()
    stack = [(maze.start, [maze.start])]
    visited_set = set()
    visited_ordered = []

    while stack:
        current, path = stack.pop()
        
        if current not in visited_set:
            visited_set.add(current)
            visited_ordered.append(current)

            if current in maze.goals:
                res = SearchResult(len(path) - 1, len(visited_ordered), time.time() - start_time)
                return res, visited_ordered, path

            # Invertimos los vecinos para respetar la jerarquía (Arriba, Derecha, Abajo, Izquierda) al hacer pop()
            neighbors = maze.get_neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor not in visited_set:
                    stack.append((neighbor, path + [neighbor]))

    res = SearchResult(0, len(visited_ordered), time.time() - start_time)
    return res, visited_ordered, []

def a_star(maze, heuristic_func):
    start_time = time.time()
    pq = []
    count = 0 
    goal = maze.goals[0] if maze.goals else (0,0)
    
    heapq.heappush(pq, (0, count, maze.start, [maze.start]))
    g_costs = {maze.start: 0}
    visited_set = set()
    visited_ordered = []

    while pq:
        f_cost, _, current, path = heapq.heappop(pq)
        
        if current in visited_set:
            continue
            
        visited_set.add(current)
        visited_ordered.append(current)

        if current in maze.goals:
            res = SearchResult(len(path) - 1, len(visited_ordered), time.time() - start_time)
            return res, visited_ordered, path

        for neighbor in maze.get_neighbors(current):
            tentative_g_cost = g_costs[current] + 1
            
            if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g_cost
                f = tentative_g_cost + heuristic_func(neighbor, goal)
                count += 1
                heapq.heappush(pq, (f, count, neighbor, path + [neighbor]))

    res = SearchResult(0, len(visited_ordered), time.time() - start_time)
    return res, visited_ordered, []

def greedy(maze, heuristic_func):
    start_time = time.time()
    pq = []
    count = 0
    goal = maze.goals[0] if maze.goals else (0,0)
    
    heapq.heappush(pq, (0, count, maze.start, [maze.start]))
    visited_set = set()
    visited_ordered = []

    while pq:
        h_cost, _, current, path = heapq.heappop(pq)
        
        if current in visited_set:
            continue
            
        visited_set.add(current)
        visited_ordered.append(current)

        if current in maze.goals:
            res = SearchResult(len(path) - 1, len(visited_ordered), time.time() - start_time)
            return res, visited_ordered, path

        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited_set:
                count += 1
                h = heuristic_func(neighbor, goal)
                heapq.heappush(pq, (h, count, neighbor, path + [neighbor]))

    res = SearchResult(0, len(visited_ordered), time.time() - start_time)
    return res, visited_ordered, []