class Wall(object):
    def __init__(self, engine, x, y):
        self.engine = engine
        self.x = x
        self.y = y
        self.engine.walls.append(self)
