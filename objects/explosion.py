from objects.block import Block, remove_block_on
from objects.wall import Wall
from objects.bot import Bot

class Explosion(object):
    def __init__(self, x, y, group):
        self.x = x
        self.y = y
        self.remaning_time = 2
        self.group = group

    def update(self):
        self.remaning_time -= 1
        if self.remaning_time == 0:
            self.group.remove(self)

def create_explosion(_map, x, y, owner, explosions, blocks):
    bots_killed = []

    if x < 0:
        raise ValueError('x menor que zero')
    if y < 0:
        raise ValueError('y menor que zero')

    #TODO: talvez essas logicas deveriam estar dentro do objeto explosion?
    try:
        for _object in _map[y][x]:
            if isinstance(_object, Wall):
                raise ValueError('tem uma parede ai irmao')

            if isinstance(_object, Bot):
                bots_killed.append(_object)

            if isinstance(_object, Block):
                remove_block_on(_map, blocks, x, y)
                explosions.append(Explosion(x, y, explosions))
                owner.points += 2
                raise ValueError('acertou um bloco')
    except IndexError:
        raise ValueError('explosao foi pra fora do mapa')

    explosions.append(Explosion(x, y, explosions))

    return bots_killed