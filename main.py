import numpy as np
import random

TURN_BY_TURN_MODE = True

NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
BOMB = 5

class Wall(object):
    pass

class Block(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bot(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.points = 0

class Bomb(object):
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.remaning_time = 7
        self.power = 3
        self.owner = owner
    
    def update(self):
        self.remaning_time -= 1

        if self.remaning_time == 0:
            bombs.remove(self)

            bots_killed = []

            bots_killed.extend(create_explosion(_map, self.x, self.y, self.owner))
            explosions_goint_to(self, 1, 0)
            explosions_goint_to(self, -1, 0)
            explosions_goint_to(self, 0, 1)
            explosions_goint_to(self, 0, -1)

            for bot in bots_killed:
                bots.remove(bot)
                #FIXME: tirar do mapa quando isso acontecer

class Explosion(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.remaning_time = 2

    def update(self):
        self.remaning_time -= 1
        if self.remaning_time == 0:
            explosions.remove(self)

class Group(list):
    def __init__(self, _map, iterable=None):
        self._map = _map
        if iterable is None:
            iterable = []
        return super().__init__(iterable)

    def update(self):
        auxiliar_list = self[:]
        for _object in auxiliar_list:
            _object.update()

    def append(self, value):
        self._map[value.y][value.x].append(value)
        return super().append(value)

    def remove(self, value):
        self._map[value.y][value.x].remove(value)
        return super().remove(value)

def build_map():

    array_x = []

    for j in range(6):

        array_y = []
        for i in range(13):
            if i % 2 == 0:
                array_y.append([])
            else:
                array_y.append([Wall()])

        array_y_empty = []
        for i in range(13):
            array_y_empty.append([])

        array_x.append(array_y_empty)
        array_x.append(array_y)

    array_x.pop()

    return np.array(array_x)

_map = build_map()

# FIXME: é mais facil usar essas variaveis pra fazer o mapa sempre ficar desenhando tudo em cada loop do que ter que sempre ficar arrumando em dois lugares
# TODO: ao inves de uma lista isso poderia ser um objeto de grupo com os metodos de update dentro disso
bombs = Group(_map)
explosions = Group(_map)
blocks = Group(_map)
#TODO: player deveria ser um jogador. e um jogador poderia ter multiplos bots
bots = [Bot('1', 0, 0), Bot('2', len(_map[0]) - 1, len(_map) - 1)] #TODO: essas posicoes nao deveriam ser fixas

#TODO: mandar isso pra dentro do objeto Bot
for bot in bots:
    _map[bot.y][bot.x].append(bot)

def remove_block_on(_map, x, y):
    if x < 0:
        return

    if y < 0:
        return

    try:
        for _object in _map[y, x]:
            if isinstance(_object, Block):
                blocks.remove(_object)
                break
    except IndexError:
        pass

def put_blocks(_map):
    for y in range(len(_map)):
        for x in range(len(_map[y])):
            if len(_map[y][x]) == 0:
                if random.randint(0, 99) < 100:
                    blocks.append(Block(x, y))

    for bot in bots:
        remove_block_on(_map, bot.x, bot.y)
        remove_block_on(_map, bot.x-1, bot.y)
        remove_block_on(_map, bot.x+1, bot.y)
        remove_block_on(_map, bot.x, bot.y-1)
        remove_block_on(_map, bot.x, bot.y+1)

from bot_sample import BotSample

bot_sample1 = BotSample()
bot_sample1.start()

def get_bot_location(_map, bot):
    found = False

    for y in range(len(_map)):
        for x in range(len(_map[y])):
            if bot in _map[y][x]:
                found = True
                break
        
        if found:
            break

    return x, y

def movements(_map, movement, bot):
    x, y = get_bot_location(_map, bot)

    #FIXME: alterar para mudar o valor no objeto bot tambem
    if movement == DOWN:
        dest_x = x
        dest_y = y + 1
    if movement == UP:
        dest_x = x
        dest_y = y - 1
    if movement == LEFT:
        dest_x = x - 1
        dest_y = y
    if movement == RIGHT:
        dest_x = x + 1
        dest_y = y

    if dest_y < 0 or dest_x < 0:
        return

    for _object in _map[dest_y][dest_x]:
        if isinstance(_object, (Bomb, Wall, Block)):
            return

    _map[dest_y][dest_x].append(bot)
    _map[y][x].remove(bot)

def plant_bombs(_map, movement, bot):
    x, y = get_bot_location(_map, bot)

    if movement == BOMB:
        bombs.append(Bomb(x, y, bot))
        #TODO: aumentar o ponto do player e não do bot
        bot.points += 1

def draw_map(turn):
    print('-' * 55)
    print(f'Turn {turn}')
    illustrated_map = []

    for col in _map:
        illustrated_map.append([])
        for row in col:
            if len(row) == 0:
                illustrated_map[-1].append(' ')
            else:
                if isinstance(row[0], Explosion):
                    illustrated_map[-1].append('@')
                if isinstance(row[0], Bot):
                    illustrated_map[-1].append(row[0].name)
                if isinstance(row[0], Wall):
                    illustrated_map[-1].append('X')
                if isinstance(row[0], Bomb):
                    illustrated_map[-1].append('o')
                if isinstance(row[0], Block):
                    illustrated_map[-1].append('+')
                    

    print(np.array(illustrated_map))
    for bot in bots:
        #TODO: apresentar pontuacao do player. Nao do bot
        print(f'Score player {bot.name}: {bot.points}')
    if TURN_BY_TURN_MODE:
        input('press any button to advance to the next turn...')
    
def create_explosion(_map, x, y, owner):
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
                remove_block_on(_map, x, y)
                explosions.append(Explosion(x, y))
                owner.points += 2
                raise ValueError('acertou um bloco')
    except IndexError:
        raise ValueError('explosao foi pra fora do mapa')

    explosions.append(Explosion(x, y))

    return bots_killed

def explosions_goint_to(bomb, x=0, y=0,):
    bots_killed = []
    for i in range(1, bomb.power):
        try:
            bots_killed.extend(create_explosion(_map, bomb.x + (i * x), bomb.y + (i * y), bomb.owner))
        except ValueError:
            break
    return bots_killed

if __name__ == "__main__":

    put_blocks(_map)
    draw_map(1)

    for turn in range(2,501):

        #TODO: this should be an loop throw all bot samples
        bot_sample1.execute_command(_map) # FIXME: i cant send the actually _map object, i need to clone it
        command = bot_sample1._last_movement
        bot_sample1._last_movement = NONE

        try:
            if command in [UP, DOWN, LEFT, RIGHT]:
                movements(_map, command, bots[0])
            if command in [BOMB]:
                plant_bombs(_map, command, bots[0])

        except IndexError:
            pass

        bombs.update()
        explosions.update()

        draw_map(turn)

        #FIXME: Uma vez que um player tiver multiplos bots, verificar se todos bots vivos são do mesmo player
        #FIXME: Existe a possibilidade de todos bots terem morrido no mesmo momento. 0 bots vivos
        if len(bots) == 1:
            print(f'{bots[0].name} venceu!')
            exit()