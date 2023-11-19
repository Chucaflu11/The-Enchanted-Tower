import pygame
import random
import sys
import heapq

from coordinates import coordinates
from charts import create_bar_chart_image
from setup import *


# Inicializa Pygame
pygame.init()

clock = pygame.time.Clock()

game_running = True
total_games = 1

# Camino de la bruja
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
                heapq.heappush(queue, (distance, neighbor)) # type: ignore

    # Si no se encontró un camino al nodo de destino, retornar una lista vacía
    return []

class Hero():
    def __init__(self, start_position, start_previous_position):
        self.current_position = start_position
        self.previous_position = start_previous_position
        self.moves = 0

    def move(self, map, roll, key_location=None):
        for i in range(roll):
            if(self.current_position == key_location):
                return self.current_position
            self.moves += 1
            if len(map[self.current_position]) > 0:
                possible_moves = list(map[self.current_position])
                try:
                    possible_moves.remove(self.previous_position)
                except ValueError:
                    pass

                self.previous_position = self.current_position
                if(self.current_position == 'vertex24'):
                    self.current_position = 'vertex23'
                else:
                    try:
                        self.current_position = random.choice(possible_moves)
                    except IndexError:
                        return self.current_position
            else:
                print("El héroe ha llegado a una casilla sin opciones de movimiento. Juego terminado.")
                return self.current_position
        return self.current_position

    def getMoves(self):
        move = self.moves
        self.moves = 0
        return move

class Witch():
    def __init__(self, start_position, start_previous_position):
        self.current_position = start_position
        self.previous_position = start_previous_position
        self.moves = 0

    def move(self, map, roll, key_location):
        if(self.current_position == key_location):
            return self.current_position
        # Calcular el camino más corto desde la posición actual de la bruja hasta la ubicación de la llave
        shortest_path = dijkstra(map, self.current_position, key_location)

        # Obtener la distancia al nodo de destino (ubicación de la llave)
        distance_to_key = len(shortest_path) - 1

        # Determinar el movimiento de la bruja según el número azul del dado
        blue_movement = roll

        if blue_movement <= distance_to_key:
            # Si el número azul del dado es menor o igual a la distancia al nodo de destino, avanzar en el camino más corto
            new_position = shortest_path[blue_movement]
            self.moves += blue_movement
        else:
            # Si el número azul del dado es mayor que la distancia al nodo de destino, la bruja llega a la ubicación de la llave
            new_position = key_location
            self.moves += distance_to_key

        return new_position

    def getMoves(self):
        move = self.moves
        self.moves = 0
        return move


class GameInstance():
    def __init__(self):
        self.iterations = 0
        self.hero_wins = 0
        self.hero_min_moves = 0
        self.hero_max_moves = 0
        self.witch_wins = 0
        self.witch_min_moves = 0
        self.witch_max_moves = 0
        self.wins = [0, 0, 0, 0, 0, 0]
        self.total_games = 0
        self.game_running = True

    def init(self):
        self.key = random.choice(['vertex24', 'vertex28', 'vertex33'])
        self.hero = Hero('vertex6', 'vertex5')
        self.witch = Hero('vertex1', 'vertex0')

    def compare_moves(self):
        hero_moves = self.hero.getMoves()
        witch_moves = self.witch.getMoves()
        if(self.hero_min_moves == 0):
            self.hero_min_moves = hero_moves
        elif(hero_moves < self.hero_min_moves):
            self.hero_min_moves = hero_moves
        if(hero_moves > self.hero_max_moves):
            self.hero_max_moves = hero_moves
        if(self.witch_min_moves == 0):
            self.witch_min_moves = witch_moves
        elif(witch_moves < self.witch_min_moves):
            self.witch_min_moves = witch_moves
        if(witch_moves > self.witch_max_moves):
            self.witch_max_moves = witch_moves

    def reset(self):
        self.iterations += 1
        self.compare_moves()
        self.key = random.choice(['vertex24', 'vertex28', 'vertex33'])
        if(self.total_games == 0):
            self.hero.current_position = 'vertex6'
            self.hero.previous_position = 'vertex5'
        elif(self.total_games == 1):
            self.hero.current_position = 'vertex7'
            self.hero.previous_position = 'vertex6'
        elif(self.total_games == 2):
            self.hero.current_position = 'vertex8'
            self.hero.previous_position = 'vertex7'

        self.witch.current_position = 'vertex1'

    def draw_players(self):
        screen.blit(map_image, (margin, margin))  # Limpiar mapa
        screen.blit(hero_image, coordinates[self.hero.current_position])
        screen.blit(witch_image, coordinates[self.witch.current_position])
        pygame.display.flip()

    def generate_graphs(self, data):
        pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, ((margin*2 + square_size), margin, screen_width - (margin*3 + square_size), square_size))  # Rectángulo superior derecho
        #Size of the image for the graphics
        bar_width = (screen_width - (margin*3 + square_size)) - 200
        bar_height = square_size

        chart_surface = create_bar_chart_image(data, bar_width, bar_height)
        screen.blit(chart_surface, ((margin*2 + square_size), margin))
        pygame.display.flip()

    def game_movement(self):
        roll = random.choice(dice)

        self.draw_players()
        hero_new_position = self.hero.move(map, roll[1])
        self.hero.previous_position = self.hero.current_position
        self.hero.current_position = hero_new_position

        self.witch.current_position = self.witch.move(map, roll[0], self.key)

    
    def reset_game_loop(self):
        self.iterations = 0
        self.hero_wins = 0
        self.hero_min_moves = 0
        self.hero_max_moves = 0
        self.witch_wins = 0
        self.witch_min_moves = 0
        self.witch_max_moves = 0
        if(self.total_games == 2):
            self.game_running = False
        else:
            self.total_games += 1

    def game_loop(self):
        self.game_movement()
        if(self.hero.current_position == self.key):
            self.hero_wins += 1
            self.wins[self.total_games * 2] = self.hero_wins
            self.wins[self.total_games * 2 + 1] = self.witch_wins
            self.generate_graphs(self.wins)
            self.reset()
        elif(self.witch.current_position == self.key):
            self.witch_wins += 1
            self.wins[self.total_games * 2] = self.hero_wins
            self.wins[self.total_games * 2 + 1] = self.witch_wins
            self.generate_graphs(self.wins)
            self.reset()

    def game(self):
        if(self.game_running):
            self.game_loop()
            if(self.iterations == 50):
                self.reset_game_loop()

# Dibuja los elementos en sus posiciones
screen.blit(map_image, (margin, margin))  # Cuadrado superior izquierdo
#pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, ((margin*2 + square_size), margin, screen_width - (margin*3 + square_size), square_size))  # Rectángulo superior derecho
pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (margin, margin * 2 + square_size, (screen_width-(margin*3))/2, screen_height-(margin*3+square_size)))  # left-down rectangle
pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (margin*2+(screen_width-(margin*3))/2, margin * 2 + square_size, (screen_width-(margin*3))/2, screen_height-(margin*3+square_size)))  # Rectángulo inferior derecho
pygame.display.flip()

# Bucle principal
running = True
game = GameInstance()
game.init()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if(game.iterations <= 50):
        game.game()

# Cierra Pygame
pygame.quit()
sys.exit()