from src.engine import Engine
from src.objects.player import Player
from src.bot_sample import BotSample

if __name__ == "__main__":
    engine = Engine()
    engine.build_map()
    player_1 = Player("1", BotSample())
    player_2 = Player("2", BotSample())
    engine.add_player(player_1)
    engine.add_player(player_2)
    engine.add_bot(player_1, 0, 0)
    y, x = engine.map.shape
    engine.add_bot(player_2, x - 1, y - 1)
    engine.start_game()

    for _ in range(2, 501):
        engine.next_turn()
