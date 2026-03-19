"""
Módulo de Algoritmos de Búsqueda (Refactorizado)
"""
import time
from collections import deque
import heapq


class SearchResult:
    def __init__(self, path, visited_ordered, execution_time):
        self.path = path
        self.visited_ordered = visited_ordered
        self.execution_time = execution_time

        # Métricas derivadas
        self.path_length = len(path) - 1 if path else 0
        self.nodes_explored = len(visited_ordered)

def reconstruct_path(parent, node):
    path = []
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


def get_closest_goal(node, goals, heuristic_func):
    return min(goals, key=lambda g: heuristic_func(node, g))


def bfs(maze):
    start_time = time.time()

    queue = deque([maze.start])
    parent = {maze.start: None}
    visited_set = set([maze.start])
    visited_ordered = []

    while queue:
        current = queue.popleft()
        visited_ordered.append(current)

        if current in maze.goals:
            path = reconstruct_path(parent, current)
            return SearchResult(path, visited_ordered, time.time() - start_time)

        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return SearchResult([], visited_ordered, time.time() - start_time)

def dfs(maze):
    start_time = time.time()

    stack = [maze.start]
    parent = {maze.start: None}
    visited_set = set()
    visited_ordered = []

    while stack:
        current = stack.pop()

        if current not in visited_set:
            visited_set.add(current)
            visited_ordered.append(current)

            if current in maze.goals:
                path = reconstruct_path(parent, current)
                return SearchResult(path, visited_ordered, time.time() - start_time)

            neighbors = maze.get_neighbors(current)
            for neighbor in reversed(neighbors):  # respeta jerarquía
                if neighbor not in visited_set:
                    parent[neighbor] = current
                    stack.append(neighbor)

    return SearchResult([], visited_ordered, time.time() - start_time)


def a_star(maze, heuristic_func):
    start_time = time.time()

    pq = []
    count = 0

    heapq.heappush(pq, (0, count, maze.start))
    g_costs = {maze.start: 0}
    parent = {maze.start: None}
    visited_set = set()
    visited_ordered = []

    while pq:
        f_cost, _, current = heapq.heappop(pq)

        if current in visited_set:
            continue

        visited_set.add(current)
        visited_ordered.append(current)

        if current in maze.goals:
            path = reconstruct_path(parent, current)
            return SearchResult(path, visited_ordered, time.time() - start_time)

        for neighbor in maze.get_neighbors(current):
            tentative_g = g_costs[current] + 1

            if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g
                parent[neighbor] = current

                goal = get_closest_goal(neighbor, maze.goals, heuristic_func)
                f = tentative_g + heuristic_func(neighbor, goal)

                count += 1
                heapq.heappush(pq, (f, count, neighbor))

    return SearchResult([], visited_ordered, time.time() - start_time)



def greedy(maze, heuristic_func):
    start_time = time.time()

    pq = []
    count = 0

    heapq.heappush(pq, (0, count, maze.start))
    parent = {maze.start: None}
    visited_set = set()
    visited_ordered = []

    while pq:
        h_cost, _, current = heapq.heappop(pq)

        if current in visited_set:
            continue

        visited_set.add(current)
        visited_ordered.append(current)

        if current in maze.goals:
            path = reconstruct_path(parent, current)
            return SearchResult(path, visited_ordered, time.time() - start_time)

        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited_set:
                parent[neighbor] = current

                goal = get_closest_goal(neighbor, maze.goals, heuristic_func)
                h = heuristic_func(neighbor, goal)

                count += 1
                heapq.heappush(pq, (h, count, neighbor))

    return SearchResult([], visited_ordered, time.time() - start_time)