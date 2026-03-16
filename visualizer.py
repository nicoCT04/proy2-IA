"""
Módulo de Visualización
"""
import matplotlib.pyplot as plt
import numpy as np
import os

def save_maze_results(maze, path, visited, name):
    """Genera y guarda una representación visual del laberinto resuelto."""
    if not os.path.exists('results'):
        os.makedirs('results')

    # Matriz para la imagen: Paredes = 0 (Negro), Caminos = 1 (Blanco)
    grid_data = np.array([[0 if cell == '1' else 1 for cell in row] for row in maze.grid])

    plt.figure(figsize=(10, 10))
    plt.imshow(grid_data, cmap='gray_r', origin='upper', interpolation='nearest')

    ax = plt.gca()
    ax.set_aspect('equal')

    # Capa 1: Nodos explorados (mancha azul claro) - fondo, zorder bajo
    if visited:
        visited_arr = np.array(list(visited))
        if visited_arr.size > 0:
            v_rows = visited_arr[:, 0]
            v_cols = visited_arr[:, 1]
            ax.scatter(v_cols, v_rows, color='#3498db', s=6, alpha=0.35, label='Explorado', zorder=1)

    # Capa 2: Camino final (línea roja) - encima de explorados, zorder alto
    if path:
        path_arr = np.array(path)
        if path_arr.size > 0:
            p_rows = path_arr[:, 0]
            p_cols = path_arr[:, 1]
            ax.plot(p_cols, p_rows, color='#e74c3c', linewidth=2.5, label='Camino Solución', zorder=3)

    # Capa 3: Puntos de Inicio y Fin - siempre por encima (zorder máximo)
    # Si hay camino, marcar inicio/fin a partir del mismo para consistencia
    if path and len(path) > 0:
        start_pt = path[0]
        end_pt = path[-1]
        ax.scatter(start_pt[1], start_pt[0], color='green', s=50, marker='o', edgecolor='k', label='Inicio', zorder=4)
        ax.scatter(end_pt[1], end_pt[0], color='yellow', s=70, marker='X', edgecolor='k', label='Meta', zorder=4)
    else:
        if getattr(maze, 'start', None):
            ax.scatter(maze.start[1], maze.start[0], color='green', s=50, marker='o', edgecolor='k', label='Inicio', zorder=4)
        # dibujar metas sin repetir etiquetas
        for idx, g in enumerate(getattr(maze, 'goals', []) or []):
            if idx == 0:
                ax.scatter(g[1], g[0], color='yellow', s=70, marker='X', edgecolor='k', label='Meta', zorder=4)
            else:
                ax.scatter(g[1], g[0], color='yellow', s=70, marker='X', edgecolor='k', zorder=4)

    # Leyenda única y posicionada sobre la imagen (arriba)
    handles, labels = ax.get_legend_handles_labels()
    if labels:
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, 1.12),
                  ncol=min(3, len(by_label)), framealpha=0.9)

    # Formato final de la imagen
    plt.title(f"Resultado: {name}\nNodos Visitados: {len(visited)} | Largo: {len(path)-1 if path else 0}")
    plt.legend(loc='upper right')
    plt.axis('off')

    # Guardar en disco
    clean_name = name.lower().replace(' ', '_').replace('*', 'star')
    filename = f"results/{clean_name}.png"
    plt.savefig(filename, bbox_inches='tight', dpi=150)
    plt.close()