'''
How to use objects:
    Each object should have an x and y value, and should be
    inside of the objList

    Each one should also have a draw and kill method.
'''

def init():
    '''
    Initalizes the object module, call before using
    '''
    global objList
    objList = []

class Obj:
    '''
    Basic Object class
    '''
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        objList.append(self)

    def draw(self):
        pass

    def kill(self):
        pass

