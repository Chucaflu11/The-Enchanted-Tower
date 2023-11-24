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



g_iter = 10

def dijkstra(graph, start, target, blocked_node=None):
    visited = set()  
    distances = {node: float('inf') for node in graph}  # Set all distances to infinity initially
    distances[start] = 0  
    queue = [(0, start)]  
    paths = {node: [] for node in graph}  

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == target:
            return paths[current_node] + [current_node]

        for neighbor in graph[current_node]:
            #assuming all edges have weight = 1 (Not completely necessary)
            weight = 1
            distance = current_distance + weight

            if neighbor == blocked_node:
                continue

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                paths[neighbor] = paths[current_node] + [current_node]  
                heapq.heappush(queue, (distance, neighbor)) 

    # If no path is found
    return []


class Hero():
    def __init__(self, start_position, start_previous_position):
        self.current_position = start_position
        self.previous_position = start_previous_position
        self.moves = 0

    def move(self, map, roll, key_location=None):
        # Move the hero according to the red dice roll
        for i in range(roll):
            # No need to move if the hero has already reached the key
            if(self.current_position == key_location):
                return self.current_position

            self.moves += 1
            # Check if the hero is in a vertex with more than one possible move
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
                # If there are no possible moves, the hero stays in the same position
                return self.current_position
        return self.current_position

    def getMoves(self):
        # Count and reset the number of moves
        move = self.moves
        self.moves = 0
        return move

class Witch():
    def __init__(self, start_position, start_previous_position):
        self.current_position = start_position
        self.previous_position = start_previous_position
        self.moves = 0

    def move(self, map, roll, key_location):
        # Move the witch according to the blue dice roll
        # No need to move if the witch has already reached the key
        if(self.current_position == key_location):
            return self.current_position
        
        self.moves += 1

        shortest_path = dijkstra(map, self.current_position, key_location)

        distance_to_key = len(shortest_path) - 1

        blue_movement = roll
        # Check if the witch can move more than the blue dice roll
        if blue_movement <= distance_to_key:
            new_position = shortest_path[blue_movement]
        else:
            # If the witch can't move that much, it will move to the last vertex of the shortest path
            new_position = key_location

        return new_position

    def getMoves(self):
        # Count and reset the number of moves
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
        self.key = random.choice(['vertex24', 'vertex28', 'vertex32'])
        self.hero = Hero('vertex6', 'vertex5')
        self.witch = Witch('vertex1', 'vertex0')

    def compare_moves(self, won):
        # Get the moves for both hero and witch only once
        hero_moves = self.hero.getMoves()
        witch_moves = self.witch.getMoves()

        # Update the min and max moves for the hero or witch based on who won
        if won == 'hero':
            self.hero_min_moves = min(self.hero_min_moves, hero_moves) if self.hero_min_moves else hero_moves
            self.hero_max_moves = max(self.hero_max_moves, hero_moves)
        elif won == 'witch':
            self.witch_min_moves = min(self.witch_min_moves, witch_moves) if self.witch_min_moves else witch_moves
            self.witch_max_moves = max(self.witch_max_moves, witch_moves)

    def draw_data(self):
        # Draw the data for the current iteration
        # Modded game means that the data will be drawn in a different spot, depending on the modifcation applied
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

        self.key = random.choice(['vertex24', 'vertex28', 'vertex32'])

        positions = {
            0: ('vertex6', 'vertex5'),
            1: ('vertex7', 'vertex6'),
            2: ('vertex8', 'vertex7')
        }

        # Update hero's current and previous positions based on total games
        if self.total_games in positions:
            self.hero.current_position, self.hero.previous_position = positions[self.total_games]

        self.witch.current_position = 'vertex1'
    
    def draw_players(self):
        screen.blit(map_image, (margin, margin))  # Limpiar mapa
        screen.blit(hero_image, coordinates[self.hero.current_position])
        screen.blit(witch_image, coordinates[self.witch.current_position])
        pygame.display.flip()

    def generate_graphs(self, data):
        if self.modded_game == 1:
            bar_width = (screen_width - (margin*3 + square_size)) - 200
            chart_surface = create_bar_chart_image(data, bar_width, square_size)
            screen.blit(chart_surface, ((margin*2 + square_size), margin))
        elif self.modded_game in [2, 3, 4]:
            bar_width = (screen_width - 4 * margin) / 3
            bar_height = screen_height-(margin*3+square_size)
            chart_surface = create_bar_chart_image(data, bar_width, bar_height)
            positions = {
                2: (margin, (margin*2+square_size)),
                3: (2*margin+bar_width, margin * 2 + square_size),
                4: (3*margin + 2*bar_width, (margin*2+square_size))
            }
            screen.blit(chart_surface, positions[self.modded_game])

        pygame.display.flip()

    def distract_witch(self):
        distraction_prob = 0.7 # Probability of the witch being distracted (Mod 4)
        r_ = random.random()
        if r_ < distraction_prob:
            return True
        return False

    def game_movement(self):
        roll = random.choice(self.dice)
        self.draw_players()
        if(self.modded_game == 4):
            #Select green vertex to distract the witch, with the probability of the function itself
            distraction = ('vertex10', 'vertex11', 'vertex15', 'vertex17', 'vertex22', 'vertex24', 'vertex26', 'vertex28', 'vertex31', 'vertex32', 'vertex35', 'vertex41')
            if(not self.distract_witch() and not(self.hero.current_position in distraction)):
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

        # Total games is used to determine the hero's starting position
        if(self.total_games == 2):
            self.game_running = False
        else:
            self.total_games += 1

    # wins are stored in the following order to generate the graphs:
    def game_loop(self):
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
        self.game_movement()

    def game(self):
        if(self.game_running):
            self.game_loop()
            if(self.iterations == g_iter):
                self.reset_game_loop()

    def get_game_state(self):
        return self.game_running

