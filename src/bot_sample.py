from typing import List, Callable

NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
BOMB = 5


class BotSample(object):
    def __init__(self):
        self.action_step = 0
        self._last_movement = NONE

    def go_down(self, is_macro=False):
        if not is_macro:
            self.action_step = 0
        self._last_movement = DOWN

    def go_right(self, is_macro=False):
        if not is_macro:
            self.action_step = 0
        self._last_movement = RIGHT

    def go_up(self, is_macro=False):
        if not is_macro:
            self.action_step = 0
        self._last_movement = UP

    def go_left(self, is_macro=False):
        if not is_macro:
            self.action_step = 0
        self._last_movement = LEFT

    def put_bomb(self, is_macro=False):
        if not is_macro:
            self.action_step = 0
        self._last_movement = BOMB

    def do_nothing(self, is_macro=False):
        if not is_macro:
            self.action_step = 0
        self._last_movement = NONE

    def start(self):
        pass

    def execute_macro(self, macro: List[Callable]):
        if self.action_step >= len(macro):
            self.action_step = 0
        macro[self.action_step](True)
        self.action_step += 1

    def execute_command(self, engine):
        pass

    def am_i_safe(self):
        return True

    def looking_for_safe_place(self):
        # usar logica de arvore para achar o caminho mais curto
        pass
