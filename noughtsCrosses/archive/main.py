# Aiyush-G

import sys
import pygame
from settings import *
# LEVEL

class Game:

    # Sets up the game settings
    def __init__(self):
        pygame.init()

        # Display Surfaces, Clock
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        # LEVEL

        # Create Window Title
        pygame.display.set_caption("Aiyush Gupta - NEA")
    
    def run(self):
        # Gets all user inputs
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # The delta time is taken so that everything in the game can be frame rate independent and consistent on any device
            # Delta time is the time between the current and previous frame
            # Movement * Framerate * DeltaTime gives the same value for any framerate => & dt therefore, pixels per second
            # are the same across devices
            # Hence, no framerate is set in tick(HERE)
            delta_time = self.clock.tick() / 1000

            # Allows the entire level to be ran in a separate file to keep main.py decluttered & organised
            # self.level.run(delta_time)
            pygame.display.update()

if __name__ == "__main__":
    game= Game()
    game.run()