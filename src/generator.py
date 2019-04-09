import random, opensimplex

def randInt():
    return int(str(random.random()).replace(".", ""))


seed = 5
b = 1
random.seed(seed)
#biomeNoise = opensimplex.OpenSimplex(seed*seed)
print(randInt())
localElevationNoise = opensimplex.OpenSimplex(randInt())
largeElevationNoise = opensimplex.OpenSimplex(randInt())





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

    def getNoise(self, noise, x, y, zoom):
        return noise.noise2d((x+self.x*Chunk.chunk_width)/zoom, (y+self.y*Chunk.chunk_height)/zoom)

    def generate(self):
        #Generates the chunk
        for y, column in enumerate(self.map):
            for x, tile in enumerate(self.map):
                localElevation = self.getNoise(localElevationNoise, x, y, 22.5) #Get the noise for this tile
                largeElevation = self.getNoise(largeElevationNoise, x, y, 150)
                elevation = largeElevation + 0.3 * localElevation
                if elevation < -.2:
                    #Make islands
                    if localElevation < .4:
                        self.map[y][x] = 2 #Ocean
                    elif localElevation < .5:
                        self.map[y][x] = 3 #Coast
                    elif localElevation <  .6:
                        self.map[y][x] = 4 #Sand
                    else:
                        self.map[y][x] = 1 #Land
                elif elevation < -.1:
                    if localElevation < .4:
                        self.map[y][x] = 2 #Ocean
                    elif localElevation < .5:
                        self.map[y][x] = 3 #Coast
                    else:
                        self.map[y][x] = 4 #Sand
                elif elevation < 0:
                    if localElevation < .4:
                        self.map[y][x] = 2 #Ocean
                    else:
                        self.map[y][x] = 3 #Coast
                    #self.map[y][x] = 7
                #Continents
                elif elevation < .05:
                    self.map[y][x] = 2 #Ocean
                elif elevation < .25:
                    self.map[y][x] = 3 #Coast
                elif elevation < .35:
                    self.map[y][x] = 4 #Sand
                elif elevation < .45:
                    self.map[y][x] = 1 #Land
                else: #We're on solid land
                    if localElevation < .4:
                        self.map[y][x] = 1 # Land
                    #mountains
                    elif localElevation < .6:
                        self.map[y][x] = 5
                    elif localElevation < .75:
                        self.map[y][x] = 6
                    else:
                        self.map[y][x] = 0



    def kill(self):
        #Call when you are done with the chunk
        del Chunk.chunks[(self.x, self.y)]




