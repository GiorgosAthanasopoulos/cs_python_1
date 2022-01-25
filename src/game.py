import board, utils, time # for Board class, for util methods, for sleep(seconds)

class Game:
    DRAW = 1

    def __init__(self):
        self.turn = '1'
        self.pawn = 'O'
        self.winner = None

    def start(self):
        utils.greet_player()
        self.load_or_create_game()

        while True:
            self.play_round()
            self.ask_continue()

    def load_or_create_game(self): # ask for user whether or not to load saved game or create new
        load_or_new = utils.check_input('Do you want to load a saved game (S) or start a new one (N)? (S or N): ', lambda letter: letter == 'N' or letter == 'S', 'Invalid input (input must be either the letter "N" or the letter "S")')
        self.size, self.score_o, self.score_x, self.board = utils.create_new_game() if load_or_new == 'N' else utils.load_game()

    def show_win_screen(self): # if someone won show them a message with the score
        self.board.mark_winner_line()
        print('\n' + str(self.board))
        if self.winner != self.DRAW: 
            extra_points = self.board.remove_winner_pieces(self.winner)
            if self.winner == 'O': self.score_o += extra_points
            elif self.winner == 'X': self.score_x += extra_points
        print(f'Winner: {self.winner if self.winner != self.DRAW else "Draw"}')
        print(f'Score: {self.score_o}-{self.score_x}')
        time.sleep(2)

        self.turn, self.pawn = ('1', 'O')

    def play_round(self): # play 1 round of the game
        self.winner = self.board.check_for_shifted_win()

        if self.winner != None:
            self.show_win_screen()
            return

        for i in range(2):
            print('\n' + str(self.board))

            while True:
                placement_choice = utils.check_input(f'Player {self.turn}: enter column to place your pawn in: ', lambda x: 1 <= x <= self.size, f'Invalid input (input must be an integer between 1 and {self.size})', int)
                if self.board.insert(self.pawn, placement_choice) == board.Board.INSERTION_SUCCESS: break
                print(f'The column you chose is full!')

            self.turn, self.pawn = ('2', 'X') if self.turn == '1' else ('1', 'O')
            self.winner = self.board.get_winner()

            if self.board.is_full(): self.winner = self.DRAW
            if self.winner == 'O' or self.winner == 'X' or self.winner == self.DRAW:
                self.show_win_screen()
                return

        print('\n' + str(self.board))

    def ask_continue(self): # after each round ends or after a player wins, ask the players whether they want to continue or not
        key = input('Press q to quit game without saving\nPress s to save and quit game\nPress any other button to continue: ')
        if key == 's': utils.save_game(self.size, self.score_o, self.score_x, self.board.get_data())
        if key == 's' or key == 'q': exit(0)
