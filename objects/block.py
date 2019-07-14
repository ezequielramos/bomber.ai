import random

class Block(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def remove_block_on(_map, blocks, x, y):
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

#TODO: should it be here or on the engine object?
def put_blocks(engine):
    for y in range(len(engine.map)):
        for x in range(len(engine.map[y])):
            if len(engine.map[y][x]) == 0:
                if random.randint(0, 99) < 100:
                    engine.blocks.append(Block(x, y))

    for bot in engine.bots:
        remove_block_on(engine.map, engine.blocks, bot.x, bot.y)
        remove_block_on(engine.map, engine.blocks, bot.x-1, bot.y)
        remove_block_on(engine.map, engine.blocks, bot.x+1, bot.y)
        remove_block_on(engine.map, engine.blocks, bot.x, bot.y-1)
        remove_block_on(engine.map, engine.blocks, bot.x, bot.y+1)