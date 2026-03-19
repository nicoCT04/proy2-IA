"""
Módulo del Laberinto (Refactorizado con Validación)
"""
import random


class Maze:
    def __init__(self, filepath):
        self.grid = []
        self.start = None
        self.goals = []
        self.load_maze(filepath)

        # Jerarquía de movimientos: Arriba, Derecha, Abajo, Izquierda
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def load_maze(self, filepath):
        """Lee el archivo .txt, valida formato flexible y construye el laberinto."""
        with open(filepath, 'r') as file:
            # Limpiar líneas vacías y espacios
            lines = [line.strip() for line in file.readlines() if line.strip()]

        if not lines:
            raise ValueError("El archivo está vacío")

        valid_chars = {'0', '1', '2', '3'}

        expected_width = len(lines[0])  # ancho esperado

        for row_idx, line in enumerate(lines):
            row = list(line)

            # Validar que todas las filas tengan el mismo tamaño
            if len(row) != expected_width:
                raise ValueError(
                    f"Inconsistencia en fila {row_idx}: "
                    f"esperado {expected_width} columnas, pero tiene {len(row)}"
                )

            for col_idx, char in enumerate(row):
                if char not in valid_chars:
                    raise ValueError(
                        f"Caracter inválido '{char}' en ({row_idx}, {col_idx})"
                    )

                if char == '2':
                    if self.start is not None:
                        raise ValueError("Solo puede haber un punto de inicio ('2')")
                    self.start = (row_idx, col_idx)

                elif char == '3':
                    self.goals.append((row_idx, col_idx))

            self.grid.append(row)

        # Validaciones finales
        if self.start is None:
            raise ValueError("No hay punto de inicio ('2')")

        if len(self.goals) == 0:
            raise ValueError("Debe existir al menos una meta ('3')")

    def get_neighbors(self, position):
        """Devuelve los vecinos válidos respetando la jerarquía de movimientos."""
        row, col = position
        neighbors = []

        for dr, dc in self.directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < len(self.grid) and
                0 <= new_col < len(self.grid[0])):

                if self.grid[new_row][new_col] in ['0', '2', '3']:
                    neighbors.append((new_row, new_col))

        return neighbors

    def set_random_start(self):
        """Asigna un punto de partida aleatorio en un espacio libre."""
        free_spaces = []

        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == '0':
                    free_spaces.append((r, c))

        if free_spaces:
            self.start = random.choice(free_spaces)
            return self.start

        return None