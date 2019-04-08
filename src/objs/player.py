'''
Contains the class for the player object
'''
import pygame, math
from src import generator
from src import obj


#CONFIG
MOVE_INTERVAL = 200 #How many miliseconds to wait between movements when key is held down

class Player(obj.Obj):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dirTimes = [False, False, False, False] #UP, DOWN, LEFT, RIGHT
        self.dirTimer = 0
        self.updateChunks(1)

    def draw(self, screen, offsetX, offsetY, tileSize):
        #Draw an orange triangle in the middle of the tile
        screen.fill(pygame.Color("orange"), (self.x*tileSize+tileSize/4-offsetX*tileSize, self.y*tileSize+tileSize/4-offsetY*tileSize, tileSize/2, tileSize/2))

    def onTick(self, deltaTime):
        #Hanle automove when keys are held down
        self.dirTimer += deltaTime
        if self.dirTimer > MOVE_INTERVAL:
            for index, direction in enumerate(self.dirTimes):
                if direction:
                    if index == 0:
                        self.move("UP")
                    elif index == 1:
                        self.move("DOWN")
                    elif index == 2:
                        self.move("LEFT")
                    elif index == 3:
                        self.move("RIGHT")
        self.dirTimer = self.dirTimer%MOVE_INTERVAL

    def setMove(self, direction, start):
        '''
        Used to start or stop moving the player in the given direction
        Set start to True if movement is starting,
        false if stopping
        '''
        if not True in self.dirTimes or not False in self.dirTimes:
            self.dirTimer = 0
        if start: self.move(direction)
        if direction == "UP":
            self.dirTimes[0] = start
        if direction == "DOWN":
            self.dirTimes[1] = start
        if direction == "LEFT":
            self.dirTimes[2] = start
        if direction == "RIGHT":
            self.dirTimes[3] = start

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
        self.updateChunks(1)

    def updateChunks(self, distance):
        '''
        Updates the chunks around the player, loading new ones that are close
        and unloading far away ones
        '''
        chunk_x = math.floor(self.x/generator.Chunk.chunk_width)
        chunk_y = math.floor(self.y/generator.Chunk.chunk_height)
        tempChunks = {}
        for x in range(chunk_x-distance, chunk_x+1+distance):
            for y in range(chunk_y-distance, chunk_y+1+distance):
                try:
                    tempChunks[(x, y)] = generator.Chunk.chunks[(x, y)]
                except KeyError:
                    tempChunks[(x, y)] = generator.Chunk(x, y)
        generator.Chunk.chunks = tempChunks
