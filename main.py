import pygame, sys, math
from src import generator, obj, constants
from src.objs import player
import time
#TODO: Variable tile size - zoom zoom

#Config
DEBUG = False
WINDOW_DIMENSIONS = (1000,600)
MAP_DIMENSIONS = (200, 200)
tileDict = {
    0:"grey",
    1:"green",
    2:"darkblue",
    3:"blue",
    4:"#c6a664",#Sand
    5:"#585858",#Dark grey
    6:"#909090", #lighter grey
    7: "red"

}

def dprint(tag, msg):
    '''
    Used for printing debug messages that will only show up if
    the debug variabe is equal to the given tag
    '''
    if DEBUG == tag:
        print(msg)

def start():
    '''
    Run once at the beginning of the program
    '''
    global tileMap, screen, gameClock, plyr, tileSize, debugFont, deltaTime, oldTime, mapSurface

    #Init pygame
    pygame.init()
    pygame.font.init()
    debugFont = pygame.font.SysFont('Comic Sans MS', 15)
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    gameClock = pygame.time.Clock()
    '''
    Map of tiles, where tile[y][x] is a certain integer
    '''
    tileSize = 4
    #mapSurface = pygame.Surface(((player.Player.viewDist*2+1)*generator.Chunk.chunk_width*tileSize, (player.Player.viewDist*2+1)*generator.Chunk.chunk_height*tileSize))


    #Offset coordinates used to move the map
    global offsetX, offsetY
    offsetX = 0
    offsetY = 0

    #Deal with time
    oldTime = time.time()

    #Init objects
    obj.init()
    deltaTime = 1

    #Make the player
    plyr = player.Player(1, 1)

    #Init map stuff
    #updateMapSurf(True)
    zoom(0)
def updateMapSurf(deep = False):
    '''
    Updates map Surface.
    Use deep to reload all chuncks,
    otherwise the function will try to use it's memory
    of what chunks looked like before in order to save time
    '''
    global mapSurface, mapSurfLoc
    if deep:
        mapSurface = pygame.Surface(((player.Player.viewDist*2+1)*generator.Chunk.chunk_width*tileSize, (player.Player.viewDist*2+1)*generator.Chunk.chunk_height*tileSize))
    #Get the uppper left chunk, or our 0,0
    upper_left = None
    for chunkKey in generator.Chunk.chunks:
        if upper_left == None or (chunkKey[0]<upper_left[0] and chunkKey[1]<=upper_left[1]) or (chunkKey[1]<upper_left[1] and chunkKey[0]<=upper_left[0]):
            upper_left = chunkKey
    mapSurfLoc = (upper_left[0]*generator.Chunk.chunk_width, upper_left[1]*generator.Chunk.chunk_height)
    #Draw to surface
    for cy in range(player.Player.viewDist*2+1): #cy, cx short for chunk y chunk x
        for cx in range(player.Player.viewDist*2+1):
            chunk = generator.Chunk.chunks[(upper_left[0]+cx,upper_left[1]+cy)]
            if chunk.new or deep:
                chunk.mapSurf = pygame.Surface((generator.Chunk.chunk_width*tileSize, generator.Chunk.chunk_height*tileSize))
                for ty, column in enumerate(chunk.map): #ty, tx short for tile y tile x
                    for tx, tile in enumerate(column):
                        #dest = ((cx*generator.Chunk.chunk_width+tx)*tileSize, (cy*generator.Chunk.chunk_height+ty)*tileSize, tileSize, tileSize)
                        dest = (tx*tileSize, ty*tileSize, tileSize, tileSize)
                        chunk.mapSurf.fill(pygame.Color(tileDict[tile]), dest)
                chunk.new = False
            mapSurface.blit(chunk.mapSurf, (cx*generator.Chunk.chunk_width*tileSize, cy*generator.Chunk.chunk_height*tileSize))


def zoom (amount):
    global tileSize
    tileSize += amount
    if WINDOW_DIMENSIONS[0] > WINDOW_DIMENSIONS[1]:
        chunks_needed = math.ceil(WINDOW_DIMENSIONS[0]/tileSize/generator.Chunk.chunk_width)+1
    else:
        chunks_needed = math.ceil(WINDOW_DIMENSIONS[1]/tileSize/generator.Chunk.chunk_height)+1
    player.Player.viewDist = math.ceil(max(0, (chunks_needed-1)/2))
    plyr.updateChunks(player.Player.viewDist)
    updateMapSurf(True)

