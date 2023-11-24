import pygame

pygame.init()

# Colour configuration
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

# Font configuration
font = pygame.font.Font(None, 22)
start_font = pygame.font.Font(None, 30)
i_font = pygame.font.Font(None, 18)


# Screen configuration
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("La torre encantada")

# Size of the map
square_size = 330
margin = 40

# Images
map_image = pygame.image.load("assets\\map.jpg")
map_image = pygame.transform.scale(map_image, (square_size, square_size)) # Resize image to fit the screen
hero_image = pygame.image.load("assets\\heroe.png")
hero_image = pygame.transform.scale(hero_image, (20, 20))
witch_image = pygame.image.load("assets\\bruja.png")
witch_image = pygame.transform.scale(witch_image, (20, 20))

# Dice values
dice = [
    (1, 3),
    (1, 1),
    (0, 2),
    (1, 3),
    (1, 1),
    (2, 0)
]

dice_red_moded = [
    (1, 4),
    (1, 2),
    (0, 3),
    (1, 4),
    (1, 2),
    (2, 1)
]

dice_blue_moded = [
    (2, 3),
    (2, 1),
    (1, 2),
    (2, 3),
    (2, 1),
    (3, 0)
]

# Map configuration (graph)
map = {
    'vertex1': {'vertex2'}, #witch initial point
    'vertex2': {'vertex1', 'vertex3'},
    'vertex3': {'vertex2', 'vertex4'},
    'vertex4': {'vertex3', 'vertex5'},
    'vertex5': {'vertex4', 'vertex6'}, 
    'vertex6': {'vertex5', 'vertex7'}, # Initial point '1'
    'vertex7': {'vertex6', 'vertex8'},
    'vertex8': {'vertex9', 'vertex11', 'vertex13'}, # Initial point '3'; Can't go to vertex 7
    'vertex9': {'vertex8', 'vertex10'},
    'vertex10': {'vertex9', 'vertex12', 'vertex20'},
    'vertex11': {'vertex8', 'vertex12', 'vertex18', 'vertex19'},
    'vertex12': {'vertex10', 'vertex11'},
    'vertex13': {'vertex8', 'vertex14', 'vertex17'},
    'vertex14': {'vertex13', 'vertex15'},
    'vertex15': {'vertex14', 'vertex16', 'vertex38'},
    'vertex16': {'vertex15', 'vertex17'},
    'vertex17': {'vertex13', 'vertex16', 'vertex18', 'vertex39'},
    'vertex18': {'vertex11', 'vertex17'},
    'vertex19': {'vertex11', 'vertex20', 'vertex31', 'vertex42'},
    'vertex20': {'vertex10', 'vertex19', 'vertex21'},
    'vertex21': {'vertex20', 'vertex22'},
    'vertex22': {'vertex21', 'vertex23'},
    'vertex23': {'vertex22', 'vertex24', 'vertex25', 'vertex26'},
    'vertex24': {'vertex23'}, # Key vertex
    'vertex25': {'vertex23', 'vertex29'},
    'vertex26': {'vertex23', 'vertex27'},
    'vertex27': {'vertex26', 'vertex28'},
    'vertex28': {'vertex27', 'vertex29', 'vertex30'}, # Key vertex
    'vertex29': {'vertex25','vertex28', 'vertex31'},
    'vertex30': {'vertex28', 'vertex31', 'vertex32'},
    'vertex31': {'vertex19', 'vertex29', 'vertex30'},
    'vertex32': {'vertex30', 'vertex33', 'vertex34'},  # Key vertex
    'vertex33': {'vertex32', 'vertex36', 'vertex41'},
    'vertex34': {'vertex32', 'vertex35'},
    'vertex35': {'vertex34', 'vertex36'},
    'vertex36': {'vertex33', 'vertex35', 'vertex37'},
    'vertex37': {'vertex36', 'vertex38'},
    'vertex38': {'vertex15', 'vertex37', 'vertex39', 'vertex40'},
    'vertex39': {'vertex17', 'vertex38'},
    'vertex40': {'vertex38', 'vertex41', 'vertex42'},
    'vertex41': {'vertex33', 'vertex40'},
    'vertex42': {'vertex19', 'vertex40'},
}