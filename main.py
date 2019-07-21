from src.engine import Engine
from src.objects.player import Player
from src.bot_sample import BotSample
from src.objects.block import put_blocks


class BotSample1(BotSample):
    def macro_pad(self):
        self.actions = []
        self.actions.append(self.go_down)
        self.actions.append(self.put_bomb)
        self.actions.append(self.go_up)
        self.actions.append(self.put_bomb)
        self.actions.append(self.go_right)
        self.actions.append(self.go_right)
        self.actions.append(self.go_right)
        self.actions.append(self.go_right)
        self.actions.append(self.go_right)
        self.actions.append(self.go_left)

        self.actions.append(self.go_down)
        self.actions.append(self.go_down)
        self.actions.append(self.put_bomb)
        self.actions.append(self.go_up)
        self.actions.append(self.go_up)
        self.actions.append(self.go_right)
        self.actions.append(self.go_right)
        self.actions.append(self.go_right)
        self.actions.append(self.go_right)
        self.actions.append(self.go_right)
        self.actions.append(self.go_left)

        return self.actions

    def execute_command(self, engine):
        self.execute_macro(self.macro_pad())


if __name__ == "__main__":
    engine = Engine()
    engine.build_map()
    engine.create_walls()
    player_1 = Player("1", BotSample1())
    player_2 = Player("2", BotSample())
    engine.add_player(player_1)
    engine.add_player(player_2)
    engine.add_bot(player_1, 0, 0)
    y, x = engine.map.shape
    engine.add_bot(player_2, x - 1, y - 1)
    put_blocks(engine)
    engine.start_game()

    for _ in range(2, 501):
        engine.next_turn()
