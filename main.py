import pygame
import random
import sys
import heapq


# Inicializa Pygame
pygame.init()

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


# Configuración de la pantalla
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("La torre encantada")

# Tamaños y posiciones de los elementos
square_size = 330
margin = 40

# Carga la imagen (asegúrate de tener la imagen en la misma carpeta que tu script)
image = pygame.image.load("map.png")
image = pygame.transform.scale(image, (square_size, square_size))  # Ajusta el tamaño de la imagen

#Dado de 6 caras
dice = [
    (1, 3),
    (1, 1),
    (0, 2),
    (1, 3),
    (1, 1),
    (2, 0)
]

#Representación del grafo
map = {
    'vertex1': {'vertex2'}, #witch initial point
    'vertex2': {'vertex1', 'vertex3'},
    'vertex3': {'vertex2', 'vertex4'},
    'vertex4': {'vertex3', 'vertex5'},
    'vertex5': {'vertex4', 'vertex6'}, 
    'vertex6': {'vertex5', 'vertex7'}, # Initial point '1'
    'vertex7': {'vertex6', 'vertex8'},
    'vertex8': {'vertex9', 'vertex11', 'vertex13'}, # Initial point '3'; No se puede volver a 'vertex7'
    'vertex9': {'vertex8', 'vertex10'},
    'vertex10': {'vertex9', 'vertex12', 'vertex20'},
    'vertex11': {'vertex8', 'vertex12', 'vertex18', 'vertex19'},
    'vertex12': {'vertex10', 'vertex11'},
    'vertex13': {'vertex8', 'vertex14', 'vertex17'},
    'vertex14': {'vertex13', 'vertex15'},
    'vertex15': {'vertex14', 'vertex16', 'vertex39'},
    'vertex16': {'vertex15', 'vertex17'},
    'vertex17': {'vertex13', 'vertex16', 'vertex18', 'vertex40'},
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
    'vertex28': {'vertex27', 'vertex30', 'vertex31', 'vertex33'}, # Key vertex
    'vertex29': {'vertex25', 'vertex30'},
    'vertex30': {'vertex28', 'vertex29', 'vertex32'},
    'vertex31': {'vertex28', 'vertex33'},
    'vertex32': {'vertex19', 'vertex30'},
    'vertex33': {'vertex31', 'vertex34', 'vertex35', 'vertex28'},  # Key vertex
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

def dijkstra(graph, start, target_nodes):
    # Inicializa las estructuras de datos necesarias
    visited = set()  # Conjunto de nodos visitados
    distances = {node: float('inf') for node in graph}  # Distancias iniciales a todos los nodos como infinito
    distances[start] = 0  # Distancia al nodo de inicio es 0
    queue = [(0, start)]  # Cola de prioridad con (distancia, nodo)
    paths = {node: [] for node in graph}  # Almacena los caminos hacia cada nodo

    while queue:
        # Obtiene el nodo con la distancia más corta
        current_distance, current_node = heapq.heappop(queue)

        # Si ya visitamos este nodo, continuamos
        if current_node in visited:
            continue

        # Marca el nodo como visitado
        visited.add(current_node)

        # Explora los nodos vecinos
        for neighbor in graph[current_node]:
            # Suponemos un peso de 1 para todas las aristas en este grafo
            weight = 1
            distance = current_distance + weight

            # Actualiza la distancia si encontramos un camino más corto
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                paths[neighbor] = paths[current_node] + [current_node]  # Actualiza el camino
                heapq.heappush(queue, (distance, neighbor))

    result_paths = {node: paths[node] + [node] for node in target_nodes}

    return result_paths

# Ejemplo de uso
start_node = 'vertex1'
target_nodes = ['vertex24', 'vertex28', 'vertex33']  # Puedes ajustar los nodos de destino según tus necesidades
shortest_paths = dijkstra(map, start_node, target_nodes)
print(shortest_paths)


def move_hero(current_position, previous_position, map):
    # Simular el lanzamiento del dado y obtener el número rojo

    red_die_roll = random.choice(dice)

    for i in range(red_die_roll[0]):
        if len(map[current_position]) > 1:
            possible_moves = list(map[current_position])
            possible_moves.remove(previous_position)

            if current_position in ['vertex24', 'vertex28', 'vertex33']:
                if current_position == 'vertex24':
                    key_location = 'vertex24'
                elif current_position == 'vertex28':
                    key_location = 'vertex28'
                elif current_position == 'vertex33':
                    key_location = 'vertex33'

                if key_location == key_location:
                    print(f"El héroe ha encontrado la llave en {key_location}. ¡Gana el juego!")
                    return current_position
                else:
                    print(f"El héroe ha llegado a {current_position} pero no encontró la llave. Continúa.")
            else:
                print(f"El héroe se encuentra en {current_position}. Continúa moviéndose.")
            
            previous_position = current_position
            current_position = random.choice(possible_moves)
        else:
            print("El héroe ha llegado a una casilla sin opciones de movimiento. Juego terminado.")
            return current_position

    return current_position

# Ejemplo de uso
current_position = 'vertex1'
previous_position = 'vertex6'
new_position = move_hero(current_position, previous_position, map)


def move_witch(current_position, map):
    # Simular el lanzamiento del dado y obtener el número azul

    blue_die_roll = random.choice(dice)

    # Determinar las posibles ubicaciones de la llave
    possible_key_locations = ['vertex24', 'vertex28', 'vertex33']

    # Calcular los caminos más cortos desde la posición actual de la bruja a cada posible ubicación de la llave
    start_node = 'vertex1'
    target_nodes = ['vertex24', 'vertex28', 'vertex33'] 
    shortest_paths = dijkstra(map, start_node, target_nodes)
    for key_location in possible_key_locations:
        shortest_paths[key_location] = dijkstra(map, current_position, key_location)

    # Elegir la ubicación de la llave con el camino más corto
    key_location = min(possible_key_locations, key=lambda location: len(shortest_paths[location]))

    # Mover la bruja hacia la ubicación de la llave con el camino más corto
    if len(shortest_paths[key_location]) > blue_die_roll[0]:
        # Si el camino es más largo que el movimiento de la bruja, limita el movimiento al camino
        next_position = shortest_paths[key_location][blue_die_roll[0]]
    else:
        # Si el camino es igual o más corto que el movimiento de la bruja, llega a la ubicación de la llave
        next_position = key_location

    # Devolver la nueva posición de la bruja
    return next_position

# Ejemplo de uso
current_position = 'vertex1'
new_position = move_witch(current_position, map)

screen.fill(RUSSIAN_VIOLET)
pygame.display.flip()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
     # Dibuja los elementos en sus posiciones
    screen.blit(image, (margin, margin))  # Cuadrado superior izquierdo
    pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, ((margin*2 + square_size), margin, screen_width - (margin*3 + square_size), square_size))  # Rectángulo superior derecho
    pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (margin, margin * 2 + square_size, (screen_width-(margin*3))/2, screen_height-(margin*3+square_size)))  # left-down rectangle
    pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (margin*2+(screen_width-(margin*3))/2, margin * 2 + square_size, (screen_width-(margin*3))/2, screen_height-(margin*3+square_size)))  # Rectángulo inferior derecho

    # Actualiza la pantalla
    pygame.display.flip()

# Cierra Pygame
pygame.quit()
sys.exit()
