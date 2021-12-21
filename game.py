from utils import *


class Game:
    def __init__(self):
        self.game_board = None

    def start(self):  # main game handler
        self.game_board = start_up_job()
