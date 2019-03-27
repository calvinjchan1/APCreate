import pygame, sys

#Config
WINDOW_DIMENSIONS = (640,450)


def start():
    '''
    Run once at the beginning of the program
    '''
    global tileMap, screen
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    tileMap = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

def mainLoop():
    '''
    The main loop of the program
    '''
    def handleEvents():
        '''
        Deals with all of the user input
        '''
        
        for event in pygame.event.get():
            #Exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    def draw():
        '''
        Handles draw everything to the screen
        '''
        def drawMap():
            screen.fill(pygame.Color("red"), (0, 0, 32, 32))

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
