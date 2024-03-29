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


class BotPlantBombToExplode(BotSample):
    def macro(self):
        return [
            self.put_bomb,
            self.go_right,
            self.go_down,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
        ]

    def execute_command(self, engine, myself):
        self.execute_macro(self.macro())


class BotPlantBombToExplode2(BotSample):
    def macro(self):
        return [
            self.do_nothing,
            self.put_bomb,
            self.go_left,
            self.go_up,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
        ]

    def execute_command(self, engine, myself):
        self.execute_macro(self.macro())


class BotSimplePlant(BotSample):
    def macro(self):
        return [
            self.put_bomb,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
            self.do_nothing,
        ]

    def execute_command(self, engine, myself):
        self.execute_macro(self.macro())


class TestExplosion(unittest.TestCase):
    def test_bomb_explode(self):
        engine = Engine()
        engine.build_map(x=7, y=7)
        player_1 = Player("1", BotPlantBombToExplode())
        player_2 = Player("2", BotSample())
        engine.add_player(player_1)
        engine.add_player(player_2)

        engine.add_bot(player_1, 3, 3)
        engine.add_bot(player_2, 6, 6)
        engine.start_game()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y in [1, 2, 3, 4, 5]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x in [1, 2, 3, 4, 5] and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

    def test_bomb_on_the_top_corner(self):
        engine = Engine()
        engine.build_map(x=7, y=7)
        player_1 = Player("1", BotPlantBombToExplode())
        player_2 = Player("2", BotSample())
        engine.add_player(player_1)
        engine.add_player(player_2)

        engine.add_bot(player_1, 0, 0)
        engine.add_bot(player_2, 6, 6)
        engine.start_game()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 1 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 1 and y == 1:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y in [0, 1, 2]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x in [0, 1, 2] and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 1 and y == 1:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 1 and y == 1:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

    def test_bomb_on_the_bottom_corner(self):
        engine = Engine()
        engine.build_map(x=7, y=7)
        player_1 = Player("1", BotSample())
        player_2 = Player("2", BotPlantBombToExplode2())
        engine.add_player(player_1)
        engine.add_player(player_2)

        engine.add_bot(player_1, 0, 0)
        engine.add_bot(player_2, 6, 6)
        engine.start_game()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 5 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 5 and y == 5:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 6 and y in [6, 5, 4]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x in [6, 5, 4] and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x == 5 and y == 5:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 5 and y == 5:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

    def test_bomb_hitting_things(self):
        engine = Engine()
        engine.build_map(x=7, y=7)
        player_1 = Player("1", BotPlantBombToExplode())
        player_2 = Player("2", BotSample())
        engine.add_player(player_1)
        engine.add_player(player_2)

        engine.add_bot(player_1, 3, 3)
        engine.add_bot(player_2, 6, 6)
        Wall(engine, 3, 4)
        Block(engine, 3, 2)
        engine.start_game()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Wall)
                elif x == 3 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Block)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Wall)
                elif x == 3 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Block)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Wall)
                elif x == 3 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Block)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Wall)
                elif x == 3 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Block)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y in [2, 3]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x in [1, 2, 3, 4, 5] and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Wall)
                elif x == 3 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Block)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 6 and y == 6:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Wall)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

    def test_bomb_hitting_bot(self):
        engine = Engine()
        engine.build_map(x=7, y=7)
        player_1 = Player("1", BotPlantBombToExplode())
        player_2 = Player("2", BotSample())
        engine.add_player(player_1)
        engine.add_player(player_2)

        engine.add_bot(player_1, 3, 3)
        engine.add_bot(player_2, 4, 3)
        engine.start_game()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y in [1, 2, 3, 4, 5]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x in [1, 2, 3, 4, 5] and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x == 4 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        with self.assertRaises(ValueError):
            engine.next_turn()

    def test_bomb_hitting_another_bomb(self):
        engine = Engine()
        engine.build_map(x=7, y=7)
        player_1 = Player("1", BotPlantBombToExplode())
        player_2 = Player("2", BotPlantBombToExplode2())
        engine.add_player(player_1)
        engine.add_player(player_2)

        engine.add_bot(player_1, 2, 3)
        engine.add_bot(player_2, 4, 3)
        engine.start_game()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 2 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 2 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 2 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 2 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 3 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 2 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 3 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 4 and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bomb)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x in [2, 3] and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                    self.assertIsInstance(engine.map[y][x][1], Explosion)
                elif x in [0, 1, 4, 5, 6] and y == 3:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x == 2 and y in [1, 2, 3, 4, 5]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x == 4 and y in [1, 2, 3, 4, 5]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 3 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 3 and y == 4:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 3 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

    def test_bomb_killing_everyone_draw(self):
        engine = Engine()
        engine.build_map(x=3, y=3)
        player_1 = Player("1", BotSimplePlant())
        player_2 = Player("2", BotSimplePlant())
        engine.add_player(player_1)
        engine.add_player(player_2)

        engine.add_bot(player_1, 0, 0)
        engine.add_bot(player_2, 1, 1)
        engine.start_game()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                elif x == 1 and y == 1:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                elif x == 1 and y == 1:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 2 and y == 2:
                    self.assertEqual(len(engine.map[y][x]), 0)
                elif x == 0 and y == 1:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                    self.assertIsInstance(engine.map[y][x][1], Explosion)
                elif x == 1 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                    self.assertIsInstance(engine.map[y][x][1], Explosion)
                else:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)

        self.assertEqual(engine.is_finished(), True)
        self.assertEqual(engine.players[0].points, 1)
        self.assertEqual(engine.players[1].points, 1)

    def test_bomb_killing_everyone(self):
        engine = Engine()
        engine.build_map(x=3, y=3)
        player_1 = Player("1", BotSimplePlant())
        player_2 = Player("2", BotSample())
        engine.add_player(player_1)
        engine.add_player(player_2)

        engine.add_bot(player_1, 0, 0)
        engine.add_bot(player_2, 0, 1)
        engine.start_game()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y in [0, 1]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 2)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                    self.assertIsInstance(engine.map[y][x][1], Bomb)
                elif x == 0 and y == 1:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Bot)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()
        engine.next_turn()

        for y in range(len(engine.map)):
            for x in range(len(engine.map[y])):
                if x == 0 and y in [0, 1, 2]:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                elif x in [0, 1, 2] and y == 0:
                    self.assertEqual(len(engine.map[y][x]), 1)
                    self.assertIsInstance(engine.map[y][x][0], Explosion)
                else:
                    self.assertEqual(len(engine.map[y][x]), 0)

        self.assertEqual(engine.is_finished(), True)
        self.assertEqual(engine.players[0].points, 51)
        self.assertEqual(engine.players[1].points, 0)
