NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

class BotSample(object):

    def __init__(self):
        self._last_movement = NONE

    def goDown(self):
        self._last_movement = DOWN

    def start(self):
        pass
    
    def execute_command(self, object):

        if self.am_i_safe():
            self.goDown()
        else:
            # go to somewhere safe
            pass

        pass
    
    def am_i_safe(self):
        return True

    def looking_for_safe_place(self):
        # usar logica de arvore para achar o caminho mais curto
        pass