def mainLoop():
    '''
    The main loop of the program
    '''
    def handleEvents():
        global offsetX, offsetY, tileSize
        '''
        Deals with all of the user input
        '''

        for event in pygame.event.get():
            #Exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYUP:
                #Handle movement using arrow keys
                if event.key == pygame.K_LEFT:
                    #offsetX-=1
                    plyr.setMove("LEFT", False)
                elif event.key == pygame.K_RIGHT:
                    #offsetX+=1
                    plyr.setMove("RIGHT", False)
                elif event.key == pygame.K_UP:
                    #offsetY-=1
                    plyr.setMove("UP", False)
                elif event.key == pygame.K_DOWN:
                    #offsetY+=1
                    plyr.setMove("DOWN", False)

            elif event.type == pygame.KEYDOWN:
                #Handle movement using arrow keys
                if event.key == pygame.K_LEFT:
                    #offsetX-=1
                    plyr.setMove("LEFT", True)
                elif event.key == pygame.K_RIGHT:
                    #offsetX+=1
                    plyr.setMove("RIGHT", True)
                elif event.key == pygame.K_UP:
                    #offsetY-=1
                    plyr.setMove("UP", True)
                elif event.key == pygame.K_DOWN:
                    #offsetY+=1
                    plyr.setMove("DOWN", True)

                #Handle Zoom
                elif event.key == pygame.K_MINUS:
                    if(tileSize > 8):
                        zoom(-8)
                    elif(tileSize > 2):
                        zoom(-2)

                elif event.key == pygame.K_EQUALS:
                    if(tileSize<8):
                        zoom(2)
                    elif(tileSize<64):
                        zoom(8)
                    updateMapSurf(True)

            elif event.type == constants.EVENT_UPDATEMAPSURF:
                updateMapSurf()

    def tick():
        for o in obj.objSet:
                o.onTick(deltaTime)

    def handleCamera():
        '''
        centers camera on the player
        '''
        global offsetX, offsetY
        offsetX = plyr.x-WINDOW_DIMENSIONS[0]/tileSize/2+.5
        offsetY = plyr.y-WINDOW_DIMENSIONS[1]/tileSize/2+.5

    def draw():
        '''
        Handles draw everything to the screen
        '''
        def drawBackground():
            '''
            Draws a black background
            '''
            screen.fill(pygame.Color("black"))
        def drawMap():
            '''
            Draws the map to the screen
            '''
            def drawTile(x, y, tile):
                '''
                Draws a tile at the given coordinates
                '''

                screen.fill(pygame.Color(tileDict[tile]), (x*tileSize, y*tileSize, tileSize, tileSize))

            '''
            We only want to draw the tiles that are on the screen, as to avoid drawing one billion tiles every frame with large maps
            So we should loop through the tiles that should be on screen and try to draw them if they exist
            map[][offsetX] is left edge of screen
            map[][ceil(WINDOW_DIMENSIONS[0]/32+offsetX] is right edge of screen
            We need to cap at 0 so we don't go into negative index, because python takes that as seraching from end of list
            '''
            '''for x in range(math.floor(offsetX), math.ceil(math.ceil(WINDOW_DIMENSIONS[0]/tileSize+offsetX))):
                for y in range(math.floor(offsetY), math.ceil(math.ceil(WINDOW_DIMENSIONS[1]/tileSize+offsetY))):
                    try:
                        chunk_x = math.floor(x/generator.Chunk.chunk_width)
                        chunk_y = math.floor(y/generator.Chunk.chunk_height)
                        tile = generator.Chunk.chunks[(chunk_x, chunk_y)].map[y%generator.Chunk.chunk_height][x%generator.Chunk.chunk_width]
                        drawTile(x-offsetX, y-offsetY, tile)
                    except KeyError:
                        pass'''
            #updateMapSurf()
            screen.blit(mapSurface, ((mapSurfLoc[0]-offsetX)*tileSize,(mapSurfLoc[1]-offsetY)*tileSize))




        def drawObjs():
            '''
            Draws all the objects
            '''
            for o in obj.objSet:
                o.draw(screen, offsetX, offsetY, tileSize)

        def drawText():
            '''
            Draws debug text
            Does each line in lines from top to bottom
            '''
            lines = [
                'Tile Size: '+ str(tileSize),
                "FPS: "+str(gameClock.get_fps()),
                "X: " + str(plyr.x) + " Y: " + str(plyr.y)
            ]
            y = 10
            for line in lines:
                textSurface = debugFont.render(line, False, (255, 255, 255), (0, 0, 0))
                textHeight = textSurface.get_size()[1]
                screen.blit(textSurface, (10, y))
                y+=textHeight

        handleCamera()
        drawBackground()
        drawMap()
        drawObjs()
        drawText()
        pygame.display.flip()

    def handleTime():
        global deltaTime, oldTime
        gameClock.tick(70)
        deltaTime = (time.time()-oldTime)*1000
        oldTime = time.time()

    #MAIN LOOP STARTS HERE
    while(True):
        handleTime()
        handleEvents()
        tick()
        draw()

def main():
    start()
    mainLoop()

if __name__ == "__main__":
    main()
