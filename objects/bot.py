import objects

NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
BOMB = 5

class Bot(object):
    def __init__(self, name, x, y, engine):
        self.name = name
        self.x = x
        self.y = y
        self.points = 0
        self.engine = engine

    def move(self, command):

        if command == DOWN:
            dest_x = self.x
            dest_y = self.y + 1
        if command == UP:
            dest_x = self.x
            dest_y = self.y - 1
        if command == LEFT:
            dest_x = self.x - 1
            dest_y = self.y
        if command == RIGHT:
            dest_x = self.x + 1
            dest_y = self.y

        if dest_y < 0 or dest_x < 0:
            return

        for _object in self.engine.map[dest_y][dest_x]:
            if isinstance(_object, (objects.bomb.Bomb, objects.wall.Wall, objects.block.Block)):
                return

        self.engine.map[dest_y][dest_x].append(self)
        self.engine.map[self.y][self.x].remove(self)

        self.x = dest_x
        self.y = dest_y