from src.engine import Engine
from src.objects.player import Player
from src.bot_sample import BotSample
from src.objects.block import put_blocks, Block
from src.objects.wall import Wall
from src.objects.bomb import Bomb


class BotSample1(BotSample):
    def start(self):
        self.commands = []

    def is_place_safe(self, my_cell):
        if not self.engine.bombs:
            return True

        self.unsafe_places = []

        for bomb in self.engine.bombs:
            cell = bomb.get_cell()
            self.unsafe_places.append(cell)

            cell_aux = cell
            try:
                for _ in range(2):
                    cell_aux = cell_aux.up
                    if cell_aux == None:
                        raise ValueError("null")
                    self.unsafe_places.append(cell_aux)
            except:
                pass

            cell_aux = cell
            try:
                for _ in range(2):
                    cell_aux = cell_aux.down
                    if cell_aux == None:
                        raise ValueError("null")
                    self.unsafe_places.append(cell_aux)
            except:
                pass

            cell_aux = cell
            try:
                for _ in range(2):
                    cell_aux = cell_aux.left
                    if cell_aux == None:
                        raise ValueError("null")
                    self.unsafe_places.append(cell_aux)
            except:
                pass

            cell_aux = cell
            try:
                for _ in range(2):
                    cell_aux = cell_aux.right
                    if cell_aux == None:
                        raise ValueError("null")
                    self.unsafe_places.append(cell_aux)
            except:
                pass

        if my_cell not in self.unsafe_places:
            return True

        print([(c.x, c.y) for c in self.unsafe_places])
        print("procurando algum lugar")
        self.search_safe_place()
        return False

    def execute_command(self, engine, myself):
        self.engine = engine
        self.mybot = myself.bots[0]
        self.myself = myself
        qtd_bomb = 0

        if not self.commands:

            if not self.is_place_safe(self.mybot.get_cell()):
                if self.commands:
                    self.commands.pop(0)()
                return

            for bomb in self.engine.bombs:
                if self.myself == bomb.owner.player:
                    qtd_bomb += 1

            if self.myself.bombs_limit != qtd_bomb:
                self.look_for_block()

        else:
            self.commands.pop(0)()

    def look_cell(self, cell, searching_for):

        if cell.x == 1 and cell.y == 0:
            print("PUTA QUE PARIU")

        for _object in cell:
            if isinstance(_object, Wall):
                return None
            if isinstance(_object, Bomb):
                return None
            if isinstance(_object, Block):
                if searching_for == "block":
                    return cell
                return None

        if searching_for == "safe_place" and cell not in self.unsafe_places:
            print("achei uma celula mds")
            return cell

        searched_cell = self.search_around_cell(cell, searching_for)
        if searched_cell is not None:
            return searched_cell

    def search_around_cell(self, cell, searching_for):
        if cell.up is not None and cell.up not in self.already_looked:
            print("fui pra cima")
            self.already_looked.append(cell.up)
            searched_cell = self.look_cell(cell.up, searching_for)
            if searched_cell is not None:
                self.commands.insert(0, self.go_up)
                return cell
        if cell.down is not None and cell.down not in self.already_looked:
            print("fui pra baixo")
            self.already_looked.append(cell.down)
            searched_cell = self.look_cell(cell.down, searching_for)
            if searched_cell is not None:
                self.commands.insert(0, self.go_down)
                return cell
        if cell.left is not None and cell.left not in self.already_looked:
            print("fui pra esquerda")
            self.already_looked.append(cell.left)
            searched_cell = self.look_cell(cell.left, searching_for)
            if searched_cell is not None:
                self.commands.insert(0, self.go_left)
                return cell
        if cell.right is not None and cell.right not in self.already_looked:
            print("fui pra direita")
            self.already_looked.append(cell.right)
            searched_cell = self.look_cell(cell.right, searching_for)
            if searched_cell is not None:
                self.commands.insert(0, self.go_right)
                return cell

    def look_for_block(self):
        cell = self.mybot.get_cell()
        self.already_looked = [cell]
        self.commands = []
        self.search_around_cell(cell, "block")
        self.commands.pop(-1)
        self.commands.append(self.put_bomb)
        self.commands.pop(0)()

    def search_safe_place(self):
        cell = self.mybot.get_cell()
        self.already_looked = [cell]
        self.commands = []
        self.search_around_cell(cell, "safe_place")
        print(self.commands)


if __name__ == "__main__":
    engine = Engine()
    engine.build_map()
    engine.create_walls()
    player_1 = Player("1", BotSample1())
    player_2 = Player("2", BotSample1())
    engine.add_player(player_1)
    engine.add_player(player_2)
    engine.add_bot(player_1, 0, 0)
    y, x = engine.map.shape
    engine.add_bot(player_2, x - 1, y - 1)
    put_blocks(engine)
    file = open("replay_files/replay.data", "wb")
    engine.start_game(file)

    try:
        for _ in range(2, 501):
            engine.next_turn()
    except Exception as e:
        print(e)

    file.close()
