#This module contains the code that implements the game
#logic of othello. It contains 2 classes.


from collections import namedtuple


class InvalidMoveException(Exception):
    '''
    Raised whenever an invalid move is made.
    '''
    pass




class othello:
    '''Represents the current "state" of the Othello game, with methods
    that manipulate the state.'''
    def __init__(self, turn, game_format)-> None:
        '''This functions creates the namedtuple which contains the
        pertinant information of the game.'''
        othello = namedtuple('othello', ['grid', 'turn', 'blacks', 'whites', 'format'])
        self._game = othello(grid = [], turn = turn, blacks = 0, whites = 0, format = game_format)

    def create_grid(self, board: list)-> None:
        '''This function creates the appropriate grid for the game based on the number of
    columns and rows it recieves in its arguments.'''
        grid = board
        self._game = self._game._replace(grid = grid)
        self._total_colors()

    def _player_turn(self)-> None:
        '''This private function changes the players turn within the othello game.'''
        if self._game.turn == 1:
            self._game = self._game._replace(turn = 2)
        else:
            self._game = self._game._replace(turn = 1)

    def whites(self)-> int:
        '''This function returns the number of white pieces present on the board.'''
        return self._game.whites

    def format(self)-> str:
        '''This function returns the type of format of the game which is decided by the user.'''
        return self._game.format

    def blacks(self)-> int:
        '''This function returns the number of black pieces present on the board.'''
        return self._game.blacks

    def grid(self)-> list:
        '''This function returns the grid, which is a list, of the game.'''
        return self._game.grid

    def turn(self)-> int:
        '''This function returns which players turn it is.'''
        return self._game.turn

    def move(self, column: int, row: int)->None:
        '''This function first determines if the desired move by the user is valid, if so,
    the move is made. If not valid, an exception is raised.'''
        while True:
            valid = self._valid_move(column, row)
            if valid == True:
                coordinates = self._make_move(column, row)
                self._adjust_grid(coordinates, column, row)
                self._player_turn()
                self._total_colors()
                break
            else:
                raise InvalidMoveException()

    def _valid_move(self, column: int, row: int)-> bool:
        '''This private function determines if a move is valid or not. If valid, it returns True.
        Otherwise it will return False.'''
        if column >= len(self._game.grid) or column < 0 or row >=len(self._game.grid[0]) or row < 0:
            return False
        if self._game.grid[column][row] != 0:
            return False
        valid = self._make_move(column, row)
        if len(valid) > 0:
            for counter in valid:
                if len(counter)> 0:
                    return True
        return False

    def _total_colors(self)-> None:
        '''This private function counts how many white and black pieces are on the board
        and then updates the namedtuple.'''
        BLACK = 0
        WHITE = 0
        for counter in range(len(self._game.grid)):
            for y in range(len(self._game.grid[0])):
                if self._game.grid[counter][y] == 0:
                    continue
                elif self._game.grid[counter][y] == 1:
                    BLACK += 1
                else:
                    WHITE += 1
        self._game = self._game._replace(blacks = BLACK)
        self._game = self._game._replace(whites = WHITE)

    def _make_move(self, column: int, row: int)-> list:
        '''This private function determines which coordinates of the board are to be
        changed by calling the appropriate functions. A list within a list that contains
        tuples of (x,y) coordinates is returned.'''
        total_coordinates = []
        if (row-2) >= 0:
            total_coordinates.append(self._vertical_changes_backwards(column,row))
        if (row+2) < len(self._game.grid[0]):
            total_coordinates.append(self._vertical_changes_forward(column,row))
        if (column -2 ) >= 0:
            total_coordinates.append(self._horizontal_changes_backwards(column,row))
        if (column + 2) < len(self._game.grid):
            total_coordinates.append(self._horizontal_changes_forward(column,row))
        if (column -2) >= 0 and (row -2) >= 0:
            total_coordinates.append(self._diagonal_negative_change_backwards(column,row))
        if (column + 2) < len(self._game.grid) and (row + 2) < len(self._game.grid[0]):
            total_coordinates.append(self._diagonal_negative_change_forward(column,row))
        if (row - 2 ) >= 0 and (column + 2) < len(self._game.grid):
            total_coordinates.append(self._diagonal_positive_change_forward(column,row))
        if (row + 2) < len(self._game.grid[0]) and (column -2) >= 0:
            total_coordinates.append(self._diagonal_positive_change_backwards(column,row))
        return total_coordinates

    def _adjust_grid(self, coordinates: [[tuple]], column :int, row: int)-> None:
        '''This private function adjusts the grid after a valid
    move by the user is made.'''
        self._game.grid[column][row] = self._game.turn
        for counter in coordinates:
            if len(counter) != 0:
                for y in counter:
                    self._game.grid[y[0]][y[1]] = self._game.turn
        

    def _horizontal_changes_backwards(self,column: int,row : int)-> list:
        '''This private function determines if there needs to be any chanes made to
        the board moving horizontally backwards from the desired spot. An empty list or
        a list of coordinates is returned.'''
        sandwich = []
        coordinates = []
        counter = 0
        if self._game.grid[column-1][row] != self._game.turn:
            while column > 0:
                if counter == 0:
                    counter += 1
                    sandwich.append(self._game.grid[column-1][row])
                    coordinates.append((column-1,row))
                    column -= 2
                else:
                    sandwich.append(self._game.grid[column][row])
                    coordinates.append((column,row))
                    column -= 1
                if (self._game.grid[column][row] == self._game.turn) and (self._game.turn not in sandwich) and (0 not in sandwich):
                    return coordinates
                else:
                       continue
        if len(coordinates) > 0:
            coordinates.clear()
        return coordinates

    def _horizontal_changes_forward(self,column: int, row: int)-> list:
        '''This private function determines if there needs to be any chanes made to
        the board moving horizontally forward from the desired spot. An empty list or
        a list of coordinates is returned.'''
        sandwich = []
        coordinates = []
        counter = 0
        if self._game.grid[column+1][row] != self._game.turn:
            while column < len(self._game.grid)-1:
                if counter == 0:
                    counter += 1
                    sandwich.append(self._game.grid[column+1][row])
                    coordinates.append((column+1, row))
                    column += 2
                else:
                    sandwich.append(self._game.grid[column][row])
                    coordinates.append((column,row))
                    column += 1
                if (self._game.grid[column][row] == self._game.turn) and (self._game.turn not in sandwich) and (0 not in sandwich):
                    return coordinates
                else:
                    continue
        if len(coordinates) > 0:
            coordinates.clear()
        return coordinates

    def _vertical_changes_forward(self,column: int, row: int)-> list:
        '''This private function determines if there needs to be any chanes made to
        the board moving vertically forward from the desired spot. An empty list or
        a list of coordinates is returned.'''
        counter = 0
        coordinates = []
        sandwich = []
        if self._game.grid[column][row + 1] != self._game.turn:
            while row < len(self._game.grid[0])-1:
                if counter == 0:
                    counter += 1
                    sandwich.append(self._game.grid[column][row + 1])
                    coordinates.append((column, row + 1))
                    row += 2
                else:
                    sandwich.append(self._game.grid[column][row])
                    coordinates.append((column,row))
                    row += 1
                if (self._game.grid[column][row] == self._game.turn) and (self._game.turn not in sandwich) and (0 not in sandwich):
                    return coordinates
                else:
                    continue
        if len(coordinates) > 0:
            coordinates.clear()
        return coordinates

    def _vertical_changes_backwards(self,column: int,row: int)-> list:
        '''This private function determines if there needs to be any chanes made to
        the board moving vertically backwards from the desired spot. An empty list or
        a list of coordinates is returned.'''
        counter = 0
        coordinates = []
        sandwich = []
        if self._game.grid[column][row - 1] != self._game.turn:
            while row > 0:
                if counter == 0:
                    counter += 1
                    sandwich.append(self._game.grid[column][row - 1])
                    coordinates.append((column, row - 1))
                    row -= 2
                else:
                    sandwich.append(self._game.grid[column][row])
                    coordinates.append((column,row))
                    row -= 1
                if (self._game.grid[column][row] == self._game.turn) and (self._game.turn not in sandwich) and (0 not in sandwich):
                    return coordinates
                else:
                    continue
        if len(coordinates) > 0:
            coordinates.clear()
        return coordinates

    def _diagonal_positive_change_backwards(self,column: int,row: int)-> list:
        '''This private function determines if there needs to be any chanes made to
        the board moving diagonally backwards, in a positive line, from the desired spot. An empty list or
        a list of coordinates is returned.'''
        counter = 0
        coordinates = []
        sandwich = []
        if self._game.grid[column -1][row+1] != self._game.turn:
            while row < len(self._game.grid[0])-1 and (column) > 0:
                if counter == 0:
                    counter += 1
                    sandwich.append(self._game.grid[column-1][row+1])
                    coordinates.append((column-1, row + 1))
                    row += 2
                    column -= 2
                else:
                    sandwich.append(self._game.grid[column][row])
                    coordinates.append((column,row))
                    row += 1
                    column -= 1
                if (self._game.grid[column][row] == self._game.turn) and (self._game.turn not in sandwich) and (0 not in sandwich):
                    return coordinates
                else:
                    continue
        if len(coordinates) > 0:
            coordinates.clear()
        return coordinates

    def _diagonal_positive_change_forward(self,column: int,row: int)-> list:
        '''This private function determines if there needs to be any chanes made to
        the board moving diagonally forward, in a positive line, from the desired spot. An empty list or
        a list of coordinates is returned.'''
        counter = 0
        coordinates = []
        sandwich = []
        if self._game.grid[column +1][row-1] != self._game.turn:
            while row > 0 and (column) < len(self._game.grid)-1:
                if counter == 0:
                    counter += 1
                    sandwich.append(self._game.grid[column+1][row-1])
                    coordinates.append((column+1, row - 1))
                    row -= 2
                    column += 2
                else:
                    sandwich.append(self._game.grid[column][row])
                    coordinates.append((column,row))
                    row -= 1
                    column += 1
                if (self._game.grid[column][row] == self._game.turn) and (self._game.turn not in sandwich) and (0 not in sandwich):
                    return coordinates
                else:
                    continue
        if len(coordinates) > 0:
            coordinates.clear()
        return coordinates

    def _diagonal_negative_change_forward(self,column: int, row: int)-> list:
        '''This private function determines if there needs to be any chanes made to
        the board moving diagonally forward, in a negative line, from the desired spot. An empty list or
        a list of coordinates is returned.'''
        counter = 0
        sandwich = []
        coordinates = []
        if self._game.grid[column +1][row+1] != self._game.turn:
            while row < len(self._game.grid[0])-1 and (column) < len(self._game.grid)-1:
                if counter == 0:
                    counter += 1
                    sandwich.append(self._game.grid[column+1][row+1])
                    coordinates.append((column+1, row + 1))
                    row += 2
                    column += 2
                else:
                    sandwich.append(self._game.grid[column][row])
                    coordinates.append((column,row))
                    row += 1
                    column += 1
                if (self._game.grid[column][row] == self._game.turn) and (self._game.turn not in sandwich) and (0 not in sandwich):
                    return coordinates
                else:
                    continue
        if len(coordinates) > 0:
            coordinates.clear()
        return coordinates

    def _diagonal_negative_change_backwards(self,column: int, row: int)-> list:
        '''This private function determines if there needs to be any chanes made to
        the board moving diagonally backwards, in a negative line, from the desired spot. An empty list or
        a list of coordinates is returned.'''
        counter = 0
        sandwich = []
        coordinates = []
        if self._game.grid[column -1][row-1] != self._game.turn:
            while row > 0 and (column) > 0:
                if counter == 0:
                    counter += 1
                    sandwich.append(self._game.grid[column-1][row-1])
                    coordinates.append((column-1, row -1))
                    row -= 2
                    column -= 2
                else:
                    sandwich.append(self._game.grid[column][row])
                    coordinates.append((column,row))
                    row -= 1
                    column -= 1
                if (self._game.grid[column][row] == self._game.turn) and (self._game.turn not in sandwich) and (0 not in sandwich):
                    return coordinates
                else:
                    continue
        if len(coordinates) > 0:
            coordinates.clear()
        return coordinates

    def available_moves(self)->bool:
        '''This function determines if there are any moves that can be made
    on the game board. If yes, True is returned. Otherwise it returns False.'''
        empty_spots = []
        for x in range(len(self._game.grid)):
            for y in range(len(self._game.grid[0])):
                if self._game.grid[x][y] == 0:
                    empty_spots.append((x,y))

        if len(empty_spots) != 0:
            for z in empty_spots:
                valid = self._valid_move(z[0], z[1])
                if valid == True:
                    return True
                else:
                    continue
            self._player_turn()
            for counter in empty_spots:
                valid = self._valid_move(z[0], z[1])
                if valid == True:
                    return True
                else:
                    continue
        
        else:
            return False
        return False

    def winner(self)->int:
        '''This function returns the winner of the game.'''
        if self._game.whites == self._game.blacks:
            return 0
        else:
            if self._game.format == '>':
                if self._game.blacks > self._game.whites:
                    return 1
                else:
                    return 2
            else:
                if self._game.blacks < self._game.whites:
                    return 1
                else:
                    return 2






    
