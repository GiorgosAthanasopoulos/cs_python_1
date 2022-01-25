import board, os # for the Board class, for file i/o

def check_input(msg, is_correct, err_msg, conversion_type=str): # equivalent to === in javascript
    while True:
        user_input = input(msg).strip()
        try:
            user_input = conversion_type(user_input)
            if is_correct(user_input): return user_input
        except: pass
        print(err_msg)

def greet_player(): print('Welcome to the game!') # when starting the game show a welcome text to the players

def create_new_game(): # create new game class, instanciate board class and set scores to 0 (and input Board.size from user)
    temp_size = check_input('Enter board size (integer between 5 and 10 - inclusive): ', lambda size: 5 <= size <= 10, 'Invalid input (input must be an integer between 5 and 10 (incusive)) ', int)
    return [temp_size, 0, 0, board.Board(temp_size)]

def load_game(): # if prompted to, load game from csv file
    filename = check_input('Enter save filename: ', lambda filename: os.path.exists(filename if filename.endswith('.csv') else filename+'.csv'), 'File not found.')
    filename += '.csv' if not filename.endswith('.csv') else ''

    temp_board = []
    with open(filename, 'r') as file: 
        for index, line in enumerate(file.readlines()):
            raw = line.replace('\n', '').split(',')

            if len(raw) > 2: temp_board.append(raw)
            else: score_o_, score_x_ = int(raw[0]), int(raw[1])

    board_ = board.Board(len(temp_board[0]))
    board_.set_data(temp_board)

    return [len(temp_board[0]), score_o_, score_x_, board_]

def save_game(size, score_o, score_x, board_): # save game if prompted, to a csv like formatted text document
    filename = check_input('Enter filename: ', lambda file: True, 'Wrong filename')
    filename += '.csv' if not filename.endswith('.csv') else ''

    with open(filename, 'w') as file:
        for i in range(size): print(','.join(board_[i]), file=file)
        print(score_o, score_x, sep=",", file=file)
    print('Game saved!')