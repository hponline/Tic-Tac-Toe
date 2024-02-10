import tkinter as tk
from tkinter import messagebox
import sys

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.geometry("600x500")
        
        self.game = [['' for _ in range(3)] for _ in range(3)]
        self.players = ['X', 'O']
        self.current_player = self.players[0]
        self.score_x = 0
        self.score_o = 0
        self.ai_mode = False
        
        main_frame = tk.Frame(self.window, width=600, height=400)
        main_frame.pack(pady=50)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(main_frame, text='', command=lambda i=i, j=j: self.click(i, j), height=3, width=6)
                self.buttons[i][j].grid(row=i, column=j, padx=10, pady=10)
        
        restart_button = tk.Button(self.window, text='Restart', command=self.restart)
        restart_button.pack(pady=10)
        
        ai_button = tk.Button(self.window, text='Play with AI', command=self.toggle_ai_mode)
        ai_button.pack(pady=10)
        
        exit_button = tk.Button(self.window, text='Exit', command=self.window.quit)
        exit_button.pack(pady=10)
        
        self.score_label = tk.Label(self.window, text='Score: X - {} O - {}'.format(self.score_x, self.score_o))
        self.score_label.pack(pady=10)
        self.click_count = 0

    def click(self, i, j):
        if self.game[i][j] == '' and not self.check_winner():
            self.buttons[i][j]['text'] = self.current_player
            self.game[i][j] = self.current_player
            
            if self.check_winner():
                messagebox.showinfo("Game Over", "{} Oyuncu Kazandı!".format(self.current_player))
                if self.current_player == 'X':
                    self.score_x += 1
                else:
                    self.score_o += 1
                self.update_score()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "Berabere!")
            else:
                self.current_player = self.players[(self.players.index(self.current_player) + 1) % 2]
                self.click_count += 1
                if self.click_count % 2 == 1:
                    self.buttons[i][j]['bg'] = '#A0C49D'
                else:
                    self.buttons[i][j]['bg'] = '#E1ECC8'
                
                if self.ai_mode and self.current_player == 'O' and not self.check_winner() and not self.check_draw():
                    self.ai_move()

    def check_winner(self):
        for i in range(3):
            if self.game[i][0] == self.game[i][1] == self.game[i][2] != '':
                return True
            if self.game[0][i] == self.game[1][i] == self.game[2][i] != '':
                return True
        if self.game[0][0] == self.game[1][1] == self.game[2][2] != '':
            return True
        if self.game[0][2] == self.game[1][1] == self.game[2][0] != '':
            return True
        return False

    def check_draw(self):
        for row in self.game:
            if '' in row:
                return False
        return True

    def restart(self):
        self.game = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ''
                self.buttons[i][j]['bg'] = 'SystemButtonFace'
        self.current_player = self.players[0]
        self.click_count = 0
        self.update_score()

    def update_score(self):
        self.score_label['text'] = 'Score: X - {} O - {}'.format(self.score_x, self.score_o)

    def toggle_ai_mode(self):
        self.ai_mode = not self.ai_mode
        self.restart()

    def ai_move(self):
        best_score = -sys.maxsize
        move = None
        for i in range(3):
            for j in range(3):
                if self.game[i][j] == '':
                    self.game[i][j] = 'O'
                    score = self.minimax(self.game, 0, False)
                    self.game[i][j] = ''
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        self.click(*move)

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner():
            if is_maximizing:
                return -1
            else:
                return 1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best_score = -sys.maxsize
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = sys.maxsize
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
