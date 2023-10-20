import pygame
import sys

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

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Cierra Pygame
pygame.quit()
sys.exit()
