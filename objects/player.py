class Player(object):
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.bombs_limit = 1 #TODO: use this property to valid number of bombs
        #TODO: propriedades para os poderes
