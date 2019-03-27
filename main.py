import pygame, sys

#Config
global WINDOW_DIMENSIONS
WINDOW_DIMENSIONS = (640,450)


def start():
    '''
    Run once at the beginning of the program
    '''
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)

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

    while(True):
        handleEvents()
    

def main():
    start()
    mainLoop()

main()
