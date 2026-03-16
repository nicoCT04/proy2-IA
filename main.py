"""
Punto de Entrada - Maze Solver
Proyecto #2: Búsqueda y Heurísticas
Autor: Nicolás Concuá
"""
import sys
from maze import Maze
import algorithms
from heuristics import manhattan, euclidean
from visualizer import save_maze_results

def display_metrics(name, result):
    """Imprime las métricas requeridas en consola de forma ordenada."""
    print(f"--- {name} ---")
    print(f"Nodos visitados:     {result.nodes_explored}")
    print(f"Largo del camino:    {result.path_length}")
    print(f"Tiempo de ejecución: {result.execution_time:.6f} s\n")

def main():
    if len(sys.argv) < 2:
        print("Error. Uso correcto: python main.py <ruta_al_laberinto.txt>")
        return

    filepath = sys.argv[1]
    print(f"Cargando laberinto desde: {filepath}...\n")
    maze = Maze(filepath)

    if not maze.start or not maze.goals:
        print("Error: El laberinto no tiene un punto de partida ('2') o una salida ('3').")
        return

    print("Ejecutando algoritmos y generando visualizaciones en ./results/\n")

    # 1. Breadth First Search (BFS)
    res_bfs, visited_bfs, path_bfs = algorithms.bfs(maze)
    display_metrics("BFS", res_bfs)
    save_maze_results(maze, path_bfs, visited_bfs, "BFS")

    # 2. Depth First Search (DFS)
    res_dfs, visited_dfs, path_dfs = algorithms.dfs(maze)
    display_metrics("DFS", res_dfs)
    save_maze_results(maze, path_dfs, visited_dfs, "DFS")

    # 3. Greedy First Search (Usando Manhattan)
    res_greedy, visited_greedy, path_greedy = algorithms.greedy(maze, manhattan)
    display_metrics("Greedy (Manhattan)", res_greedy)
    save_maze_results(maze, path_greedy, visited_greedy, "Greedy Manhattan")

    # 4. A* Search (Usando Euclidiana)
    res_astar, visited_astar, path_astar = algorithms.a_star(maze, euclidean)
    display_metrics("A* (Euclidiana)", res_astar)
    save_maze_results(maze, path_astar, visited_astar, "A Star Euclidiana")

    print("¡Proceso completado! Revisa la carpeta 'results/' para ver las imágenes.")

if __name__ == "__main__":
    main()