"""
Interfaz Gráfica Streamlit - Maze Solver (Refactorizado)
Proyecto #2: Búsqueda y Heurísticas
"""

import streamlit as st
import tempfile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from maze import Maze
import algorithms
from heuristics import manhattan, euclidean

st.set_page_config(page_title="Maze Solver - Proyecto 2", layout="wide")

if 'last_results' not in st.session_state:
    st.session_state.last_results = None
if 'maze_obj' not in st.session_state:
    st.session_state.maze_obj = None
if 'current_h' not in st.session_state:
    st.session_state.current_h = "Manhattan"


def calculate_ebf(n_explored, depth):
    if depth <= 0:
        return 0
    return round(n_explored ** (1 / depth), 4)


def render_maze_pyplot(maze, path, visited, title):
    fig, ax = plt.subplots(figsize=(8, 8))
    grid_data = np.array([[0 if cell == '1' else 1 for cell in row] for row in maze.grid])
    ax.imshow(grid_data, cmap='gray', origin='upper')

    if visited:
        v_rows, v_cols = zip(*visited)
        ax.scatter(v_cols, v_rows, s=5, alpha=0.4)

    if path:
        p_rows, p_cols = zip(*path)
        ax.plot(p_cols, p_rows, linewidth=2.5)

    if maze.start:
        ax.plot(maze.start[1], maze.start[0], 'go')
    for g in maze.goals:
        ax.plot(g[1], g[0], 'yx')

    ax.set_title(title)
    ax.axis('off')
    return fig


def animate_maze_pyplot(maze, visited, path, title):
    placeholder = st.empty()

    grid_data = np.array([[0 if cell == '1' else 1 for cell in row] for row in maze.grid])

    if not path:
        st.warning(f"No hay camino para animar en {title}")
        return

    step = max(1, len(path) // 40)

    for i in range(1, len(path) + 1, step):
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.imshow(grid_data, cmap='gray', origin='upper')

        if visited:
            v_rows, v_cols = zip(*visited)
            ax.scatter(v_cols, v_rows, s=5, alpha=0.2)

        current_path = path[:i]
        p_rows, p_cols = zip(*current_path)
        ax.plot(p_cols, p_rows, linewidth=2.5)

        if maze.start:
            ax.plot(maze.start[1], maze.start[0], 'go')
        for g in maze.goals:
            ax.plot(g[1], g[0], 'yx')

        ax.set_title(f"{title} ({i-1} pasos)")
        ax.axis('off')

        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.02)

st.title("Maze Solver - Análisis de Algoritmos")

with st.sidebar:
    st.header("Configuración")

    uploaded_file = st.file_uploader("Cargar laberinto (.txt)", type=['txt'])
    start_mode = st.radio("Inicio:", ["Original", "Aleatorio"])

    h_name = st.selectbox("Heurística:", ["Manhattan", "Euclidiana"])
    sel_h = manhattan if h_name == "Manhattan" else euclidean

    algo_choice = st.selectbox("Algoritmo:", ["Todos", "BFS", "DFS", "Greedy", "A*"])

    run_btn = st.button("Resolver")


if uploaded_file is not None:
    if run_btn:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            maze = Maze(tmp_path)

            if start_mode == "Aleatorio":
                maze.set_random_start()

            results = {}

            if algo_choice in ["Todos", "BFS"]:
                results["BFS"] = algorithms.bfs(maze)

            if algo_choice in ["Todos", "DFS"]:
                results["DFS"] = algorithms.dfs(maze)

            if algo_choice in ["Todos", "Greedy"]:
                results["Greedy"] = algorithms.greedy(maze, sel_h)

            if algo_choice in ["Todos", "A*"]:
                results["A*"] = algorithms.a_star(maze, sel_h)

            st.session_state.last_results = results
            st.session_state.maze_obj = maze
            st.session_state.current_h = h_name

        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.last_results:
        tab1, tab2 = st.tabs(["Análisis", "Animación"])

        with tab1:
            res_dict = st.session_state.last_results
            m_obj = st.session_state.maze_obj

            cols = st.columns(len(res_dict))

            for idx, (name, res) in enumerate(res_dict.items()):
                with cols[idx]:
                    st.metric(f"{name} (Nodos)", res.nodes_explored)
                    st.pyplot(render_maze_pyplot(m_obj, res.path, res.visited_ordered, name))

            # Tabla
            data_summary = []
            for name, res in res_dict.items():
                h_val = st.session_state.current_h if name in ["Greedy", "A*"] else "N/A"

                ebf = calculate_ebf(res.nodes_explored, res.path_length)

                data_summary.append({
                    "Algoritmo": name,
                    "Heurística": h_val,
                    "Nodos": res.nodes_explored,
                    "Profundidad": res.path_length,
                    "Branching Factor": ebf,
                    "Tiempo (ms)": round(res.execution_time * 1000, 4)
                })

            df = pd.DataFrame(data_summary)
            st.table(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Descargar CSV", csv, "resultados.csv", "text/csv")

        with tab2:
            if st.button("Iniciar Animación"):
                for name, res in st.session_state.last_results.items():
                    st.write(f"Animando: {name}")
                    animate_maze_pyplot(
                        st.session_state.maze_obj,
                        res.visited_ordered,
                        res.path,
                        name
                    )