"""
Punto de Entrada - Maze Solver (Refactorizado)
Proyecto #2: Búsqueda y Heurísticas
Autor: Nicolás Concuá
"""

import sys
from maze import Maze
import algorithms
from heuristics import manhattan, euclidean
from visualizer import save_maze_results


def display_metrics(name, result):
    """Imprime las métricas de forma ordenada."""
    print(f"--- {name} ---")
    print(f"Nodos visitados:     {result.nodes_explored}")
    print(f"Largo del camino:    {result.path_length}")
    print(f"Tiempo de ejecución: {result.execution_time:.6f} s\n")

def main():
    if len(sys.argv) < 2:
        print("Uso correcto: python main.py <ruta_al_laberinto.txt>")
        return

    filepath = sys.argv[1]

    try:
        print(f"Cargando laberinto desde: {filepath}...\n")
        maze = Maze(filepath)

    except FileNotFoundError:
        print("Error: El archivo no existe.")
        return

    except ValueError as e:
        print(f"Error en el laberinto: {e}")
        return

    except Exception as e:
        print(f"Error inesperado: {e}")
        return

    print("Ejecutando algoritmos y generando visualizaciones en ./results/\n")

    try:

        # BFS
        res_bfs = algorithms.bfs(maze)
        display_metrics("BFS", res_bfs)
        save_maze_results(maze, res_bfs.path, res_bfs.visited_ordered, "BFS")

        # DFS
        res_dfs = algorithms.dfs(maze)
        display_metrics("DFS", res_dfs)
        save_maze_results(maze, res_dfs.path, res_dfs.visited_ordered, "DFS")

        # Greedy (Manhattan)
        res_greedy = algorithms.greedy(maze, manhattan)
        display_metrics("Greedy (Manhattan)", res_greedy)
        save_maze_results(maze, res_greedy.path, res_greedy.visited_ordered, "Greedy Manhattan")

        # A* (Euclidiana)
        res_astar = algorithms.a_star(maze, euclidean)
        display_metrics("A* (Euclidiana)", res_astar)
        save_maze_results(maze, res_astar.path, res_astar.visited_ordered, "A Star Euclidiana")

    except Exception as e:
        print(f"Error durante la ejecución de algoritmos: {e}")
        return

    print("Proceso completado. Revisa la carpeta 'results/' para ver las imágenes.")


main()