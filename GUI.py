import tkinter
from othello import othello

class Othello_GUI:
    '''This class contains the entire gameplay of Othello. It acquires the necessary
    functions from class 'othello' and class 'Othello_Options' to make the game function
    accordingly. The layout of the board, labels, and buttons are all handeled within this
    class.'''
    def __init__(self)-> None:
        options_menu = GUI_Options()
        options_menu.run()
        self._move_on = options_menu.get_signal()
        if self._move_on == True:
            self._rows = int(options_menu.get_rows())
            self._columns = int(options_menu.get_columns())
            self._gameplay = options_menu.get_gameplay()
            self._first_turn = options_menu.get_first_player()
            self._player = 'Black'
            self._game = othello(self._first_turn, self._gameplay)
            self._window = tkinter.Tk()
            self._top_frame = tkinter.Frame(master = self._window)
            self._top_frame.grid(row = 0, column = 0, columnspan = self._columns, padx = 0, pady = 0,
                                 sticky = tkinter.S + tkinter.N)
            self._top_frame.columnconfigure(1, weight = 1)
            self._game_type_label = tkinter.Label(master = self._top_frame, text = 'Othello\nFULL', font = ('ariel', 10))
            self._game_type_label.grid(row = 0, column = 0)
            self._text = tkinter.StringVar()
            self._text.set('Populate Board: Black')
            self._label = tkinter.Label(master = self._top_frame, textvariable = self._text,
                              font = ('Ariel', 24, 'bold'), anchor = 'center')
            self._label.grid(row = 0, column = 1)
            self._count_text = tkinter.StringVar()
            self._count_text.set('{}: 0 {}: 0'.format('Black', 'White'))
            self._bottom_frame = tkinter.Frame(master = self._window)
            self._bottom_frame.grid(row = self._rows + 2, column = 0, columnspan = self._columns, padx = 0, pady = 0,
                                    sticky = tkinter.S + tkinter.N)
            self._count_label = tkinter.Label(master = self._bottom_frame, textvariable = self._count_text,
                                              font = ('Ariel', 24, 'bold'), anchor = 'center')
            self._count_label.grid(row = 0, column = 0, columnspan = self._columns, sticky = tkinter.S)
            self._bottom_frame.rowconfigure(0, weight = 1)
            self._canvases = {}
            self._post_populate_grid = []
            self._grid = []
            self._create_grid()
            self._circle = (0.15,0.15,0.85,0.85)
            self._add_spots(self._rows, self._columns)
            self._population_phase = True
            self._populate_board()
        else:
            quit()
            
    def run(self)-> None:
        '''This function runs the window for the gameplay.'''
        self._window.mainloop()

    def _add_spots(self, rows, columns)-> None:
        '''This function creates the green empty spaces for the board
        which are all canvases and they are saved in a dictionary
        for future manipulations.'''
        for x in range(columns):
            for y in range(rows):
                canvas = tkinter.Canvas(master = self._window,
                                        height = 50, width = 50,
                                        background = 'darkgreen')
                coordinate = str(y) + ' ' + str(x)
                self._canvases[coordinate] = canvas
        self._create_board(self._canvases)

    def _create_board(self, canvases)-> None:
        '''This function adds the green canvases to the board. Each canvas
        is given 3 bind() functions for manipulation.'''
        counter = 0
        for x in range(self._columns):
            for y in range(self._rows):
                coordinate = str(y) + ' ' + str(x)
                self._canvases[coordinate].grid(row = y+1, column = x,
                                             padx = 0, pady = 0,
                                             sticky = tkinter.N + tkinter.S +
                                             tkinter.E + tkinter.W)
                self._canvases[coordinate].bind('<Configure>', self._adjust_size)
                self._canvases[coordinate].bind('<Button-1>', self._change_color)
                self._canvases[coordinate].bind('<ButtonRelease-1>' ,self._adjust_display)
                self._window.rowconfigure(y+1, weight = 1)
                self._window.columnconfigure(x, weight = 1)
                counter += 1

    def _adjust_size(self, event: tkinter.Event)-> None:
        '''This function adjusts the size of all the pieces on the board
        if the window is configured.'''
        canvas = event.widget
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        for x in self._canvases:
            if self._canvases[x] == canvas:
                row = x[0:2]
                column = x[2:5]
                break
        row, column = int(row), int(column)
        if len(self._game.grid()) != 0:
            if self._game.grid()[column][row] == 1:
                canvas.delete(tkinter.ALL)
                canvas.create_oval(
                canvas_width * self._circle[0], canvas_height * self._circle[1],
                canvas_width * self._circle[2], canvas_height * self._circle[3],
                fill = 'black')
            elif self._game.grid()[column][row] == 2:
                canvas.delete(tkinter.ALL)
                canvas.create_oval(
                canvas_width * self._circle[0], canvas_height * self._circle[1],
                canvas_width * self._circle[2], canvas_height * self._circle[3],
                fill = 'white')
            else:
                pass


    def _change_color(self, event: tkinter.Event)-> None:
        '''This function adds the players color to an empty spot on the board depending
        what stage the game is in the population phase or if it is a valid move during
        gameplay. The function also checks if there are any available moves as a pre and post
        condition.'''
        if self._population_phase == True:
            for x in self._canvases:
                if self._canvases[x] == event.widget:
                    row = x[0:2]
                    row = int(row)
                    column = x[2:5]
                    column = int(column)
                    break
            if self._player == 'black' or self._player == 'Black':
                self._grid[column][row] = 1
            else:
                self._grid[column][row] = 2
            
            canvas = event.widget
            canvas.delete(tkinter.ALL)
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            canvas.create_oval(
                canvas_width * self._circle[0], canvas_height * self._circle[1],
                canvas_width * self._circle[2], canvas_height * self._circle[3],
                fill = self._player)
        else:
            if self._game.available_moves() == False:
                    self._winner()
            for x in self._canvases:
                if self._canvases[x] == event.widget:
                    row = x[0:2]
                    row = int(row)
                    column = x[2:5]
                    column = int(column)
                    break
            try:
                self._game.move(column, row)
                self._total_colors_label()
                canvas = event.widget
                canvas.delete(tkinter.ALL)
                canvas_width = canvas.winfo_width()
                canvas_height = canvas.winfo_height()
                canvas.create_oval(
                canvas_width * self._circle[0], canvas_height * self._circle[1],
                canvas_width * self._circle[2], canvas_height * self._circle[3],
                fill = self._player)
                if self._game.available_moves() == False:
                    self._winner()
                if self._game.turn() == 1:
                    self._player = 'Black'
                else:
                    self._player = 'White'
                self._text.set(str(self._player) + "'s Turn")
                
            except:
                self._text.set('INVALID MOVE')
                
    def _adjust_display(self, event: tkinter.Event)-> None:
        '''This function flips any pieces that were caught in between
        the sequence of a valid move after button-1 is released. It then
        determines if there are any moves to be made after the pieces are flipped.'''
        if self._population_phase != True:
            for x in self._canvases:
                row = x[0:2]
                row = int(row)
                column = x[2:5]
                column = int(column)
                if self._game.grid()[column][row] != 0:
                    self._canvases[x].delete(tkinter.ALL)
                    canvas_width = self._canvases[x].winfo_width()
                    canvas_height = self._canvases[x].winfo_height()
                    if self._game.grid()[column][row] == 1:
                        self._canvases[x].create_oval(
                        canvas_width * self._circle[0], canvas_height * self._circle[1],
                        canvas_width * self._circle[2], canvas_height * self._circle[3],
                        fill = 'black')
                    else:
                        self._canvases[x].create_oval(
                        canvas_width * self._circle[0], canvas_height * self._circle[1],
                        canvas_width * self._circle[2], canvas_height * self._circle[3],
                        fill = 'white')
            if self._game.available_moves() == False:
                self._winner()
        
                        
    def _populate_board(self)-> None:
        '''This function sets up the necessary display components for the population phase of the board.'''
        self._situational_button_text = tkinter.StringVar()
        self._situational_button_text.set('Done')
        self._situational_button = tkinter.Button(master = self._top_frame, textvariable = self._situational_button_text, font = ('ariel', 14),command = self._situation_button)
        self._situational_button.grid(row = 0, column = 3, sticky = tkinter.E + tkinter.W)
        self._top_frame.columnconfigure(3, weight = 1)

    def _situation_button(self)-> None:
        '''This function determines the current situation of the Population
        phase of the game. After both players finish populating the board, the
        game will begin depending if there are any available moves after the population.'''
        if self._situational_button['text'] == 'Done':
            self._situational_button_text.set('Begin')
            self._player = 'White'
            self._text.set('Populate Board: White')
        else: 
            self._situational_button.destroy()
            self._population_phase = False
            self._game.create_grid(self._grid)
            if self._game.available_moves() == True:
                if self._game.turn() == 1:
                    self._player = 'Black'
                else:
                    self._player = 'White'
                self._text.set(str(self._player) + "'s Turn")
            else:
                self._winner()
            self._total_colors_label()
            
            
    def _total_colors_label(self)-> None:
        '''This function displays the number of black and white pieces on the board in the
        bottom of the display.'''
        whites = self._game.whites()
        blacks = self._game.blacks()
        self._count_text.set('BLACKS: {} WHITES: {}'.format(blacks, whites))

    def _create_grid(self)-> None:
        '''This function creates the list for the class 'othello' after both users
        populate the board.'''
        counter = 0
        for x in range(self._columns):
            temp = []
            for y in range(self._rows):
                temp.append(0)
            self._grid.append(temp)
            
            
    def _winner(self)-> None:
        '''This function displays the winner of the game in the top label of the display.'''
        winner = self._game.winner()
        if winner == 0:
            self._text.set('TIE')
        elif winner == 1:
            self._text.set('WINNER: BLACK')
        else:
            self._text.set('WINNER: WHITE')
        self._label['state'] = 'disabled'
        self._count_label['state'] = 'disabled'
        for x in self._canvases:
            self._canvases[x]['state'] = 'disabled'
        




