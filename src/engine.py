import numpy as np
import random

from src.objects.wall import Wall
from src.objects.block import Block, remove_block_on, put_blocks
from src.objects.bomb import Bomb
from src.objects.explosion import Explosion, create_explosion
from src.objects.bot import Bot
from src.objects.group import Group
from src.objects.player import Player
from typing import List


TURN_BY_TURN_MODE = False

NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
BOMB = 5


class Engine(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.explosions = Group(self)
        self.blocks = Group(self)
        self.bombs = Group(self)
        self.bots: List[Bot] = []
        self.players: List[Player] = []
        self.turn = 1
        self.map: np.array = None

    def build_map(self):

        array_x = []

        for j in range(6):

            array_y = []
            for i in range(13):
                if i % 2 == 0:
                    array_y.append([])
                else:
                    array_y.append([Wall()])

            array_y_empty = []
            for i in range(13):
                array_y_empty.append([])

            array_x.append(array_y_empty)
            array_x.append(array_y)

        array_x.pop()

        self.map = np.array(array_x)

    def draw_map(self):
        print("-" * 55)
        print(f"Turn {self.turn}")
        illustrated_map = []

        for col in self.map:
            illustrated_map.append([])
            for row in col:
                if len(row) == 0:
                    illustrated_map[-1].append(" ")
                else:
                    if isinstance(row[0], Explosion):
                        illustrated_map[-1].append("@")
                    if isinstance(row[0], Bot):
                        illustrated_map[-1].append(row[0].player.name)
                    if isinstance(row[0], Wall):
                        illustrated_map[-1].append("X")
                    if isinstance(row[0], Bomb):
                        illustrated_map[-1].append("o")
                    if isinstance(row[0], Block):
                        illustrated_map[-1].append("+")

        print(np.array(illustrated_map))
        for player in self.players:
            print(f"Score player {player.name}: {player.points}")
        if TURN_BY_TURN_MODE:
            input("press any button to advance to the next turn...")

    def next_turn(self):
        self.turn += 1

        for player in self.players:
            # FIXME: i cant send the actually _map object, i need to clone it
            player.bot_sample.execute_command(self)
            player.last_movement = player.bot_sample._last_movement
            player.bot_sample._last_movement = NONE

        for player in self.players:
            if player.last_movement in [UP, DOWN, LEFT, RIGHT]:
                bot = player.bots[0]
                bot.move(player.last_movement)
                player.last_movement = NONE

        for player in self.players:
            if player.last_movement in [BOMB]:
                bot = player.bots[0]
                bot.plant_bombs(player.last_movement)
                player.last_movement = NONE

        self.bombs.update()
        self.explosions.update()

        self.draw_map()

        players_alive = set()
        for bot in self.bots:
            players_alive.add(bot.player)

        if len(players_alive) == 1:
            winner = players_alive.pop()
            print(f"Player {winner.name} won!")
            exit()

        if len(players_alive) == 0:
            p = Player("dumb")
            p.points = -1
            winners = [p]
            for player in self.players:
                if player.points > winners[0].points:
                    winners = [player]
                if player.points == winners[0].points:
                    winners.append(player)

            if len(winners) == 1:
                print(f"Player {winners.name} won!")
            else:
                print(f"Draw: Players {' '.join([p.name for p in winners])}")
            exit()

    def start_game(self):
        for player in self.players:
            player.bot_sample.start()
        self.draw_map()

    def add_player(self, player: Player):
        self.players.append(player)

    def add_bot(self, player, x, y):
        self.bots.append(Bot(x, y, self, player))
