import board
import utils
import time
import os


class Game:
    def __init__(self):
        self.turn = '1'
        self.pawn = 'O'
        self.winner = None

    def start(self):
        utils.greet_player()
        self.load_or_create_game()

        while self.winner == None:
            self.play_round()
            self.ask_continue()

    def load_or_create_game(self):
        load_or_new = utils.check_input(
            'Do you want to load a saved game(S) or start a new one(N)? (S or N): ',
            lambda letter: letter == 'N' or letter == 'S',
            'Incorrect input(input must be either the letter "N" or the letter "S")'
        )

        self.size, self.score_o, self.score_x, self.board = utils.create_new_game(
        ) if load_or_new == 'N' else utils.load_game()

    def play_round(self):
        for i in range(2):
            print(self.board)

            placement_choice = utils.check_input(
                f'Player {self.turn}: enter column to place your pawn in: ',
                lambda placement_choice_: 1 <= placement_choice_ <= self.size and self.board.insert(
                    self.pawn, placement_choice_) == 0,
                f'Incorrect input(input must be an integer between 1 and {self.size})',
                int
            )

            self.turn, self.pawn = (
                '2', 'X') if self.turn == '1' else ('1', 'O')

            self.winner = self.board.get_winner()

            if self.winner == 'O':
                self.score_o += 1
            elif self.winner == 'X':
                self.score_x += 1
            elif utils.is_board_full(self.board):
                    self.winner = 1

            if self.winner == 'O' or self.winner == 'X' or self.winner == 1:
                self.board.mark_winner_line()
                print(self.board)
                print(f'Winner: {self.winner if self.winner != 1 else "Draw"}')

                time.sleep(2)
                self.board.reset()
                self.turn, self.pawn = ('1', 'O')
                return

        print(self.board)

    def ask_continue(self):
        key = input(
            'Press any key to continue\nIf you want to exit and save the game press "s": ')

        if key == 's':
            print('s')
            utils.save_game(self.size, self.score_o,
                            self.score_x, self.board.get_data())
            exit(0)
