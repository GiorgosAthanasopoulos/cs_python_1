class Board:
    INSERTION_SUCCESS = 0
    INSERTION_COLUMN_FULL = 1
    INSERTION_OUT_OF_BOUNDS = 2

    def __init__(self, size):
        if size < 5 or size > 10:
            raise ValueError('Invalid size')
        self.size = size
        self.reset()


    def reset(self):
        # Keep track of the position of the inserted piece
        # That way we only check if the insertion of the last piece created a line
        self.last_insertion = (-1, -1)
        self.win_positions = []
        self.board = [ [' '] * self.size for i in range(self.size) ]

    def insert(self, char, column):
        """
        Inserts a character in the specified column

        >>> board = Board(5)
        >>> board.insert('X', 1)
        0
        >>> board.insert('O', 0)
        2
        >>> board.insert('O', 1)
        0
        >>> board.insert('X', 1)
        0
        >>> board.insert('O', 1)
        0
        >>> board.insert('X', 1)
        0
        >>> board.insert('O', 1)
        1
        >>> board.insert('X', -100)
        2
        """
        if column <= 0 or column > self.size:
            return self.INSERTION_OUT_OF_BOUNDS

        column -= 1
        row_to_insert = self.size - 1
        for row in range(self.size):
            if self.board[row][column] != ' ':
                row_to_insert = row - 1
                break

        if row_to_insert == -1:
            return self.INSERTION_COLUMN_FULL

        self.board[row_to_insert][column] = char
        self.last_insertion = (row_to_insert, column)
        return self.INSERTION_SUCCESS

    # If the last insertion caused created a 4-piece sequence, returns the winner's character
    # Otherwise returns None
    def get_winner(self):
        """
        >>> board = Board(5)
        >>> board.get_winner() == None
        True
        >>> board.insert('X', 1)
        0
        >>> board.insert('X', 1)
        0
        >>> board.insert('X', 1)
        0
        >>> board.insert('X', 1)
        0
        >>> board.get_winner() == 'X'
        True
        """
        if self.last_insertion == (-1, -1):
            return None
        prev_row = self.last_insertion[0]
        prev_col = self.last_insertion[1]
        last_char = self.board[prev_row][prev_col]

        def find_line(board, char, sequence):
            count = 0
            positions = []
            for (row, col) in sequence:
                if char == board[row][col]:
                    count += 1
                    positions.append((row, col))
                    if count == 4:
                        return positions
                else:
                    count = 0
                    positions.clear()
            return None

        def same_sequence(x):
            while True:
                yield x

        min_dist_to_axes = min(prev_col, prev_row)

        diagonal_end_y = self.size - 1
        diagonal_end_x = 0 if (prev_col + prev_row) < self.size else (prev_col + prev_row) - diagonal_end_y

        point_sequences = []
        # Horizontal sequence
        point_sequences.append(zip(same_sequence(prev_row), range(self.size)))
        # Vertical sequence
        point_sequences.append(zip(range(self.size), same_sequence(prev_col)))
        # Diagonal sequence (top-left to bottom-right)
        point_sequences.append(zip(range(prev_row - min_dist_to_axes, self.size),
                                   range(prev_col - min_dist_to_axes, self.size)))
        # Diagonal sequence (bottom-left to top-right)
        point_sequences.append(zip(range(diagonal_end_x, diagonal_end_y + 1),
                                   range(diagonal_end_y, diagonal_end_x - 1, -1)))

        for seq in point_sequences:
            line = find_line(self.board, last_char, seq)
            if line != None:
                self.win_positions = line
                return last_char

        return None


    def mark_winner_line(self):
        for row, column in self.win_positions:
            self.board[row][column] = '*'


    def get_data(self):
        return self.board


    def set_data(self, data):
        self.board = data
        

    def __str__(self):
        repr = ""
        dotted_line = '-' * (self.size * 5 + 2)
        for i in range(self.size):
            repr += "    " + str(i + 1)

        repr += '\n' + dotted_line + '\n'
        for row in range(self.size):
            repr += "ABCDEFGHIJ"[row] + '|'
            for col in range(self.size):
                repr += f'  {self.board[row][col]} |'
            repr += '\n'

        repr += dotted_line
        return repr
