from src.objects.explosion import Explosion, create_explosion


class Bomb(object):
    def __init__(self, engine, x, y, owner):
        self.x = x
        self.y = y
        self.remaning_time = 6
        self.power = 3
        self.owner = owner
        self.engine = engine

    def explode(self):
        self.engine.bombs.remove(self)

        bots_killed = []

        bots_killed.extend(create_explosion(self.engine, self.x, self.y, self.owner))
        bots_killed.extend(self._explosions_goint_to(1, 0))
        bots_killed.extend(self._explosions_goint_to(-1, 0))
        bots_killed.extend(self._explosions_goint_to(0, 1))
        bots_killed.extend(self._explosions_goint_to(0, -1))

        for bot in bots_killed:
            self.engine.bots.remove(bot)

    def update(self):
        if self.remaning_time == 0:
            self.explode()
        self.remaning_time -= 1

    def _explosions_goint_to(self, x=0, y=0):
        bots_killed = []
        for i in range(1, self.power):
            try:
                bots_killed.extend(
                    create_explosion(
                        self.engine, self.x + (i * x), self.y + (i * y), self.owner
                    )
                )
            except ValueError:
                break
        return bots_killed

    def get_cell(self):
        return self.engine.map[self.y][self.x]