class GUI_Options:
    '''This class is the option panel for the game Othello. It creates the layout of the grid for tkinter
    and allows the user to submit the data necessary for the gameplay of Othello. The user will type in the
    appropriate data in the displayed text boxes and then click 'Enter' to proceed. 'Cancel' to exit.'''
    def __init__(self)-> None:
        self._done = False
        self._window = tkinter.Tk()
        self._welcome_label = tkinter.Label(master = self._window, text = 'Welcome to Othello!',
                                            font = ('ariel black', 20, 'bold'))
        self._welcome_label.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10,
                                 sticky = tkinter.N + tkinter.S)
        self._rows_label = tkinter.Label(master = self._window,
                                         text = 'Enter Rows (Even integer from 4 to 16):',
                                         font = ('ariel', 14))
        self._rows_label.grid(row = 1, column = 0,  padx = 10, pady = 10,
            sticky = tkinter.N)

        self._columns_label = tkinter.Label(master = self._window,
                                         text = 'Enter Col. (Even integer from 4 to 16):',
                                         font = ('ariel', 14))
        self._columns_label.grid(row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N)

        self._rows_entry = tkinter.Entry(master = self._window, width = 10, font = ('ariel', 14))
        self._rows_entry.grid(row = 1, column = 1, padx = 10, pady = 1, sticky =
                              tkinter.W + tkinter.E)

        self._columns_entry = tkinter.Entry(master = self._window, width = 10, font = ('ariel', 14))
        self._columns_entry.grid(row = 2, column = 1, padx = 10, pady = 1, sticky =
                                 tkinter.W + tkinter.E)


        self._gameplay_label = tkinter.Label(master = self._window,
                                         text = 'Enter Winning Method (< or >):',
                                         font = ('ariel', 14))
        self._gameplay_label.grid(row = 3, column = 0,  padx = 10, pady = 10,
            sticky = tkinter.N)
        
        
        self._gameplay_entry = tkinter.Entry(master = self._window, width = 10, font = ('ariel', 14))
        self._gameplay_entry.grid(row = 3, column = 1, padx = 10, pady = 1, sticky =
                                 tkinter.W + tkinter.E)

        self._first_label = tkinter.Label(master = self._window,
                                         text = 'Enter Who Gets The First Turn (Black or White):',
                                         font = ('ariel', 14))
        self._first_label.grid(row = 4, column = 0,  padx = 10, pady = 10,
            sticky = tkinter.N)
        
        
        self._first_entry = tkinter.Entry(master = self._window, width = 10, font = ('ariel', 14))
        self._first_entry.grid(row = 4, column = 1, padx = 10, pady = 1, sticky =
                                 tkinter.W + tkinter.E)

        enter_button = tkinter.Button(master = self._window, text = 'Enter',
                                      font = ('ariel', 14), command = self._enter_button)
        enter_button.grid(row = 5, column = 0, padx = 10, pady = 10)
        
        cancel_button = tkinter.Button(master = self._window, text = 'Cancel', font = ('ariel', 14), command = self._cancel_button)
        cancel_button.grid(row = 5, column = 1, padx = 10, pady = 10)
        
        self._window.rowconfigure(5, weight = 1)
        self._window.columnconfigure(2, weight = 1)
        
    def run(self)-> None:
        '''This function runs the tkinter display for this class.'''
        self._window.mainloop()

    def _enter_button(self)-> None:
        '''This function sets the values for the given domain onces 'Enter' is pressed.'''
        self._rows = self._rows_entry.get()
        self._columns = self._columns_entry.get()
        self._gameplay = self._gameplay_entry.get()
        self._first_player = self._first_entry.get()
        self._done = True
        self._window.destroy()

    def _cancel_button(self)-> None:
        '''This function destroys the window if 'Cancel' is pressed.'''
        self._window.destroy()
        
    def get_rows(self)-> str:
        '''This function returns the rows inputted by the user.'''
        return self._rows

    def get_columns(self)-> str:
        '''This function returns the columns inputted by the user.'''
        return self._columns

    def get_gameplay(self)-> str:
        '''This function returns the game option for selecting the winner of the game.'''
        return self._gameplay

    def get_first_player(self)-> int:
        '''This function returns which player goes first.'''
        if self._first_player == 'black' or self._first_player == 'Black' or self._first_player == 'BLACK':
            return 1
        else:
            return 2

    def get_signal(self)-> bool:
        '''This function returns a bool based on whether the inputs were correctly submitted or not.'''
        return self._done
    
if __name__ == '__main__':
    app = Othello_GUI()
    app.run()
        
