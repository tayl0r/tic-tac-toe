import random
import time


class TicTacToeGame:
    # game config
    TOP_BOTTOM_OUTLINE_CHAR = '# '
    LEFT_OUTLINE_CHAR = '# '
    RIGHT_OUTLINE_CHAR = ' #'
    COL_SEP_CHAR = ' | '
    PLAYER_SYMBOLS = ['X', 'O', 'A', 'B', 'C', 'D']  # must not be numbers
    SECS_BETWEEN_TURNS = .5
    IS_BOARD_FULL_CHAR = "-1"

    cols = 0
    rows = 0
    num_players = 0
    board = [[]]
    moves_count = 0
    human_turn_idx = 0

    def __init__(self, cols, rows, num_players):
        self.cols = cols
        self.rows = rows
        self.num_players = num_players
        if self.num_players > len(self.PLAYER_SYMBOLS):
            raise ValueError(f'{num_players} is greater than maximum of {len(self.PLAYER_SYMBOLS)} players.')

        # initialize board with numbers, 1-9
        self.board = [[" "] * cols for _ in [" "] * rows]
        i = 0
        for c in range(self.cols):
            for r in range(self.rows):
                i += 1
                self.board[c][r] = str(i)

        print(f'Welcome to Tic Tac Toe! We are playing with {num_players} players on a {cols} x {rows} board.')

        # figure out if the player goes first or second
        going_first_input = input('Type "1" if you want to go first, anything else for second. ')
        if going_first_input == '1' or going_first_input == '"1"':
            print('You will go first!')
            self.human_turn_idx = 0
        else:
            print('You will go second! Very bold =)')
            self.human_turn_idx = 1

        print('')

        # start the game loop!
        while self.find_winner() == '':
            self.next_move()
            time.sleep(self.SECS_BETWEEN_TURNS)

        winner_symbol = self.find_winner()
        self.end_game(winner_symbol)

    def print_board(self, should_print_cell_indexes=False):
        # print the top board outline
        print(f'{self.TOP_BOTTOM_OUTLINE_CHAR}'
              f'{self.TOP_BOTTOM_OUTLINE_CHAR * (self.cols * 2 - 1)}'
              f'{self.TOP_BOTTOM_OUTLINE_CHAR}')

        # print the actual game board
        for c in range(self.cols):
            col_chars = self.board[c]
            if not should_print_cell_indexes:
                col_chars = map(lambda val: ' ' if val.isdigit() else val, col_chars)
            print(f'{self.LEFT_OUTLINE_CHAR}{self.COL_SEP_CHAR.join(col_chars)}{self.RIGHT_OUTLINE_CHAR}')

        # print the bottom board outline
        print(f'{self.TOP_BOTTOM_OUTLINE_CHAR}'
              f'{self.TOP_BOTTOM_OUTLINE_CHAR * (self.cols * 2 - 1)}'
              f'{self.TOP_BOTTOM_OUTLINE_CHAR}')

    def next_move(self):
        # what symbol goes next?
        current_turn_idx = self.moves_count % self.num_players
        current_symbol = self.PLAYER_SYMBOLS[current_turn_idx]
        print(f'\nTurn #{self.moves_count + 1}. {current_symbol} goes next!')
        # is it the human player turn?
        if current_turn_idx == self.human_turn_idx:
            # yes, player's turn
            self.get_player_move(current_turn_idx)
        else:
            self.get_ai_move(current_turn_idx)

        self.moves_count += 1
        print('')
        self.print_board()

    def get_player_move(self, turn_idx):
        self.print_board(True)
        grid_selection = input('Input the cell number you want to mark with your '
                               f'{self.PLAYER_SYMBOLS[turn_idx]}: ')
        # find the board element with this same value
        is_valid_input = False
        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[c][r] == grid_selection:
                    # got it, set this symbol to our player symbol
                    self.board[c][r] = self.PLAYER_SYMBOLS[turn_idx]
                    is_valid_input = True
                    break

        if not is_valid_input:
            self.get_player_move(turn_idx)

    def get_ai_move(self, turn_idx):
        # randomly pick a cell
        while True:
            c = random.randrange(0, self.cols)
            r = random.randrange(0, self.rows)
            if self.board[c][r].isdigit():
                self.board[c][r] = self.PLAYER_SYMBOLS[turn_idx]
                break

    def find_winner(self):
        # strategy: go through each column, each row, then the diagonals
        # if every symbol is the same, we have a winner

        # check each column
        for c in range(self.cols):
            winner = self.check_column_for_winner(c)
            if winner != '':
                return winner

        # check each row
        for r in range(self.rows):
            winner = self.check_row_for_winner(r)
            if winner != '':
                return winner

        # check diagonals
        winner = self.check_top_left_diagonal_for_winner()
        if winner != '':
            return winner

        winner = self.check_top_right_diagonal_for_winner()
        if winner != '':
            return winner

        # check if all our cells are filled, and we don't have a winner yet
        is_board_full = True
        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[c][r].isdigit():
                    is_board_full = False
        if is_board_full:
            return self.IS_BOARD_FULL_CHAR

        return ''

    # if all vals are the same, we have a winner
    @staticmethod
    def check_values_for_winner(vals):
        current_symbol = vals[0]
        for val in vals:
            if current_symbol != val:
                return ''

        # winner!
        return current_symbol

    def check_column_for_winner(self, col):
        vals = []
        for r in range(self.rows):
            vals.append(self.board[col][r])
        return self.check_values_for_winner(vals)

    def check_row_for_winner(self, row):
        vals = []
        for c in range(self.cols):
            vals.append(self.board[c][row])
        return self.check_values_for_winner(vals)

    def check_top_left_diagonal_for_winner(self):
        vals = []
        r = 0
        for c in range(self.cols):
            vals.append(self.board[c][r])
            r += 1
        return self.check_values_for_winner(vals)

    def check_top_right_diagonal_for_winner(self):
        vals = []
        r = 0
        for c in reversed(range(self.cols)):
            vals.append(self.board[c][r])
            r += 1
        return self.check_values_for_winner(vals)

    def end_game(self, winner_symbol):
        if winner_symbol == self.PLAYER_SYMBOLS[self.human_turn_idx]:
            print(f'\n!!! GAME OVER !!!\n{winner_symbol} is the winner!\n')
            print('YOU WON!!')
        elif winner_symbol == self.IS_BOARD_FULL_CHAR:
            print(f'\n!!! GAME OVER !!!\n')
            print('NO WINNER =(')
        else:
            print(f'\n!!! GAME OVER !!!\n{winner_symbol} is the winner!\n')
            print('YOU LOST =(')
