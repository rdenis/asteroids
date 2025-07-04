# main.py

import sys
from game.engine import GameEngine

def main():
    game_engine = GameEngine()
    game_engine.start()

    while True:
        game_engine.update()
        game_engine.render()

if __name__ == "__main__":
    main()