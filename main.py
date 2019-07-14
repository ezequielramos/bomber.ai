import numpy as np
import random

NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
BOMB = 5

class Wall(object):
    pass

class Block(object):
    pass

class Player(object):
    def __init__(self, name):
        self.name = name

class Bomb(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.remaning_time = 7
        self.power = 3
    
    def update(self):
        self.remaning_time -= 1

class Explosion(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.remaning_time = 2

    def update(self):
        self.remaning_time -= 1

bombs = []
explosions = []

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

players = [Player('1'), Player('2')]

_map[0][0].append(players[0])
_map[-1][-1].append(players[1])

def put_blocks(_map):
    for x in range(len(_map)):
        for y in range(len(_map[x])):
            #TODO: alterar essa logica para deixar de ser fixa e pegar o redor de cada player
            if (
                (x == 1 and y == 0) or
                (x == 0 and y == 1) or
                (x == len(_map) - 1 and y == len(_map[x]) - 2) or 
                (x == len(_map) - 2 and y == len(_map[x]) - 1)
            ):
                continue
            if len(_map[x][y]):
                if random.randint(0, 99) < 80:
                    _map[x][y].append(Block())


from bot_sample import BotSample

bot_sample1 = BotSample()
bot_sample1.start()

def get_player_location(_map, player):
    found = False

    for y in range(len(_map)):
        for x in range(len(_map[y])):
            if player in _map[y][x]:
                found = True
                break
        
        if found:
            break

    return x, y

def movements(_map, movement, player):
    x, y = get_player_location(_map, player)

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

    _map[dest_y][dest_x].append(player)
    _map[y][x].remove(player)

def plant_bombs(_map, movement, player):
    x, y = get_player_location(_map, player)

    if movement == BOMB:
        bombs.append(Bomb(x, y))
        _map[y][x].append(bombs[-1])

def draw_map():
    illustrated_map = []

    for col in _map:
        illustrated_map.append([])
        for row in col:
            if len(row) == 0:
                illustrated_map[-1].append(' ')
            else:
                if isinstance(row[0], Explosion):
                    illustrated_map[-1].append('@')
                if isinstance(row[0], Player):
                    illustrated_map[-1].append(row[0].name)
                if isinstance(row[0], Wall):
                    illustrated_map[-1].append('X')
                if isinstance(row[0], Bomb):
                    illustrated_map[-1].append('o')
                    

    print(np.array(illustrated_map))
    input('press any button to advance to the next turn...')
    
draw_map()

def create_explosion(_map, x, y):
    players_killed = []

    if x < 0:
        raise ValueError('x menor que zero')
    if y < 0:
        raise ValueError('y menor que zero')

    explosions.append(Explosion(x, y))
    _map[y][x].append(explosions[-1])

    for _object in _map[y][x]:
        if isinstance(_object, Player):
            players_killed.append(_object)

    return players_killed

def update_bombs(_map):
    auxiliar_bombs = bombs[:]
    for bomb in auxiliar_bombs:
        bomb: Bomb
        bomb.update()
        if bomb.remaning_time == 0:
            bombs.remove(bomb)
            x = bomb.x
            y = bomb.y
            _map[y][x].remove(bomb)

            players_killed = []

            players_killed.extend(create_explosion(_map, x, y))

            #FIXME: todos esses caras tem que validar se não existe algum obstaculo
            for i in range(bomb.power):
                try:
                    players_killed.extend(create_explosion(_map, bomb.x + i, bomb.y))
                except ValueError:
                    break

            for i in range(bomb.power):
                try:
                    players_killed.extend(create_explosion(_map, bomb.x - i, bomb.y))
                except ValueError:
                    break

            for i in range(bomb.power):
                try:
                    players_killed.extend(create_explosion(_map, bomb.x, bomb.y + i))
                except ValueError:
                    break

            for i in range(bomb.power):
                try:
                    players_killed.extend(create_explosion(_map, bomb.x, bomb.y - i))
                except ValueError:
                    break

            for player in players_killed:
                players.remove(player)

def update_explosions(_map):
    auxiliar_explosions = explosions[:]
    for explosion in auxiliar_explosions:
        explosion.update()
        if explosion.remaning_time == 0:
            explosions.remove(explosion)
            x = explosion.x
            y = explosion.y
            _map[y][x].remove(explosion)

while True:

    #TODO: this should be an loop throw all bot samples
    bot_sample1.execute_command(_map) # FIXME: i cant send the actually _map object, i need to clone it
    command = bot_sample1._last_movement
    bot_sample1._last_movement = NONE

    try:
        if command in [UP, DOWN, LEFT, RIGHT]:
            movements(_map, command, players[0])
        if command in [BOMB]:
            plant_bombs(_map, command, players[0])

    except IndexError:
        pass

    update_bombs(_map)
    update_explosions(_map)

    draw_map()

    if len(players) == 1:
        print(f'{players[0].name} venceu!')
        exit()