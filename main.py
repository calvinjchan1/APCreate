import pygame, sys

#Config
WINDOW_DIMENSIONS = (640,450)
tileDict = {
    0:"grey",
    1:"green",
    2:"blue"
}

def start():
    '''
    Run once at the beginning of the program
    '''
    global tileMap, screen
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    '''
    Map of tiles, where tile[y][x] is a certain integer
    '''
    tileMap = [
                [1, 1, 1, 2, 2, 1],
                [1, 0, 1, 2, 1, 1],
                [1, 1, 1, 2, 2, 2]
    ]
    #Offset coordinates used to move the map
    global offsetX, offsetY
    offsetX = 0
    offsetY = 0

def mainLoop():
    '''
    The main loop of the program
    '''
    def handleEvents():
        global offsetX, offsetY
        '''
        Deals with all of the user input
        '''
        
        for event in pygame.event.get():
            #Exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #Handle movement using arrow keys
                if event.key == pygame.K_LEFT:
                    offsetX+=1
                if event.key == pygame.K_RIGHT:
                    offsetX-=1
                if event.key == pygame.K_UP:
                    offsetY+=1
                if event.key == pygame.K_DOWN:
                    offsetY-=1
            
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
                screen.fill(pygame.Color(tileDict[tile]), (x*32, y*32, 32, 32))
                
            #Draw the tiles based off of the map
            for y, column in enumerate(tileMap):
                for x, tile in enumerate(column):
                    drawTile(x+offsetX, y+offsetY, tile)
        drawBackground()
        drawMap()
        pygame.display.flip()
        

    #MAIN LOOP STARTS HERE
    while(True):
        handleEvents()
        draw()

def main():
    start()
    mainLoop()

main()
