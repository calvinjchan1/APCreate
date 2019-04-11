import os
from src import generator

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

