class Player(object):
    def __init__(self, name, bot_sample):
        self.name = name
        self.points = 0
        self.bombs_limit = 1
        self.bot_sample = bot_sample
        self.bots = []
        self.last_movement = None
        # TODO: propriedades para os poderes
