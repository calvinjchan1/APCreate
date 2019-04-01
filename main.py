import pygame, sys, math
from src import generator, obj
from src.objs import player
#TODO: Variable tile size - zoom zoom

#Config
DEBUG = False
WINDOW_DIMENSIONS = (1000,600)
MAP_DIMENSIONS = (200, 200)
tileDict = {
    0:"grey",
    1:"green",
    2:"darkblue",
    3:"blue"
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
    global tileMap, screen, gameClock, plyr, tileSize, debugFont, deltaTime

    #Init pygame
    pygame.init()
    pygame.font.init()
    debugFont = pygame.font.SysFont('Comic Sans MS', 15)
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    gameClock = pygame.time.Clock()
    '''
    Map of tiles, where tile[y][x] is a certain integer
    '''
    tileSize = 32;
    tileMap = generator.createMap(MAP_DIMENSIONS)

    #Offset coordinates used to move the map
    global offsetX, offsetY
    offsetX = 0
    offsetY = 0

    #Init objects
    obj.init()
    deltaTime = 1

    #Make the player
    plyr = player.Player(1, 1)

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

            if event.type == pygame.KEYUP:
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

            if event.type == pygame.KEYDOWN:
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
                        tileSize-=8
                    elif(tileSize > 2):
                        tileSize -=2
                elif event.key == pygame.K_EQUALS:
                    if(tileSize<8):
                        tileSize+=2
                    elif(tileSize<64):
                        tileSize+=8

    def tick():
        for o in obj.objSet:
                o.onTick(deltaTime)

    def handleCamera():
        '''
        centers camera on the player
        '''
        global offsetX, offsetY
        offsetX = plyr.x-WINDOW_DIMENSIONS[0]/tileSize/2
        offsetY = plyr.y-WINDOW_DIMENSIONS[1]/tileSize/2

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
            for x in range(math.floor(max(offsetX, 0)), math.ceil(max(math.ceil(WINDOW_DIMENSIONS[0]/tileSize+offsetX), 0))):
                for y in range(math.floor(max(offsetY,0)), math.ceil(max(math.ceil(WINDOW_DIMENSIONS[1]/tileSize+offsetY),0))):
                    try:
                        drawTile(x-offsetX, y-offsetY, tileMap[y][x])
                    except IndexError:
                        pass

        def drawObjs():
            '''
            Draws all the objects
            '''
            for o in obj.objSet:
                o.draw(screen, offsetX, offsetY, tileSize)

        def drawText():
            '''
            Draws debug text
            '''
            textSurface = debugFont.render('Tile Size: '+ str(tileSize)+" FPS: "+str(gameClock.get_fps()), False, (255, 255, 255), (0, 0, 0))
            screen.blit(textSurface, (10, 10))

        handleCamera()
        drawBackground()
        drawMap()
        drawObjs()
        drawText()
        pygame.display.flip()

    def handleTime():
        global deltaTime
        deltaTime = gameClock.tick(70)

    #MAIN LOOP STARTS HERE
    while(True):
        handleTime()
        handleEvents()
        tick()
        draw()

def main():
    start()
    mainLoop()

main()
