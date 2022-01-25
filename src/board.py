class Board:
    INSERTION_SUCCESS, INSERTION_COLUMN_FULL, INSERTION_OUT_OF_BOUNDS = 0, 1, 2

    def __init__(self, size):
        if size < 5 or size > 10:
            raise ValueError('Invalid size')
        self.size = size
        self.reset()

    # Removes every piece from the board
    # Called before a new round begins
    def reset(self):
        # self.last_insertion keeps track of the position of the previously inserted piece
        # That way we don't need to check every single row and column to see if a line was formed,
        # we can just check if the previous insertion lead to a line being formed
        self.last_insertion = (-1, -1)
        self.win_positions = []
        self.board = [ [' '] * self.size for i in range(self.size) ]

    # This function is 1-indexed, meaning the first column is 1 not 0
    # If the column is not between 1 and self.size (inclusive), the insertion fails and returns INSERTION_OUT_OF_BOUNDS
    # If the column is full, the insertion fails and the function returns INSERTION_COLUMN_FULL
    # Otherwise the character is placed at the bottom of the specified column and returns INSERTION_SUCCESS
    def insert(self, char, column):
        if column <= 0 or column > self.size: 
            return self.INSERTION_OUT_OF_BOUNDS

        column -= 1 # Arrays are zero-indexed so we have to decrement this
        row_to_insert = self.size - 1 # Assume character can be placed at the bottom row

        for row in range(self.size):
            # If all characters are whitespaces, then the previously mentioned assumption is correct and nothing changes
            # If a non-whitespace character is found, that means that the column isn't empty,
            # therefore we choose to insert the new character one row above the character at the top of the column
            if self.board[row][column] != ' ':
                row_to_insert = row - 1
                break

        # If a non-whitespace character is found in the top row in the previous loop, then
        # row_to_insert = row - 1 is equal to row_to_insert = 0 - 1
        if row_to_insert == -1: return self.INSERTION_COLUMN_FULL

        self.board[row_to_insert][column] = char
        self.last_insertion = (row_to_insert, column)
        return self.INSERTION_SUCCESS

    # If there exists a line of four identical characters, returns the forementioned character
    # Otherwise returns None
    def get_winner(self):
        # (-1, -1) is the initial value assigned in reset()
        # So if last_insertion is equal to that, nobody has won yet because the board is empty
        if self.last_insertion == (-1, -1): return None

        prev_row = self.last_insertion[0]
        prev_col = self.last_insertion[1]
        last_char = self.board[prev_row][prev_col]

        # If there are 4 identical characters one after the other at the positions
        # given by the sequence, then the function returns the indexes of each piece
        # This is done so we can mark each character with a star '*' in mark_winner_line
        # If no such pattern is found, returns None
        def find_line(board, char, sequence):
            count = 0
            positions = []
            for (row, col) in sequence:
                if char == board[row][col]:
                    count += 1
                    positions.append((row, col))
                    if count == 4: return positions
                else:
                    count = 0
                    positions.clear()
            return None

        def same_sequence(x):
            while True: yield x

        min_dist_to_axes = min(prev_col, prev_row)

        # Used to calculate the first and last position of the bottom-left to top-right sequence later
        diagonal_end_row = self.size - 1
        diagonal_end_col = 0 if (prev_col + prev_row) < self.size else (prev_col + prev_row) - diagonal_end_row

        point_sequences = []

        # Horizontal sequence
        point_sequences.append(zip(same_sequence(prev_row), range(self.size)))

        # Vertical sequence
        point_sequences.append(zip(range(self.size), same_sequence(prev_col)))

        # Diagonal sequence (top-left to bottom-right)
        point_sequences.append(zip(range(prev_row - min_dist_to_axes, self.size),
                                   range(prev_col - min_dist_to_axes, self.size)))

        # Diagonal sequence (bottom-left to top-right)
        point_sequences.append(zip(range(diagonal_end_col, diagonal_end_row + 1),
                                   range(diagonal_end_row, diagonal_end_col - 1, -1)))

        for seq in point_sequences:
            line = find_line(self.board, last_char, seq)
            if line != None:
                self.win_positions = line
                return last_char

        return None
    
    # Removes the pieces that form a line of four, as well as the pieces
    # that are right beside them (diagonally, vertically and horizontally)
    # As a side effect, all the pieces that were above the removed ones
    # are shifted downwards until they reach the bottom
    def remove_winner_pieces(self, piece):
        # Gets the n <= 8 characters that are around each 
        # character of the winner's line, so that we can remove them
        # as well if they are the same as the winner's character
        def get_neighbour_pieces(piece, row, column):
            pieces = []
            for r in range(max(0, row - 1), min(self.size, row + 2)):
                for c in range(max(0, column - 1), min(self.size, column + 2)):
                    if (r, c) != (row, column) and (self.board[r][c] == piece): 
                        pieces.append((r, c))
            return pieces

        def shift_row_down(column):
            # Parameter: the row that a space character is found
            # Moves all the characters above the space 1 spot down
            # and places a space character at the top
            def move_down(row_of_space):
                for row in range(row_of_space - 1, -1, -1): 
                    self.board[row + 1][column] = self.board[row][column]
                self.board[0][column] = ' '

            # Becuase there can be more than 1 space characters in a row,
            # and they don't even have to be in continuous rows, we have
            # to keep moving down the row until all the spaces are gone
            for row in range(self.size - 1, -1, -1):
                space_count = 0
                while self.board[row][column] == ' ':
                    move_down(row)
                    space_count += 1
                    if space_count >= self.size: 
                        break

        count = 0
        for row, column in self.win_positions:
            # We have called mark_winner_line before calling this, so we have to include the star character as well
            neighbours = get_neighbour_pieces(piece, row, column) + get_neighbour_pieces('*', row, column)
            for r, c in neighbours:
                self.board[r][c] = ' '
                count += 1
        
        for column in range(self.size): 
            shift_row_down(column)

        return count


    # Checks if a line has been created near each character of the winner's line
    def check_for_shifted_win(self):
        if self.win_positions == []: 
            return
    
        for (row, col) in self.win_positions.copy(): 
            for i in range(self.size): 
                self.win_positions.append((row, i))

        for (row, col) in set(self.win_positions):
            if self.board[row][col] != ' ':
                self.last_insertion = (row, col) # Used in get_winner()
                winner = self.get_winner()
                if winner != None: 
                    return winner

        # Once we reach this point, there are no more lines created by a shift
        # So we can just forget the winner positions (runs faster because of the first if in this function)
        self.win_positions.clear()

    def is_full(self):
        return ' ' not in self.board[0]

    def mark_winner_line(self):
        for row, column in self.win_positions: self.board[row][column] = '*'
    
    def get_data(self):
        return self.board

    def set_data(self, data): # Data must be a a list that contains self.size lists, that contain self.size characters
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

        return repr + dotted_line