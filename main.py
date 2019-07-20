from src import Engine

if __name__ == "__main__":
    engine = Engine()
    engine.start_game()

    for _ in range(2, 501):
        engine.next_turn()
