import random

def createMap(dimensions):
    '''
    This function returns a map list of dimensions given
    '''
    #Fill map with green
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
        

    map = []
    initMap(1)
    randomBlue()
    return map


    
