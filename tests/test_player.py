import sys
import os
import unittest

sys.path.append(os.path.abspath("."))

from src.engine import Engine
from src.bot_sample import BotSample
from src.objects.wall import Wall
from src.objects.bot import Bot
from src.objects.player import Player
from src.objects.block import Block, put_blocks
from src.objects.bomb import Bomb
from src.objects.explosion import Explosion


class BotTest(BotSample):
    pass


class BotGoesLeft(BotSample):
    def execute_command(self, engine, myself):
        self.go_left()


class BotGoesRight(BotSample):
    def execute_command(self, engine, myself):
        self.go_right()


class BotGoesUp(BotSample):
    def execute_command(self, engine, myself):
        self.go_up()


class BotGoesDown(BotSample):
    def execute_command(self, engine, myself):
        self.go_down()


class BotWalkingIntoBomb(BotSample):
    def macro(self):
        return [self.put_bomb, self.go_right, self.go_left]

    def execute_command(self, engine, myself):
        self.execute_macro(self.macro())


class BotMultipleBombs(BotSample):
    def macro(self):
        return [self.put_bomb, self.go_right]

    def execute_command(self, engine, myself):
        self.execute_macro(self.macro())


class TestCreateMap(unittest.TestCase):
    def test_default_map(self):
        engine = Engine()
        engine.build_map()
        self.assertEqual((11, 13), engine.map.shape)

        for col in engine.map:
            for row in col:
                self.assertIsInstance(row, list)
                self.assertEqual(len(row), 0)

    def test_custom_value_map(self):
        engine = Engine()
        engine.build_map(x=5, y=5)
        self.assertEqual(engine.map.shape, (5, 5))

        for col in engine.map:
            for row in col:
                self.assertIsInstance(row, list)
                self.assertEqual(len(row), 0)

    def test_invalid_map_x(self):
        engine = Engine()
        with self.assertRaises(ValueError):
            engine.build_map(x=2, y=3)

    def test_invalid_map_y(self):
        engine = Engine()
        with self.assertRaises(ValueError):
            engine.build_map(x=3, y=2)


