from pdb import run
from turtle import st
from networkx import draw
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

font = pygame.font.Font(None, 22)
start_font = pygame.font.Font(None, 30)

g_iter = 10

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
                        pass
            else:
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
        self.moves += 1
        # Calcular el camino más corto desde la posición actual de la bruja hasta la ubicación de la llave
        shortest_path = dijkstra(map, self.current_position, key_location)
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

    def getMoves(self):
        move = self.moves
        self.moves = 0
        return move


class GameInstance():
    def __init__(self, dice, mod):
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
        self.dice = dice
        self.modded_game = mod

    def init(self):
        self.key = random.choice(['vertex24', 'vertex28', 'vertex33'])
        self.hero = Hero('vertex6', 'vertex5')
        self.witch = Witch('vertex1', 'vertex0')

    def compare_moves(self, won):
        hero_moves = self.hero.getMoves()
        witch_moves = self.witch.getMoves()
        if(won == 'hero'):
            if(self.hero_min_moves == 0):
                self.hero_min_moves = hero_moves
            elif(hero_moves < self.hero_min_moves):
                self.hero_min_moves = hero_moves
            if(hero_moves > self.hero_max_moves):
                self.hero_max_moves = hero_moves
        elif(won == 'witch'):
            if(self.witch_min_moves == 0):
                self.witch_min_moves = witch_moves
            elif(witch_moves < self.witch_min_moves):
                self.witch_min_moves = witch_moves
            if(witch_moves > self.witch_max_moves):
                self.witch_max_moves = witch_moves

    def draw_data(self):
        iteration_text = font.render("Iteración: " + str(self.iterations), True, WHITE)
        iteration_text_rect = iteration_text.get_rect(center=(2*margin, 0.5*margin))
        
        if(self.modded_game == 1):
            hero_moves_text = font.render("H: " + str(self.hero_min_moves) + " - " + str(self.hero_max_moves), True, WHITE)
            hero_moves_text_rect = hero_moves_text.get_rect(center=(square_size + margin*3, 0.5*margin))
            
            
            witch_moves_text = font.render("B: " + str(self.witch_min_moves) + " - " + str(self.witch_max_moves), True, WHITE)
            witch_moves_text_rect = witch_moves_text.get_rect(center=((square_size + margin*3) + hero_moves_text_rect.width + margin, 0.5*margin))

            if self.iterations > 0 and self.iterations <= g_iter:
                pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (0,0, screen_width, margin))
        
        elif(self.modded_game == 2):
            hero_moves_text = font.render("H: " + str(self.hero_min_moves) + " - " + str(self.hero_max_moves), True, WHITE)
            hero_moves_text_rect = hero_moves_text.get_rect(center=(2*margin, 1.5*margin+square_size))
            
            
            witch_moves_text = font.render("B: " + str(self.witch_min_moves) + " - " + str(self.witch_max_moves), True, WHITE)
            witch_moves_text_rect = witch_moves_text.get_rect(center=(2*margin+hero_moves_text_rect.width+margin, (1.5*margin+square_size)))

            if self.iterations > 0 and self.iterations <= g_iter:
                pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (0,margin+square_size, square_size, margin))
        
        elif(self.modded_game == 3):
            hero_moves_text = font.render("H: " + str(self.hero_min_moves) + " - " + str(self.hero_max_moves), True, WHITE)
            hero_moves_text_rect = hero_moves_text.get_rect(center=(((screen_width - 3*margin)/3)+2.5*margin, (1.5*margin+square_size)))
            
            
            witch_moves_text = font.render("B: " + str(self.witch_min_moves) + " - " + str(self.witch_max_moves), True, WHITE)
            witch_moves_text_rect = witch_moves_text.get_rect(center=((((screen_width - 3*margin)/3)+2.5*margin)+hero_moves_text_rect.width+margin, (1.5*margin+square_size)))

            if self.iterations > 0 and self.iterations <= g_iter:
                pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (square_size + 2*margin,margin+square_size, square_size, margin))
        
        elif(self.modded_game == 4):
            hero_moves_text = font.render("H: " + str(self.hero_min_moves) + " - " + str(self.hero_max_moves), True, WHITE)
            hero_moves_text_rect = hero_moves_text.get_rect(center=(((2*(screen_width - 3*margin)/3)+3.5*margin), (1.5*margin+square_size)))
            
            
            witch_moves_text = font.render("B: " + str(self.witch_min_moves) + " - " + str(self.witch_max_moves), True, WHITE)
            witch_moves_text_rect = witch_moves_text.get_rect(center=(((2*(screen_width - 3*margin)/3)+3.5*margin)+hero_moves_text_rect.width+margin, (1.5*margin+square_size)))

            if self.iterations > 0 and self.iterations <= g_iter:
                pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (2*square_size + 2*margin,margin+square_size, square_size, margin))

        else:
            return 0

        if self.iterations > 0 and self.iterations <= g_iter:
            pygame.draw.rect(screen, RUSSIAN_VIOLET_LIGHT, (0,0, square_size, margin))

        screen.blit(iteration_text, iteration_text_rect)
        screen.blit(hero_moves_text, hero_moves_text_rect)
        screen.blit(witch_moves_text, witch_moves_text_rect)

    def reset(self, won):
        self.iterations += 1
        self.compare_moves(won)

        self.draw_data()

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

        if(self.modded_game == 1):
            bar_width = (screen_width - (margin*3 + square_size)) - 200
            bar_height = square_size
            chart_surface = create_bar_chart_image(data, bar_width, bar_height)
            screen.blit(chart_surface, ((margin*2 + square_size), margin))
        elif(self.modded_game == 2):
            bar_width = (screen_width - 4 * margin) / 3
            bar_height = screen_height-(margin*3+square_size)
            chart_surface = create_bar_chart_image(data, bar_width, bar_height)
            screen.blit(chart_surface, (margin, (margin*2+square_size)))
        elif(self.modded_game == 3):
            bar_width = (screen_width - 4 * margin) / 3
            bar_height = screen_height-(margin*3+square_size)
            chart_surface = create_bar_chart_image(data, bar_width, bar_height)
            screen.blit(chart_surface, (2*margin+bar_width, margin * 2 + square_size))
        elif(self.modded_game == 4):
            bar_width = (screen_width - 4 * margin) / 3
            bar_height = screen_height-(margin*3+square_size)
            chart_surface = create_bar_chart_image(data, bar_width, bar_height)
            screen.blit(chart_surface, (3*margin + 2*bar_width, (margin*2+square_size)))
        
        pygame.display.flip()

    def distract_witch(self):
        distraction_prob = 0.7  # Por ejemplo, 20% de probabilidad de distraer a la bruja
        r_ = random.random()
        if r_ < distraction_prob:
            return True
        return False

    def game_movement(self):
        roll = random.choice(self.dice)
        self.draw_players()
        if(self.modded_game == 4):
            #Select some vertex to distract the witch, with the probability of the function itself
            if(not self.distract_witch() and not (self.hero.current_position == 'vertex15' or self.hero.current_position == 'vertex41' or self.hero.current_position == 'vertex25')):
                self.witch.current_position = self.witch.move(map, roll[0], self.key)
            
            self.hero_new_position = self.hero.move(map, roll[1], self.key)
            self.hero.previous_position = self.hero.current_position
            self.hero.current_position = self.hero_new_position
        else:
            hero_new_position = self.hero.move(map, roll[1], self.key)
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
            self.reset('hero')
        elif(self.witch.current_position == self.key):
            self.witch_wins += 1
            self.wins[self.total_games * 2] = self.hero_wins
            self.wins[self.total_games * 2 + 1] = self.witch_wins
            self.generate_graphs(self.wins)
            self.reset('witch')

    def game(self):
        if(self.game_running):
            self.game_loop()
            if(self.iterations == g_iter):
                self.reset_game_loop()

    def get_game_state(self):
        return self.game_running

