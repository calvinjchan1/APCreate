import random, opensimplex

seed = 5
b = 1
#biomeNoise = opensimplex.OpenSimplex(seed*seed)
tileNoise = opensimplex.OpenSimplex(seed)


#Make each chunk a 32x 32 area?
class Chunk:

    chunk_width = 16
    chunk_height = 16
    chunks = {}

    def __init__(self, x, y):
        #Use chunk x, y not coordiantes. Ex chunk 0,0 1,0 not 0,0 32, 0
        self.x = x
        self.y = y
        #Initilize map
        self.map = [[0 for x in range(Chunk.chunk_width)]for y in range(Chunk.chunk_height)]
        self.generate()
        Chunk.chunks[(self.x, self.y)] = self
        self.new = True

    def generate(self):
        #Generates the chunk
        for y, column in enumerate(self.map):
            for x, tile in enumerate(self.map):
                #b = biomeNoise.noise2d((x+self.x*Chunk.chunk_width)/100, (y+self.y*Chunk.chunk_height)/100)
                n = tileNoise.noise2d((x+self.x*Chunk.chunk_width)/15, (y+self.y*Chunk.chunk_height)/15) #Get the noise for this tile
                if b <= 1: #Arcepeligo
                    if n < 0:
                        self.map[y][x] = 2 #Ocean
                    elif n < .2:
                        self.map[y][x] = 3 #Coast
                    elif n < 0.3:
                        self.map[y][x] = 4 #Beach
                    else:
                        self.map[y][x] = 1 #Land
                elif b < 0: #Coast Water
                    self.map[y][x] = 2
                elif b < .05: #Coast Water
                    self.map[y][x] = 3
                elif b < .1: #Big Coast
                    self.map[y][x] = 4
                else: #Continent
                    if n < .7:
                        self.map[y][x] = 1
                    elif n < .8:
                        self.map[y][x] = 5
                    else:
                        self.map[y][x] = 0


    def kill(self):
        #Call when you are done with the chunk
        del Chunk.chunks[(self.x, self.y)]




