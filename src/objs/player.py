'''
Contains the class for the player object
'''
import pygame
from src import obj

#CONFIG
MOVE_INTERVAL = 200 #How many miliseconds to wait between movements when key is held down

class Player(obj.Obj):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dirTimes = [[False,0],[False,0],[False,0],[False, 0]] #UP, DOWN, LEFT, RIGHT

    def draw(self, screen, offsetX, offsetY, tileSize):
        screen.fill(pygame.Color("orange"), (self.x*tileSize+tileSize/4-offsetX*tileSize, self.y*tileSize+tileSize/4-offsetY*tileSize, tileSize/2, tileSize/2))

    def onTick(self, deltaTime):
        for index, direction in enumerate(self.dirTimes):
            if direction[0]:
                direction[1]+=deltaTime
                if direction[1] > MOVE_INTERVAL:
                    if index == 0:
                        self.move("UP")
                    elif index == 1:
                        self.move("DOWN")
                    elif index == 2:
                        self.move("LEFT")
                    elif index == 3:
                        self.move("RIGHT")
                    direction[1] = direction[1]%MOVE_INTERVAL

    def setMove(self, direction, start):
        '''
        Used to start or stop moving the player in the given direction
        Set start to True if movement is starting,
        false if stopping
        '''
        if start: self.move(direction)
        if direction == "UP":
            self.dirTimes[0] = [start, 0]
        if direction == "DOWN":
            self.dirTimes[1] = [start, 0]
        if direction == "LEFT":
            self.dirTimes[2] = [start, 0]
        if direction == "RIGHT":
            self.dirTimes[3] = [start, 0]

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