def main(mod):
    global g_iter
    if(mod == 1):
        if(game.iterations <= g_iter):
            game.game()
        if(not game.get_game_state()):
            mod += 1
    if(mod == 2):
        if(game_mod.iterations <= g_iter):
            game_mod.game()
        if(not game_mod.get_game_state()):
            mod += 1
    if(mod == 3):
        if(game_mod2.iterations <= g_iter):
            game_mod2.game()
        if(not game_mod2.get_game_state()):
            mod += 1
    if(mod == 4):
        if(game_mod3.iterations <= g_iter):
            game_mod3.game()
        if(not game_mod3.get_game_state()):
            mod += 1


    return mod


# Inicializa la ventana
if __name__ == "__main__":
    screen.fill(RUSSIAN_VIOLET_LIGHT)
    screen.blit(map_image, (margin, margin))
    pygame.display.flip()

    mod = 1
    #Juego normal
    game = GameInstance(dice, 1)
    game.init()
    #Juego modificado dados azules
    game_mod = GameInstance(dice_blue_moded, 2)
    game_mod.init()
    #Juego modificado dados rojos
    game_mod2 = GameInstance(dice_red_moded, 3)
    game_mod2.init()
    #Juego modificado distracción
    game_mod3 = GameInstance(dice, 4)
    game_mod3.init()
    # Bucle principal
    running = True
    playing = False
    text = ""

    start_button = pygame.Rect(screen_width-200, 3*margin, 145, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not playing:
                if event.key == pygame.K_RETURN:
                    try:
                        # Intentar convertir la entrada a un número
                        g_iter = int(text)
                        #text = ""
                    except ValueError:
                        #text = ""
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    # Eliminar el último carácter
                    text = text[:-1]
                else:
                    # Agregar el carácter ingresado al texto
                    text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos) and not playing:
                    try:
                        # Intentar convertir la entrada a un número
                        g_iter = int(text)
                        #text = ""
                    except ValueError:
                        #text = ""
                        pass
                    playing = True

        pygame.draw.rect(screen, FRENCH_VIOLET, (screen_width - (margin + 180), margin, 180, square_size))  # Rectángulo superior derecho
        pygame.draw.rect(screen, HELIOTROPE, start_button)
        start = start_font.render("Iniciar", True, WHITE)
        text_rect = start.get_rect(center=(screen_width - (margin + 90), 3*margin+20))
        screen.blit(start, text_rect)
        # Renderizar el texto en el centro del rectángulo
        input_text = font.render(text, True, WHITE)
        text_rect = input_text.get_rect(center=(screen_width - (margin + 90), 2*margin))
        screen.blit(input_text, text_rect)

        if(playing):
            mod = main(mod)

        pygame.display.flip()

# Cierra Pygame
pygame.quit()
sys.exit()