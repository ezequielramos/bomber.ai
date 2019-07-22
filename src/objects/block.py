import random


class Block(object):
    def __init__(self, engine, x, y):
        self.x = x
        self.y = y
        self.engine = engine
        engine.blocks.append(self)


def remove_block_on(engine, x, y):
    if x < 0:
        return

    if y < 0:
        return

    try:
        for _object in engine.map[y, x]:
            if isinstance(_object, Block):
                engine.blocks.remove(_object)
                break
    except IndexError:
        pass


# TODO: should it be here or on the engine object?
def put_blocks(engine, probability=90):
    for y in range(len(engine.map)):
        for x in range(len(engine.map[y])):
            if len(engine.map[y][x]) == 0:
                if random.randint(0, probability) < 100:
                    Block(engine, x, y)

    for bot in engine.bots:
        remove_block_on(engine, bot.x, bot.y)
        remove_block_on(engine, bot.x - 1, bot.y)
        remove_block_on(engine, bot.x + 1, bot.y)
        remove_block_on(engine, bot.x, bot.y - 1)
        remove_block_on(engine, bot.x, bot.y + 1)
