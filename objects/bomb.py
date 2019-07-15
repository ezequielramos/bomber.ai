from objects.explosion import Explosion, create_explosion

class Bomb(object):
    def __init__(self, x, y, owner, group, _map, explosions, bots, blocks):
        self.x = x
        self.y = y
        self.remaning_time = 7
        self.power = 3
        self.owner = owner
        self.group = group
        self._map = _map
        self.explosions = explosions
        self.bots = bots
        self.blocks = blocks
    
    def update(self):
        self.remaning_time -= 1

        if self.remaning_time == 0:
            self.group.remove(self)

            bots_killed = []

            bots_killed.extend(create_explosion(self._map, self.x, self.y, self.owner, self.explosions, self.blocks))
            bots_killed.extend(explosions_goint_to(self, 1, 0))
            bots_killed.extend(explosions_goint_to(self, -1, 0))
            bots_killed.extend(explosions_goint_to(self, 0, 1))
            bots_killed.extend(explosions_goint_to(self, 0, -1))

            for bot in bots_killed:
                self.bots.remove(bot)

def explosions_goint_to(bomb, x=0, y=0):
    bots_killed = []
    for i in range(1, bomb.power):
        try:
            bots_killed.extend(create_explosion(bomb._map, bomb.x + (i * x), bomb.y + (i * y), bomb.owner, bomb.explosions, bomb.blocks))
        except ValueError:
            break
    return bots_killed