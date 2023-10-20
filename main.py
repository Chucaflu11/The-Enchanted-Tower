import pygame
import sys
import heapq


# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("La torre encantada")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RUSSIAN_VIOLET = (16, 0, 43)
RUSSIAN_VIOLET_LIGHT = (36, 0, 70)
PERSIAN_INDIGO = (60, 9, 108)
TEKHELET =  (90, 24, 154)
FRENCH_VIOLET = (123, 44, 191)
AMETHYST = (157, 78, 221)
HELIOTROPE = (199, 125, 255)
MAUVE = (224, 170, 255)
font = pygame.font.Font(None, 36)

map = {
    'vertex1': {'vertex2'}, #Witch initial point
    'vertex2': {'vertex3'},
    'vertex3': {'vertex4'},
    'vertex4': {'vertex5'},
    'vertex5': {'vertex6'},
    'vertex6': {'vertex7'}, #Initial point '1'
    'vertex7': {'vertex8'},
    'vertex8': {'vertex9', 'vertex11', 'vertex13'}, #Initial point '3'
    'vertex9': {'vertex8', 'vertex10'},
    'vertex10': {'vertex9', 'vertex12', 'vertex20'},
    'vertex11': {'vertex8', 'vertex12', 'vertex18', 'vertex19'},
    'vertex12': {'vertex10', 'vertex11'},
    'vertex13': {'vertex8', 'vertex14', 'vertex17'},
    'vertex14': {'vertex13', 'vertex15'},
    'vertex15': {'vertex14', 'vertex16', 'vertex39'},
    'vertex16': {'vertex15', 'vertex17'},
    'vertex17': {'vertex13','vertex16', 'vertex18', 'vertex40'},
    'vertex18': {'vertex11', 'vertex17'},
    'vertex19': {'vertex11', 'vertex20', 'vertex32', 'vertex43'},
    'vertex20': {'vertex10', 'vertex19', 'vertex21'},
    'vertex21': {'vertex20', 'vertex22'},
    'vertex22': {'vertex21', 'vertex23'},
    'vertex23': {'vertex22', 'vertex24', 'vertex25', 'vertex26'},
    'vertex24': {'vertex23'}, # Key vertex
    'vertex25': {'vertex23', 'vertex29'},
    'vertex26': {'vertex23', 'vertex27'},
    'vertex27': {'vertex26', 'vertex28'},
    'vertex28': {'vertex27', 'vertex30', 'vertex31'},   #key vertex
    'vertex29': {'vertex25', 'vertex30'},
    'vertex30': {'vertex28', 'vertex29', 'vertex32'},
    'vertex31': {'vertex28', 'vertex33'},
    'vertex32': {'vertex19', 'vertex30'},
    'vertex33': {'vertex31', 'vertex34', 'vertex35'},  #key vertex
    'vertex34': {'vertex33', 'vertex37', 'vertex42'},
    'vertex35': {'vertex33', 'vertex36'},
    'vertex36': {'vertex35', 'vertex37'},
    'vertex37': {'vertex34', 'vertex36', 'vertex38'},
    'vertex38': {'vertex37', 'vertex39'},
    'vertex39': {'vertex15', 'vertex38', 'vertex40', 'vertex41'},
    'vertex40': {'vertex17', 'vertex39'},
    'vertex41': {'vertex39', 'vertex42', 'vertex43'},
    'vertex42': {'vertex34', 'vertex41'},
    'vertex43': {'vertex19', 'vertex41'},
}


def dijkstra(graph, start):
    # Inicializa las estructuras de datos necesarias
    visited = set()  # Conjunto de nodos visitados
    distances = {node: float('inf') for node in graph}  # Distancias iniciales a todos los nodos como infinito
    distances[start] = 0  # Distancia al nodo de inicio es 0
    queue = [(0, start)]  # Cola de prioridad con (distancia, nodo)

    while queue:
        # Obtiene el nodo con la distancia más corta
        current_distance, current_node = heapq.heappop(queue)

        # Si ya visitamos este nodo, continuamos
        if current_node in visited:
            continue

        # Marca el nodo como visitado
        visited.add(current_node)

        # Explora los nodos vecinos
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # Actualiza la distancia si encontramos un camino más corto
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances

# Ejemplo de uso

start_node = 'vertex1'
shortest_distances = dijkstra(map, start_node)
print(shortest_distances)


# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Cierra Pygame
pygame.quit()
sys.exit()
