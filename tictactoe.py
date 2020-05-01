from tkinter import *
from tkinter import messagebox
from random import choice


def button(frame):
    """
    Instantiates a button
    :param frame: the frame to which the button belongs
    :return: the button instance
    """
    b = Button(frame, padx=1, bg="papaya whip", width=3, text="   ", font=('arial', 60, 'bold'), relief="groove", bd=10)
    return b


class TicTacToe:

    def __init__(self):
        """
        Sets up the GUI windows and the game itself
        """
        self.mark = {1: ' O ', 2: ' X '}
        self.player = 1
        self.ai = None
        self.level = 9
        self.ai_board = [['   ' for _ in range(3)] for _ in range(3)]
        self.depth = 0
        ###############################################
        self.root = Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.geometry('500x500')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ###############################################
        self.menu_frame = Frame(self.root)
        self.menu_frame.grid(row=0, column=0, sticky='news')
        self.button_1_player = Button(self.menu_frame, text='1 Player', command=lambda: self.level_frame.tkraise())
        self.button_2_players = Button(self.menu_frame, text='2 Players', command=lambda: self.game_vs_players())
        self.button_1_player.pack(expand=True, fill='both')
        self.button_2_players.pack(expand=True, fill='both')
        ###############################################
        self.level_frame = Frame(self.root)
        self.level_frame.grid(row=0, column=0, sticky='news')
        self.button_level_easy = Button(self.level_frame, text='Easy', command=lambda: self.game_vs_ai(1))
        self.button_level_medium = Button(self.level_frame, text='Medium', command=lambda: self.game_vs_ai(5))
        self.button_level_hard = Button(self.level_frame, text='Hard', command=lambda: self.game_vs_ai(9))
        self.button_level_easy.pack(expand=True, fill='both')
        self.button_level_medium.pack(expand=True, fill='both')
        self.button_level_hard.pack(expand=True, fill='both')
        ###############################################
        self.board_frame = Frame(self.root)
        self.board_frame.grid(row=0, column=0, sticky='news')
        for i in range(3):
            self.board_frame.grid_columnconfigure(index=i, weight=1)
            self.board_frame.grid_rowconfigure(index=i, weight=1)
        self.board = [[], [], []]
        for i in range(3):
            for j in range(3):
                self.board[i].append(button(self.board_frame))
                self.board[i][j].config(command=lambda row=i, col=j: self.player_click(row, col))
                self.board[i][j].grid(row=i, column=j, sticky=NSEW)
        self.label = Label(self.board_frame, text=f'Player {self.player}: {self.mark[self.player]}',
                           font=('arial', 20, 'bold'))
        self.label.grid(row=3, column=0, columnspan=3)
        ###############################################
        self.menu_frame.tkraise()
        
    def mainloop(self):
        """
        Infinite loop used to run the application
        """
        self.root.mainloop()

    def game_vs_players(self):
        """
        Raises window for two players playing against each other
        """
        self.board_frame.tkraise()

    def player_click(self, row, col):
        """
        Adds the corresponding player mark to the board
        :param row: the desired row
        :param col: the desired col
        """
        self.board[row][col].config(text=self.mark[self.player], state=DISABLED)
        self.ai_board[row][col] = self.mark[self.player]
        self.check_gui_board()
        self.player = 3 - self.player
        self.label.config(text=f'Player {self.player}: {self.mark[self.player]}')
        if self.ai:
            self.ai_click()

    def game_vs_ai(self, level):
        """
        Raises the window for the game against the AI
        :param level: the desired level of difficulty
        """
        self.level = level
        self.ai = choice([1, 2])
        self.board_frame.tkraise()
        if self.player == self.ai:
            self.ai_click()

    def ai_click(self):
        """
        Simulates the AI move
        """
        row, col = self.best_move(self.ai)
        self.board[row][col].config(text=self.mark[self.player], state=DISABLED)
        self.ai_board[row][col] = self.mark[self.player]
        self.check_gui_board()
        self.player = 3 - self.player
        self.label.config(text=f'Player {self.player}: {self.mark[self.player]}')

    def best_move(self, player):
        """
        Calculates the best move for the player passed as parameter
        :param player: the player for whom the move is calculated
        :return: the best move (if the search is at the highest node), otherwise the score
        """
        best_score = -100 if player == self.ai else 100
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.ai_board[i][j] == '   ':
                    self.ai_board[i][j] = self.mark[player]
                    score = self.move_score(player)
                    self.ai_board[i][j] = '   '
                    if player == self.ai and score > best_score:
                        best_score = score
                        best_move = i, j
                    if player != self.ai and score < best_score:
                        best_score = score
                        best_move = i, j
        if self.depth == 0:
            return best_move
        else:
            self.depth -= 1
            return best_score

    def move_score(self, player):
        """
        Calculates the score for the attempted move.
        If the board is still empty it will recursively check for the best move
        :param player: the player for whom the score is calculated
        :return: the score for the attempted move
        """
        score = 10 - self.depth if player == self.ai else -10 + self.depth
        if self.ai_board[0][0] == self.ai_board[1][1] == self.ai_board[2][2] != '   ':
            return score
        if self.ai_board[0][2] == self.ai_board[1][1] == self.ai_board[2][0] != '   ':
            return score
        for i in range(3):
            if self.ai_board[i][0] == self.ai_board[i][1] == self.ai_board[i][2] != '   ':
                return score
            if self.ai_board[0][i] == self.ai_board[1][i] == self.ai_board[2][i] != '   ':
                return score
        if all([True if self.ai_board[i][j] != '   ' else False for i in range(3) for j in range(3)]):
            return - self.depth if player == self.ai else self.depth
        if self.depth < self.level:
            player = 1 if player == 2 else 2
            self.depth += 1
            return self.best_move(player)
        else:
            return - self.depth if player == self.ai else self.depth

    def check_gui_board(self):
        """
        Checks if there is a winner or a draw in the GUI board
        """
        if self.board[0][0]['text'] == self.board[1][1]['text'] == self.board[2][2]['text'] == self.mark[self.player]:
            self.display_winner_message()
        if self.board[0][2]['text'] == self.board[1][1]['text'] == self.board[2][0]['text'] == self.mark[self.player]:
            self.display_winner_message()
        for i in range(3):
            if self.board[i][0]['text'] == self.board[i][1]['text'] == self.board[i][2]['text'] == self.mark[self.player]:
                self.display_winner_message()
            if self.board[0][i]['text'] == self.board[1][i]['text'] == self.board[2][i]['text'] == self.mark[self.player]:
                self.display_winner_message()
        if all([True if self.board[i][j]['state'] == DISABLED else False for i in range(3) for j in range(3)]):
            self.display_draw_message()

    def reset(self):
        """
        Resets the game
        """
        for i in range(3):
            for j in range(3):
                self.board[i][j]["text"] = "   "
                self.board[i][j]["state"] = NORMAL
        self.ai_board = [['   ' for _ in range(3)] for _ in range(3)]
        self.player = 2
        self.ai = None
        self.menu_frame.tkraise()

    def display_winner_message(self):
        """
        Display a message box for a win
        """
        if not self.ai:
            messagebox.showinfo(message=f"Congrats!! Player {self.player} has won")
        elif self.player == self.ai:
            messagebox.showinfo(message=f"Sorry!! You lost")
        else:
            messagebox.showinfo(message=f"Congrats!! You won")
        self.reset()

    def display_draw_message(self):
        """
        Display a message box for a draw
        """
        messagebox.showinfo(message="No winners! The game ended with a draw")
        self.reset()


if __name__ == "__main__":
    TicTacToe().mainloop()
