'''
Contains the class for the player object
'''
import pygame
from src import obj

class Player(obj.Obj):
    def __init__(self, x, y):
        super().__init__(x, y)
    def draw(self, screen, offsetX, offsetY, tileSize):
        screen.fill(pygame.Color("orange"), (self.x*tileSize+tileSize/4-offsetX*tileSize, self.y*tileSize+tileSize/4-offsetY*tileSize, tileSize/2, tileSize/2))

    def move(self, direction):
        direction = direction.upper() #Conver to caps as to no be case-sensitive
        if direction == "UP":
            self.y-=1
        elif direction == "DOWN":
            self.y+=1
        elif direction == "RIGHT":
            self.x+=1
        elif direction == "LEFT":
            self.x-=1
