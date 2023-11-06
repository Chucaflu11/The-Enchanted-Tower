import pygame
import random
import sys
import heapq

import time


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
image = pygame.image.load("map.jpeg")
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
    'vertex28': {'vertex27', 'vertex30', 'vertex31'}, # Key vertex
    'vertex29': {'vertex25', 'vertex30'},
    'vertex30': {'vertex28', 'vertex29', 'vertex32'},
    'vertex31': {'vertex28', 'vertex33'},
    'vertex32': {'vertex19', 'vertex30'},
    'vertex33': {'vertex31', 'vertex34', 'vertex35'},  # Key vertex
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

def dijkstra(graph, start, target):
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

        # Si alcanzamos el nodo de destino, retornamos el camino más corto
        if current_node == target:
            return paths[current_node] + [current_node]

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

    # Si no se encontró un camino al nodo de destino, retornar una lista vacía
    return []


def move_hero(current_position, previous_position, map, roll):

    for i in range(roll):
        if len(map[current_position]) > 0:
            possible_moves = list(map[current_position])
            try:
                possible_moves.remove(previous_position)
            except ValueError:
                print("The previous_position is not in the list of possible moves.")

            #print("Possible moves: ", possible_moves)
            previous_position = current_position
            if(current_position == 'vertex24'):
                current_position = 'vertex23'
            else:
                current_position = random.choice(possible_moves)
        else:
            print("El héroe ha llegado a una casilla sin opciones de movimiento. Juego terminado.")
            return current_position

    return current_position



def move_witch(current_position, key_location, map, roll):
    # Calcular el camino más corto desde la posición actual de la bruja hasta la ubicación de la llave
    shortest_path = dijkstra(map, current_position, key_location)
    print(f"Camino más corto: {shortest_path}")

    # Obtener la distancia al nodo de destino (ubicación de la llave)
    distance_to_key = len(shortest_path) - 1

    # Determinar el movimiento de la bruja según el número azul del dado
    blue_movement = roll

    if blue_movement <= distance_to_key:
        # Si el número azul del dado es menor o igual a la distancia al nodo de destino, avanzar en el camino más corto
        new_position = shortest_path[blue_movement]
    else:
        # Si el número azul del dado es mayor que la distancia al nodo de destino, la bruja llega a la ubicación de la llave
        new_position = key_location

    return new_position


#Game loop
key = random.choice(['vertex24', 'vertex28', 'vertex33'])

hero_current_position = 'vertex6'
hero_previous_position = 'vertex5'

witch_current_position = 'vertex1'

def game_loop():
    global hero_current_position, hero_previous_position, witch_current_position

    if(hero_previous_position == 'vertex6' and hero_current_position != 'vertex7'): #Error handling (En primera iteración la posición previa queda igual que la actual por algún motivo)
        hero_previous_position = 'vertex5'
    
    roll = random.choice(dice)

    print(f"Dado: {roll}")
    hero_new_position = move_hero(hero_current_position, hero_previous_position, map, roll[1])
    print(f"Héroe: {hero_current_position} -> {hero_new_position}")


    witch_current_position = move_witch(witch_current_position, key, map, roll[0])
    print(f"Bruja: {witch_current_position}")

    if(roll[0] != 0):
        hero_previous_position = hero_current_position
        hero_current_position = hero_new_position
    if(hero_new_position == key):
        return 1
    elif(witch_current_position == key):
        return 0

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

    #game loop
    #Retorna 1 si gana el héroe, 0 si gana la bruja, 2 mientras se siga ejecutando.
    print("loop")
    game_loop()
    if(hero_current_position == key):
        running = False
        print("El héroe ha encontrado la llave. ¡Gana el juego!")
    elif(witch_current_position == key):
        running = False
        print("La bruja ha encontrado la llave. ¡Pierde el juego!")
    

# Cierra Pygame
pygame.quit()
sys.exit()
