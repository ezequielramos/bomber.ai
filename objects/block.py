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