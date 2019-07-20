from src import engine, put_blocks, bot_sample1, UP, DOWN, LEFT, RIGHT, BOMB, NONE, Bot

if __name__ == "__main__":

    put_blocks(engine)
    engine.draw_map(1)

    for turn in range(2, 501):

        # TODO: this should be an loop throw all bot samples
        bot_sample1.execute_command(
            engine
        )  # FIXME: i cant send the actually _map object, i need to clone it
        command = bot_sample1._last_movement
        bot_sample1._last_movement = NONE

        try:
            bot: Bot = engine.bots[0]
            if command in [UP, DOWN, LEFT, RIGHT]:
                bot.move(command)
                # movements(engine.map, command, engine.bots[0])
            if command in [BOMB]:
                bot.plant_bombs(command)

        except IndexError:
            pass

        engine.bombs.update()
        engine.explosions.update()

        engine.draw_map(turn)

        # FIXME: Uma vez que um player tiver multiplos bots, verificar se todos bots vivos são do mesmo player
        # FIXME: Existe a possibilidade de todos bots terem morrido no mesmo momento. 0 bots vivos
        if len(engine.bots) == 1:
            print(f"Player {engine.bots[0].player.name} won!")
            exit()
