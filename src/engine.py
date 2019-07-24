import numpy as np
import random
import _io
from typing import List

from src.objects.wall import Wall
from src.objects.block import Block, remove_block_on, put_blocks
from src.objects.bomb import Bomb
from src.objects.explosion import Explosion, create_explosion
from src.objects.bot import Bot
from src.objects.group import Group
from src.objects.player import Player
from src.objects.cell import Cell

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
        self.walls = Group(self)
        self.bots = Group(self)
        self.players: List[Player] = []
        self.turn = 1
        self.map: np.array = None
        self._started = False
        self._finished = False
        self.file: _io.BufferedWriter = None

    def is_finished(self):
        return self._finished

    def build_map(self, y=13, x=11):

        if x % 2 == 0:
            raise ValueError("'x' must be a odd number")

        if y % 2 == 0:
            raise ValueError("'y' must be a odd number")

        array_x = []

        for j in range(x):

            array_y = []
            for i in range(y):
                array_y.append(Cell(i, j))

            array_x.append(array_y)

        array_x[0][0].append(" ")
        self.map = np.array(array_x)
        self.map[0][0].pop()

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                try:
                    if (y - 1) < 0:
                        raise ValueError("y menor que zero")
                    self.map[y][x].up = self.map[y - 1][x]
                except:
                    pass
                try:
                    self.map[y][x].down = self.map[y + 1][x]
                except:
                    pass
                try:
                    if (x - 1) < 0:
                        raise ValueError("x menor que zero")
                    self.map[y][x].left = self.map[y][x - 1]
                except:
                    pass
                try:
                    self.map[y][x].right = self.map[y][x + 1]
                except:
                    pass

    def create_walls(self):

        for y in range(0, len(self.map)):
            if y % 2 == 0:
                continue
            for x in range(0, len(self.map[y])):
                if x % 2 == 0:
                    continue

                Wall(self, x, y)

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

        if self.file is not None:
            self.file.write(self.blocks.get_objects_position())
            self.file.write(self.explosions.get_objects_position())
            self.file.write(self.bombs.get_objects_position())
            self.file.write(self.bots.get_objects_position())
            # self.players: List[Player] = []

    def next_turn(self):

        if not self._started:
            raise ValueError("Game isn't started.")

        if self._finished:
            raise ValueError("Game is finished.")

        self.turn += 1

        for player in self.players:
            # FIXME: i cant send the actually _map object, i need to clone it
            player.bot_sample.execute_command(self, player)
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
            self._finished = True
            return True

        if len(players_alive) == 0:
            p = Player("dumb", None)
            p.points = -1
            winners = [p]
            for player in self.players:
                if player.points > winners[0].points:
                    winners = [player]
                elif player.points == winners[0].points:
                    winners.append(player)

            if len(winners) == 1:
                print(f"Player {winners[0].name} won!")
            else:
                print(f"Draw: Players {' '.join([p.name for p in winners])}")
            self._finished = True
            return True

        return False

    def start_game(self, file: _io.BufferedWriter = None):

        if len(self.players) < 2:
            raise ValueError("Game can't start. It must have at least 2 players.")

        if len(self.bots) < 2:
            raise ValueError("Game can't start. It must have at least 2 bots.")

        self._started = True
        self.file = file

        if self.file is not None:
            y, x = self.map.shape
            self.file.write(bytes(f"{x},{y}\n", "utf8"))

            self.file.write(
                bytes(
                    " ".join([f"{wall.x},{wall.y}" for wall in self.walls]) + "\n",
                    "utf8",
                )
            )

            for player in self.players:
                self.file.write(bytes(f"{player.name}\n", "utf8"))

            self.file.write(b"\n")

        for player in self.players:
            player.bot_sample.start()
        self.draw_map()

    def add_player(self, player: Player):
        self.players.append(player)

    def add_bot(self, player, x, y):
        self.bots.append(Bot(self, x, y, player))
