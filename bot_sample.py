NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
BOMB = 5

class BotSample(object):

    def __init__(self):
        self._last_movement = NONE

    def goDown(self):
        self._last_movement = DOWN

    def goRight(self):
        self._last_movement = RIGHT

    def goUp(self):
        self._last_movement = UP

    def goLeft(self):
        self._last_movement = LEFT
    
    def putBomb(self):
        self._last_movement = BOMB

    def start(self):
        self.actions = []
        self.actions.append(self.putBomb)
        self.actions.append(self.goDown)
        self.actions.append(self.goDown)
        self.actions.append(self.goRight)
        self.actions.append(self.goRight)
        self.actions.append(self.goUp)
        self.actions.append(self.goUp)
        self.actions.append(self.goLeft)
        self.actions.append(self.goLeft)
        self.action_step = -1
    
    def execute_command(self, object):

        if self.am_i_safe():
            self.action_step += 1
            if self.action_step >= len(self.actions):
                self.action_step = 0
            
            self.actions[self.action_step]()
            
        else:
            # go to somewhere safe
            pass

        pass
    
    def am_i_safe(self):
        return True

    def looking_for_safe_place(self):
        # usar logica de arvore para achar o caminho mais curto
        pass