def main(mod):
    global g_iter
    # Mod 1: normal game
    if(mod == 1):
        if(game.iterations <= g_iter):
            game.game()
        if(not game.get_game_state()):
            mod += 1
    # Mod 2: blue dice modification
    if(mod == 2):
        if(game_mod.iterations <= g_iter):
            game_mod.game()
        if(not game_mod.get_game_state()):
            mod += 1
    # Mod 3: red dice modification
    if(mod == 3):
        if(game_mod2.iterations <= g_iter):
            game_mod2.game()
        if(not game_mod2.get_game_state()):
            mod += 1
    # Mod 4: distraction modification
    if(mod == 4):
        if(game_mod3.iterations <= g_iter):
            game_mod3.game()
        if(not game_mod3.get_game_state()):
            global playing
            playing = False
            mod = 1

    return mod


if __name__ == "__main__":
    screen.fill(RUSSIAN_VIOLET_LIGHT)
    screen.blit(map_image, (margin, margin))
    pygame.display.flip()

    mod = 1
    # Normal game
    game = GameInstance(dice, 1)
    game.init()
    # Modified game with blue dice
    game_mod = GameInstance(dice_blue_moded, 2)
    game_mod.init()
    # Modified game with red dice
    game_mod2 = GameInstance(dice_red_moded, 3)
    game_mod2.init()
    # Modified game with distraction
    game_mod3 = GameInstance(dice, 4)
    game_mod3.init()
    # Main loop
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
                        # Try to convert the input to a number
                        g_iter = int(text)
                    except ValueError:
                        text = ""
                    playing = True
                elif event.key == pygame.K_BACKSPACE:
                    # Delete the last character from the text
                    text = text[:-1]
                else:
                    # Add the character to the text
                    text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos) and not playing:
                    try:
                        # Try to convert the input to a number
                        g_iter = int(text)
                    except ValueError:
                        text = ""
                    playing = True

        # Draw the start button
        pygame.draw.rect(screen, FRENCH_VIOLET, (screen_width - (margin + 180), margin, 180, square_size))
        pygame.draw.rect(screen, HELIOTROPE, start_button)
        start = start_font.render("Iniciar", True, WHITE)
        text_rect = start.get_rect(center=(screen_width - (margin + 90), 3*margin+20))
        screen.blit(start, text_rect)

        # Draw text
        important = i_font.render("Importante: Leer README!", True, WHITE)
        text_rect = important.get_rect(center=(screen_width - (margin + 90), 6*margin))
        pygame.draw.rect(screen, FRENCH_VIOLET, text_rect)
        screen.blit(important, text_rect)

        # Draw the input text
        input_text = font.render(text, True, WHITE)
        text_rect = input_text.get_rect(center=(screen_width - (margin + 90), 2*margin))
        screen.blit(input_text, text_rect)

        if(playing):
            mod = main(mod)

        pygame.display.flip()

pygame.quit()
sys.exit()