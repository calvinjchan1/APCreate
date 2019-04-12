import os
from main import generator

def init():
    #Makes sure saves folder exists and intilizes module
    #Returns True if succesful, false otherwise
    if not os.path.exists("saves"):
        try:
            os.mkdir("saves")
        except OSError:
            return False
    return True

def newSave(name, seed):
    '''
    Creates a new save file with the given seed and name
    return values:
        0 - Success
        1 - Failure
        2 - File already exists
    '''
    if os.path.exists("saves/"+name):
        return 2
    else:
        try:
            os.mkdir("saves/"+name)
        except OSError:
            print("Failed to make world directory")
            return 1
    f = open("saves/"+name+"/worlddata", "w")
    f.write(seed)
    f.close
    return 0

def loadSave(name):
    '''
    Attempts to load the save of the given name
    returns 0 if successful, 1 if the world doesn't exist
    and 2 if it failed for some other reason
    '''
    #TODO:Write this function
    #Make get a selection and make sure it exists
    worldList = os.listdir("saves")#Get all world folders
    if len(worldList) == 0: #Make sure that there is at least one save to be loaded
        return 2
    if not name in worldList: #Return to main menu if user makes a choice that doesn't exist
        return 1
    else:
        f = open("saves/"+name+"/worlddata", "r")#Get the seed from the save file
        seed = f.readline()
        f.close()
        generator.setSeed(seed)
        return 0
