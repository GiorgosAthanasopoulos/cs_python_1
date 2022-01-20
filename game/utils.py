import board

def is_board_full(board):
    return ' ' not in board.get_data()[0]

# function that checks user input (type, range if num, etc.)
def check_input(msg, correct, err_msg, type_=str):
    while True:
        input_ = input(msg).strip()
        try:
            input_ = type_(input_)
            if correct(input_):
                return input_
        except:
            pass
        print(err_msg)

def greet_player():
    print('Welcome to the game!')

# if prompted with 'N' in load_or_create_game create new game and initialize correct values to variables
def create_new_game():
    data = []

    temp_size = check_input(
        'Enter board size: ',
        lambda size: 5 <= size <= 10,
        'Incorrect input(input must be an integer between 5 and 10(inclusive))',
        int
    )
    data.append(temp_size)

    data.append(0)
    data.append(0)

    data.append(board.Board(data[0]))

    return data

# if prompted with 'S' in load_or_create_game load saved game
def load_game():
    import os

    filename = check_input(
        'Enter save filename: ',
        lambda filename: os.path.exists(filename if filename.endswith('.csv') else filename+'.csv'),
        'Incorrect input(Could be due to the file missing or the file being located in a different folder than the one the program runs in)'
    )
    filename += '.csv' if not filename.endswith('.csv') else ''

    data = [0,0,0]
    temp_board = []

    with open(filename, 'r') as file:
        for index, line in enumerate(file.readlines()):
            raw = line.replace('\n', '').split(',')
            if len(line.replace('\n', '')) > 3:
                if index == 0:
                    data[0] = len(raw)
                temp_board.append(raw)
            else:
                data[1], data[2] = raw

    data.append(board.Board(data[0]))
    data[3].set_data(temp_board)

    data[1], data[2] = int(data[1]), int(data[2])

    return data

# save game to file if prompted with 's' in ask_continue
def save_game(size, score_o, score_x, board):
    filename = check_input(
        'Enter filename: ',
        lambda file: True,
        'Wrong filename'
    )
    filename += '.csv' if not filename.endswith('.csv') else ''

    with open(filename, 'w') as file:
        for i in range(size):
            print(','.join(board[i]), file=file)
        print(score_o, score_x, sep=",", file=file)
