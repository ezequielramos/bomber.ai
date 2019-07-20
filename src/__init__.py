import numpy as np
import random

from src.objects.wall import Wall
from src.objects.block import Block, remove_block_on, put_blocks
from src.objects.bomb import Bomb
from src.objects.explosion import Explosion, create_explosion
from src.objects.bot import Bot
from src.objects.group import Group
from src.objects.player import Player

TURN_BY_TURN_MODE = False

NONE = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
BOMB = 5

from src.bot_sample import BotSample

bot_sample1 = BotSample()


class Engine(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.explosions = Group(self)
        self.blocks = Group(self)
        self.bombs = Group(self)
        self.bots = []
        self.players = []
        self.turn = 1

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
            # TODO: apresentar pontuacao do player. Nao do bot
            print(f"Score player {player.name}: {player.points}")
        if TURN_BY_TURN_MODE:
            input("press any button to advance to the next turn...")

    def next_turn(self):
        self.turn += 1

        # TODO: this should be an loop throw all bot samples
        bot_sample1.execute_command(
            self
        )  # FIXME: i cant send the actually _map object, i need to clone it
        command = bot_sample1._last_movement
        bot_sample1._last_movement = NONE

        try:
            bot: Bot = self.bots[0]
            if command in [UP, DOWN, LEFT, RIGHT]:
                bot.move(command)
                # movements(self.map, command, self.bots[0])
            if command in [BOMB]:
                bot.plant_bombs(command)

        except IndexError:
            pass

        self.bombs.update()
        self.explosions.update()

        self.draw_map()

        # FIXME: Uma vez que um player tiver multiplos bots, verificar se todos bots vivos são do mesmo player
        # FIXME: Existe a possibilidade de todos bots terem morrido no mesmo momento. 0 bots vivos
        if len(self.bots) == 1:
            print(f"Player {self.bots[0].player.name} won!")
            exit()

    def start_game(self):
        # FIXME: i dont want to build map, generate players and bots on start game
        self.build_map()

        self.players.extend([Player("1"), Player("2")])

        # TODO: player deveria ser um jogador. e um jogador poderia ter multiplos bots
        self.bots.extend(
            [
                Bot(0, 0, self, self.players[0]),
                Bot(len(self.map[0]) - 1, len(self.map) - 1, self, self.players[1]),
            ]
        )  # TODO: essas posicoes nao deveriam ser fixas

        # TODO: mandar isso pra dentro do objeto Bot
        for bot in self.bots:
            self.map[bot.y][bot.x].append(bot)

        bot_sample1.start()

        put_blocks(self)
        self.draw_map()
