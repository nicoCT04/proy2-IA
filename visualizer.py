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

    # Crear figura con GridSpec: fila superior para la leyenda, fila inferior para el mapa
    # aumentar ligeramente el tamaño de la figura y reducir la altura de la leyenda
    fig = plt.figure(figsize=(11, 11))
    gs = fig.add_gridspec(2, 1, height_ratios=[0.06, 0.94], hspace=0.02)

    # Eje dedicado solo a la leyenda (arriba)
    ax_legend = fig.add_subplot(gs[0])
    ax_legend.axis('off')
    # asegurar que no tenga parche de fondo que cree un cuadro
    ax_legend.patch.set_visible(False)

    # Eje principal para el mapa (abajo)
    ax = fig.add_subplot(gs[1])
    ax.set_aspect('equal')
    ax.imshow(grid_data, cmap='gray_r', origin='upper', interpolation='nearest')
    # ocultar ejes y spines para que no aparezca ningún cuadro alrededor
    ax.axis('off')
    for spine in ax.spines.values():
        spine.set_visible(False)

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

    # Asegurar que no exista una leyenda residual en el eje del mapa
    existing_leg = ax.get_legend()
    if existing_leg is not None:
        try:
            existing_leg.remove()
        except Exception:
            pass

    # Preparar leyenda: extraer handles únicos y dibujar en el eje superior
    handles, labels = ax.get_legend_handles_labels()
    if labels:
        by_label = dict(zip(labels, handles))
        # Dibujar la leyenda centrada en el eje superior (ax_legend)
        leg = ax_legend.legend(by_label.values(), by_label.keys(), loc='center',
                               ncol=min(4, len(by_label)), frameon=False, prop={'size': 10})
        # asegurar que no haya parche que cree un recuadro lateral
        if leg.get_frame() is not None:
            leg.get_frame().set_alpha(0.0)

    # Título general en la figura (supertitle) y no usar leyenda en el eje del mapa
    # título general ligeramente más abajo para no superponerse al mapa
    fig.suptitle(f"Resultado: {name}   Nodos Visitados: {len(visited)} | Largo: {len(path)-1 if path else 0}",
                 fontsize=12, y=0.975)

    # Ajustar márgenes para evitar cuadros laterales y guardar en disco
    # ajustar márgenes para dejar espacio al título y maximizar área del mapa
    fig.subplots_adjust(hspace=0.02, left=0, right=1, top=0.96, bottom=0)
    clean_name = name.lower().replace(' ', '_').replace('*', 'star')
    filename = f"results/{clean_name}.png"
    fig.savefig(filename, bbox_inches='tight', pad_inches=0.02, dpi=150)
    plt.close(fig)