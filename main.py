import numpy as np
import random

NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

array_y = [' ', 'X'] * 7
array_y.pop()
array_y_empty = [' '] * 14
array_y_empty.pop()
array_x = [array_y_empty, array_y] * 6
array_x.pop()

_map = np.array(array_x)
_map[0][0] = '1'
_map[-1][-1] = '2'

for x in range(len(_map)):
    for y in range(len(_map[x])):
        if (
            (x == 1 and y == 0) or
            (x == 0 and y == 1) or
            (x == len(_map) - 1 and y == len(_map[x]) - 2) or 
            (x == len(_map) - 2 and y == len(_map[x]) - 1)
        ):
            continue
        if _map[x][y] == " ":
            if random.randint(0, 99) < 80:
                # _map[x][y] = "-"
                pass


from bot_sample import BotSample

bot_sample1 = BotSample()
bot_sample1.start()


while True:
    print(_map)
    bot_sample1.execute_command(_map) # i cant send the actually _map object, i need to clone it
    movement = bot_sample1._last_movement
    bot_sample1._last_movement = NONE

    y, x = np.where(_map == '1')
    print(x, y)

    if movement == DOWN:
        try:
            dest_x = x[0]
            dest_y = y[0] + 1
            
            if _map[dest_y][dest_x] == ' ':
                _map[dest_y][dest_x] = '1'
                _map[y[0]][x[0]] = ' '
        except IndexError:
            pass

    input('press any button to advance to the next turn...')


