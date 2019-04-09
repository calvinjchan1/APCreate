import random, opensimplex

seed = 5
noise = opensimplex.OpenSimplex(seed)


#Make each chunk a 32x 32 area?
class Chunk:

    chunk_width = 32
    chunk_height = 32
    chunks = {}

    def __init__(self, x, y):
        #Use chunk x, y not coordiantes. Ex chunk 0,0 1,0 not 0,0 32, 0
        self.x = x
        self.y = y
        #Initilize map
        self.map = [[0 for x in range(Chunk.chunk_width)]for y in range(Chunk.chunk_height)]
        self.generate()
        Chunk.chunks[(self.x, self.y)] = self

    def generate(self):
        #Generates the chunk
        for y, column in enumerate(self.map):
            for x, tile in enumerate(self.map):
                n = noise.noise2d((x+self.x*Chunk.chunk_width)/15, (y+self.y*Chunk.chunk_height)/15) #Get the noise for this tile
                if n < 0:
                    self.map[y][x] = 2 #Ocean
                elif n < .2:
                    self.map[y][x] = 3 #Coast
                elif n < 0.3:
                    self.map[y][x] = 4 #Beach
                else:
                    self.map[y][x] = 1 #Land

    def kill(self):
        #Call when you are done with the chunk
        del Chunk.chunks[(self.x, self.y)]




