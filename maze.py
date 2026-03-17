"""
Módulo del Laberinto
"""
import random

class Maze:
    def __init__(self, filepath):
        self.grid = []
        self.start = None
        self.goals = []
        self.load_maze(filepath)
        
        # Jerarquía de movimientos: Arriba, Derecha, Abajo, Izquierda 
        # Representado como (delta_fila, delta_columna)
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def load_maze(self, filepath):
        """Lee el archivo .txt y mapea los estados del laberinto."""
        with open(filepath, 'r') as file:
            for row_idx, line in enumerate(file):
                row = list(line.strip())
                self.grid.append(row)
                for col_idx, char in enumerate(row):
                    if char == '2': # Punto de partida [cite: 12]
                        self.start = (row_idx, col_idx)
                    elif char == '3': # Punto de salida [cite: 14]
                        self.goals.append((row_idx, col_idx))

    def get_neighbors(self, position):
        """Devuelve los vecinos válidos respetando la jerarquía de movimientos."""
        row, col = position
        neighbors = []
        
        for dr, dc in self.directions:
            new_row, new_col = row + dr, col + dc
            # Verifica límites y si el camino está libre ('0' o '3') [cite: 10, 14]
            if (0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0])):
                if self.grid[new_row][new_col] in ['0', '3', '2']:
                    neighbors.append((new_row, new_col))
                    
        return neighbors
    
    def set_random_start(self):
        """Asigna un punto de partida aleatorio en un camino libre."""
        free_spaces = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == '0':
                    free_spaces.append((r, c))
        
        if free_spaces:
            self.start = random.choice(free_spaces)
            return self.start
        return None