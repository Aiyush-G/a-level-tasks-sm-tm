import pygame
from settings import * 

class Level:
    def __init__(self):

        # Show surface to player
        self.display_surface = pygame.display.get_surface()

        # Sprite Group
        