"""
Módulo de Heurísticas

Referencias (APA 7ma ed.):
Russell, S. J., & Norvig, P. (2021). Artificial Intelligence: A Modern Approach (4th ed.). Pearson.
"""
import math

def euclidean(p1, p2):
    """Calcula la distancia en línea recta entre dos puntos."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def manhattan(p1, p2):
    """Calcula la suma de las diferencias absolutas de sus coordenadas cartesianas."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])