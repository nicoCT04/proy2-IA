"""
Punto de Entrada - Maze Solver
Autor: Nicolás Concuá
"""
import sys
from maze import Maze
from algorithms import bfs, dfs, a_star, greedy
from heuristics import manhattan, euclidean

def display_results(name, result):
    """Muestra los resultados en consola según los requerimientos."""
    print(f"--- {name} ---")
    print(f"Nodos visitados:     {result.nodes_explored}")
    print(f"Largo del camino:    {result.path_length}")
    print(f"Tiempo de ejecución: {result.execution_time:.6f} s\n")

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <ruta_al_laberinto.txt>")
        return

    filepath = sys.argv[1]
    print(f"Cargando laberinto: {filepath}...\n")
    maze = Maze(filepath)

    if not maze.start or not maze.goals:
        print("Error: El laberinto debe tener un punto de partida ('2') y una salida ('3').")
        return

    # Ejecución de algoritmos [cite: 55]
    res_bfs = bfs(maze)
    display_results("BFS", res_bfs)

    res_dfs = dfs(maze)
    display_results("DFS", res_dfs)

    res_greedy_manhattan = greedy(maze, manhattan)
    display_results("Greedy (Manhattan)", res_greedy_manhattan)

    res_astar_euclidean = a_star(maze, euclidean)
    display_results("A* (Euclidiana)", res_astar_euclidean)

if __name__ == "__main__":
    main()