class TestPutObjectsOnMap(unittest.TestCase):
    def test_putting_wall(self):
        engine = Engine()
        engine.build_map(x=3, y=3)
        Wall(engine, 1, 1)

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 0)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 1)
        self.assertIsInstance(engine.map[1][1][0], Wall)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 0)

    def test_putting_walls(self):
        engine = Engine()
        engine.build_map(x=5, y=5)
        engine.create_walls()

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 0)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)
        self.assertEqual(len(engine.map[0][3]), 0)
        self.assertEqual(len(engine.map[0][4]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 1)
        self.assertIsInstance(engine.map[1][1][0], Wall)
        self.assertEqual(len(engine.map[1][2]), 0)
        self.assertEqual(len(engine.map[1][3]), 1)
        self.assertIsInstance(engine.map[1][3][0], Wall)
        self.assertEqual(len(engine.map[1][4]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 0)
        self.assertEqual(len(engine.map[2][3]), 0)
        self.assertEqual(len(engine.map[2][4]), 0)

        # y = 3
        self.assertEqual(len(engine.map[3][0]), 0)
        self.assertEqual(len(engine.map[3][1]), 1)
        self.assertIsInstance(engine.map[3][3][0], Wall)
        self.assertEqual(len(engine.map[3][2]), 0)
        self.assertEqual(len(engine.map[3][3]), 1)
        self.assertIsInstance(engine.map[3][3][0], Wall)
        self.assertEqual(len(engine.map[3][4]), 0)

        # y = 4
        self.assertEqual(len(engine.map[4][0]), 0)
        self.assertEqual(len(engine.map[4][1]), 0)
        self.assertEqual(len(engine.map[4][2]), 0)
        self.assertEqual(len(engine.map[4][3]), 0)
        self.assertEqual(len(engine.map[4][4]), 0)

    def test_putting_block(self):
        engine = Engine()
        engine.build_map(x=3, y=3)

        Block(engine, 0, 0)
        self.assertEqual(len(engine.blocks), 1)

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Block)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 0)

    def test_putting_multiple_blocks(self):
        engine = Engine()
        engine.build_map(x=3, y=3)

        Block(engine, 0, 0)
        Block(engine, 2, 2)

        self.assertEqual(len(engine.blocks), 2)

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Block)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Block)

    def test_putting_default_blocks(self):
        engine = generate_engine_with_two_bots(BotSample)
        put_blocks(engine, 99)
        engine.draw_map()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 1)
        self.assertIsInstance(engine.map[0][2][0], Block)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 1)
        self.assertIsInstance(engine.map[1][1][0], Block)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 1)
        self.assertIsInstance(engine.map[2][0][0], Block)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)

    def test_putting_bot(self):
        engine = Engine()
        engine.build_map(x=3, y=3)
        engine.add_bot(Player("1", BotTest()), 0, 0)

        self.assertEqual(len(engine.bots), 1)

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 0)

    def test_putting_multiple_bots(self):
        engine = Engine()
        engine.build_map(x=3, y=3)
        engine.add_bot(Player("1", BotTest()), 0, 0)
        engine.add_bot(Player("2", BotTest()), 2, 2)

        self.assertEqual(len(engine.bots), 2)

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)

    def test_next_turn_on_game_not_started(self):
        engine = Engine()
        engine.build_map(x=3, y=3)
        with self.assertRaises(ValueError):
            engine.next_turn()

    def test_trying_to_start_game_without_enough_players(self):
        engine = Engine()
        engine.build_map(x=3, y=3)
        with self.assertRaises(ValueError):
            engine.start_game()

    def test_trying_to_start_game_without_enough_bots(self):
        engine = Engine()
        engine.build_map(x=3, y=3)
        player_1 = Player("1", BotTest())
        engine.add_player(player_1)
        engine.add_player(player_1)
        with self.assertRaises(ValueError):
            engine.start_game()

    def test_bot_goes_left(self):
        engine = generate_engine_with_two_bots(BotGoesLeft)
        engine.start_game()

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        # --------------------------
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 1)
        self.assertIsInstance(engine.map[2][1][0], Bot)
        self.assertEqual(len(engine.map[2][2]), 0)

    def test_bot_goes_right(self):
        engine = generate_engine_with_two_bots(BotGoesRight)
        engine.start_game()

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        # --------------------------
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 0)
        self.assertEqual(len(engine.map[0][1]), 1)
        self.assertIsInstance(engine.map[0][1][0], Bot)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)

    def test_bot_goes_up(self):
        engine = generate_engine_with_two_bots(BotGoesUp)
        engine.start_game()

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        # --------------------------
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 1)
        self.assertIsInstance(engine.map[1][2][0], Bot)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 0)

    def test_bot_goes_down(self):
        engine = generate_engine_with_two_bots(BotGoesDown)
        engine.start_game()

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        # --------------------------
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 0)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 1)
        self.assertIsInstance(engine.map[1][0][0], Bot)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)

    def test_walk_against_wall(self):
        engine = generate_engine_with_two_bots(BotGoesDown)
        Wall(engine, 0, 1)
        engine.start_game()

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 1)
        self.assertIsInstance(engine.map[1][0][0], Wall)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        # --------------------------
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 1)
        self.assertIsInstance(engine.map[1][0][0], Wall)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)

    def test_walk_against_block(self):
        engine = generate_engine_with_two_bots(BotGoesDown)
        Block(engine, 0, 1)
        engine.start_game()

        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 1)
        self.assertIsInstance(engine.map[1][0][0], Block)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        # --------------------------
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 1)
        self.assertIsInstance(engine.map[1][0][0], Block)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)

    def test_walk_against_bomb(self):
        engine = generate_engine_with_two_bots(BotWalkingIntoBomb)

        engine.start_game()
        # turn 1
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        # --------------------------
        # turn 2
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 2)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertIsInstance(engine.map[0][0][1], Bomb)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 2)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        self.assertIsInstance(engine.map[2][2][1], Bomb)
        # --------------------------
        # turn 3
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bomb)
        self.assertEqual(len(engine.map[0][1]), 1)
        self.assertIsInstance(engine.map[0][1][0], Bot)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 2)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        self.assertIsInstance(engine.map[2][2][1], Bomb)
        # --------------------------
        # turn 4
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bomb)
        self.assertEqual(len(engine.map[0][1]), 1)
        self.assertIsInstance(engine.map[0][1][0], Bot)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 1)
        self.assertIsInstance(engine.map[2][1][0], Bot)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bomb)

    def test_trying_to_put_multiple_bombs(self):
        engine = generate_engine_with_two_bots(BotMultipleBombs)
        engine.start_game()
        # turn 1
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 1)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        # --------------------------
        # turn 2
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 2)
        self.assertIsInstance(engine.map[0][0][0], Bot)
        self.assertIsInstance(engine.map[0][0][1], Bomb)
        self.assertEqual(len(engine.map[0][1]), 0)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 2)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        self.assertIsInstance(engine.map[2][2][1], Bomb)
        # --------------------------
        # turn 3
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bomb)
        self.assertEqual(len(engine.map[0][1]), 1)
        self.assertIsInstance(engine.map[0][1][0], Bot)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 2)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        self.assertIsInstance(engine.map[2][2][1], Bomb)
        # --------------------------
        # turn 4
        engine.next_turn()
        # y = 0
        self.assertEqual(len(engine.map[0][0]), 1)
        self.assertIsInstance(engine.map[0][0][0], Bomb)
        self.assertEqual(len(engine.map[0][1]), 1)
        self.assertIsInstance(engine.map[0][1][0], Bot)
        self.assertEqual(len(engine.map[0][2]), 0)

        # y = 1
        self.assertEqual(len(engine.map[1][0]), 0)
        self.assertEqual(len(engine.map[1][1]), 0)
        self.assertEqual(len(engine.map[1][2]), 0)

        # y = 2
        self.assertEqual(len(engine.map[2][0]), 0)
        self.assertEqual(len(engine.map[2][1]), 0)
        self.assertEqual(len(engine.map[2][2]), 2)
        self.assertIsInstance(engine.map[2][2][0], Bot)
        self.assertIsInstance(engine.map[2][2][1], Bomb)


def generate_engine_with_two_bots(bot_sample):
    engine = Engine()
    engine.build_map(x=3, y=3)
    player_1 = Player("1", bot_sample())
    player_2 = Player("2", bot_sample())
    engine.add_player(player_1)
    engine.add_player(player_2)

    engine.add_bot(player_1, 0, 0)
    engine.add_bot(player_2, 2, 2)

    return engine
