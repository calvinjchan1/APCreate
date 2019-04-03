import random

seed = 5

def createMap(dimensions):
    '''
    This function returns a map list of dimensions given
    '''
    def initMap(num):
        '''
        Initalizes the map making it the correct length
        and makes all tiles the given num
        '''
        for y in range(dimensions[1]):
            column = []
            for x in range(dimensions[0]):
                column.append(num)
            map.append(column)

    def onEachTile(function):
        '''
        Decorator that runs the given functions for each tile
        x and y are passed as the first 2 parameters to the function,
        and when actually calling the function should not be used
        example:

        @onEachTile
        def exampleFunc(x, y, num):
            map[y][x] = num
        should be called as

        exampleFunc(num)
        '''
        def wrapper(*args, **kwargs):
            for y in range(dimensions[1]):
                for x in range(dimensions[0]):
                    function(x, y, *args, **kwargs)
        return wrapper

    @onEachTile
    def randomBlue(x, y):
        if(bool(random.getrandbits(1))):
            map[y][x] = 2

    @onEachTile
    def makeIslands(x, y):
        def island(x, y, count):
            if(map[y][x] == 1):
                return
            map[y][x] = 1
            if random.random()<count/1:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        try:
                            island(x+i, y+j, count-0.1)
                        except IndexError:
                            pass
                        #if random.random() < .4 if 4 else .1: map[y][x] == 4 FIX ME
        if random.random()<0.005:
            island(x, y, 0.8)

    @onEachTile
    def makeCoast(x, y):
        if map[y][x] == 1:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if map[y+i][x+j] == 2:
                            map[y+i][x+j] = 3
                    except IndexError:
                        pass

    map = []
    initMap(2)
    makeIslands()
    makeCoast()
    return map

def uNum(x, y):
    '''
    Returns a number that will be different from every other x
    and y given
    X and Y should both be integers
    '''
    def convert(num):
        #Converts number into unique string of numbers
        neg = False
        if num<0:
            neg = True
        val = str(bin(abs(num)))[2:]
        val = "2" if neg else "3" + val
        return val

    print(convert(5))


#Make each chunk a 32x 32 area?
class chunk:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map = []
        random.seed(seed*self.x*self.y)
        for y in range(32):
            for x in range(32):
                self.map[y][x] = 1


uNum(0,0)