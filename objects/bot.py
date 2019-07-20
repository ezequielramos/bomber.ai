import objects

NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
BOMB = 5


class Bot(object):
    def __init__(self, x, y, engine, player):
        self.x = x
        self.y = y
        self.engine = engine
        self.player = player

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
            if isinstance(
                _object, (objects.bomb.Bomb, objects.wall.Wall, objects.block.Block)
            ):
                return

        self.engine.map[dest_y][dest_x].append(self)
        self.engine.map[self.y][self.x].remove(self)

        self.x = dest_x
        self.y = dest_y

    def plant_bombs(self, command):

        if command == BOMB:
            bomb_quantity = 0
            for bomb in self.engine.bombs:
                if bomb.owner.player.name == self.player.name:
                    bomb_quantity += 1

            if bomb_quantity < self.player.bombs_limit:
                self.engine.bombs.append(
                    objects.bomb.Bomb(
                        self.x,
                        self.y,
                        self,
                        self.engine.bombs,
                        self.engine.map,
                        self.engine.explosions,
                        self.engine.bots,
                        self.engine.blocks,
                    )
                )
                # TODO: aumentar o ponto do player e não do bot
                self.player.points += 1
