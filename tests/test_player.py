import sys
import os

sys.path.append(os.path.abspath("."))

from src import Engine

engine = Engine()
engine.start_game()
