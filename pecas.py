import os
import pygame
from pathlib import Path
from constants import *


class Domino(pygame.sprite.Sprite):
    def __init__(self, first, second, x, y):
        super().__init__()
        self.first = first
        self.second = second
        self.x = x
        self.y = y
        actual_path = Path(os.getcwd())
        image_path = actual_path / 'images'
        load_image_1 = "{}".format(image_path / "{}.png".format(self.first))
        load_image_2 = "{}".format(image_path / "{}.png".format(self.second))
        self.square1 = pygame.image.load(load_image_1).convert()
        self.square2 = pygame.image.load(load_image_2).convert()
        

    def __repr__(self):
        return "[{}|{}]" .format(self.first, self.second)

    def __contains__(self, key):
        return key == self.first or key == self.second

    def __del__(self):
        del self  

    def invert(self):
        self.first, self.second = self.second, self.first

    def is_startable(self):
        return self.first == 6 and self.second == 6
    
    def is_removable(self):
        return self.first == 0 and self.second == 0
    
    def draw(self, screen):
        screen.blit(self.square1, (self.x, self.y))
        screen.blit(self.square2, (self.x, self.y+34))
        
