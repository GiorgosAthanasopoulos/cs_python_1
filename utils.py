def start_up_job(self):
    greet_players()
    mode = get_game_mode()

    if mode == 'N':
        game_board = create_game_board()
    else:
        game_board = load_game()

    return game_board


def greet_players():
    print('Καλωσήλθατε στο παιχνίδι!')


def get_game_mode():
    def cond(x):
        return x == 'N' or x == 'S'

    mode = check_input('Επιθυμείτε νέο παιχνίδι (N) ή φόρτωση παιχνιδιού από αρχείο (S): ',
                       'Η επιλογή δεν είναι σωστή(N ή S)...Προσπαθήστε ξανά', cond)

    return mode


def check_input(msg, err_msg, cond):
    res = input(msg)
    while not cond(res):
        print(err_msg)
        res = input(msg)

    return res


def create_game_board():
    def cond(x):
        return 5 <= x <= 10

    rows = columns = int(check_input('Δώστε αριθμό στηλών παιχνιδιού (5-10): ',
                                     'Ο αριθμός στηλών δεν είναι έγκυρος (5-10)...Προσπαθήστε ξανά!', cond))

    game_board = [[' '] * columns] * rows

    return game_board


def load_game():
    def cond(x):
        import os
        return os.path.isfile(x)

    filepath = check_input('Δώστε όνομα αρχείου: ',
                           'Το αρχείο δεν υπάρχει...Προσπαθήστε ξανά!', cond)

    game_board = create_game_board()

    with open(f'{filepath}', 'r') as f:
        pass
