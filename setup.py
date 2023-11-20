import pygame

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
map_image = pygame.image.load("map.jpg")
map_image = pygame.transform.scale(map_image, (square_size, square_size))  # Ajusta el tamaño de la imagen
hero_image = pygame.image.load("heroe.png")
hero_image = pygame.transform.scale(hero_image, (20, 20))
witch_image = pygame.image.load("bruja.png")
witch_image = pygame.transform.scale(witch_image, (20, 20))

#Dado de 6 caras
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
    'vertex25': {'vertex23', 'vertex30'},
    'vertex26': {'vertex23', 'vertex27'},
    'vertex27': {'vertex26', 'vertex28'},
    'vertex28': {'vertex27', 'vertex30', 'vertex31'}, # Key vertex
    'vertex30': {'vertex25','vertex28', 'vertex32'},
    'vertex31': {'vertex28', 'vertex33', 'vertex32'},
    'vertex32': {'vertex19', 'vertex30', 'vertex31'},
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