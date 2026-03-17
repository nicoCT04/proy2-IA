"""
Interfaz Gráfica Streamlit - Maze Solver
"""
import streamlit as st
import tempfile
import matplotlib.pyplot as plt
import numpy as np

from maze import Maze
import algorithms
from heuristics import manhattan, euclidean

st.set_page_config(page_title="Maze Solver - Proyecto 2", layout="wide")

def render_maze_pyplot(maze, path, visited, title):
    """Genera la gráfica directamente para Streamlit."""
    fig, ax = plt.subplots(figsize=(8, 8))
    grid_data = np.array([[0 if cell == '1' else 1 for cell in row] for row in maze.grid])
    
    ax.imshow(grid_data, cmap='gray', origin='upper')

    if visited:
        v_rows, v_cols = zip(*visited)
        ax.scatter(v_cols, v_rows, color='#3498db', s=5, alpha=0.5, label='Explorado')

    if path:
        p_rows, p_cols = zip(*path)
        ax.plot(p_cols, p_rows, color='#e74c3c', linewidth=2, label='Camino')

    if maze.start:
        ax.plot(maze.start[1], maze.start[0], 'go', markersize=8, label='Inicio')
    
    for g in maze.goals:
        ax.plot(g[1], g[0], 'yx', markersize=10, label='Meta')

    ax.set_title(title)
    ax.legend(loc='upper right')
    ax.axis('off')
    return fig

# --- INTERFAZ DE USUARIO ---
st.title("🧩 Maze Solver - Inteligencia Artificial")
st.markdown("Comparación de algoritmos de búsqueda informada y no informada.")

# Barra lateral para controles
with st.sidebar:
    st.header("Configuración")
    uploaded_file = st.file_uploader("Cargar laberinto (.txt)", type=['txt'])
    
    start_mode = st.radio("Punto de Partida:", ["Original del archivo", "Aleatorio"])
    
    algo_choice = st.selectbox("Seleccionar Algoritmo:", 
                                ["Todos", "BFS", "DFS", "Greedy (Manhattan)", "A* (Euclidiana)"])
    
    run_btn = st.button("Resolver Laberinto", type="primary")

# Lógica principal
if uploaded_file is not None and run_btn:
    # Streamlit maneja archivos en memoria, lo guardamos temporalmente para que Maze() lo lea
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    maze = Maze(tmp_path)

    if start_mode == "Aleatorio":
        maze.set_random_start()
        st.info(f"Nuevo punto de partida aleatorio generado en: {maze.start}")

    # Diccionario de algoritmos a ejecutar
    algos_to_run = {}
    if algo_choice in ["Todos", "BFS"]:
        algos_to_run["BFS"] = algorithms.bfs(maze)
    if algo_choice in ["Todos", "DFS"]:
        algos_to_run["DFS"] = algorithms.dfs(maze)
    if algo_choice in ["Todos", "Greedy (Manhattan)"]:
        algos_to_run["Greedy (Manhattan)"] = algorithms.greedy(maze, manhattan)
    if algo_choice in ["Todos", "A* (Euclidiana)"]:
        algos_to_run["A* (Euclidiana)"] = algorithms.a_star(maze, euclidean)

    # Mostrar resultados en columnas
    cols = st.columns(len(algos_to_run))
    
    for idx, (name, (res, visited, path)) in enumerate(algos_to_run.items()):
        with cols[idx]:
            st.subheader(name)
            st.metric("Largo del Camino", res.path_length)
            st.metric("Nodos Explorados", res.nodes_explored)
            st.metric("Tiempo (s)", f"{res.execution_time:.5f}")
            
            fig = render_maze_pyplot(maze, path, visited, name)
            st.pyplot(fig)