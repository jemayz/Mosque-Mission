import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk,Image


class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Mosque Mission")
        self.board = [' ']*9
        self.current_player = 'X'
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):        
        # Set background color to black
        self.master.configure(bg="lightblue")
       

        # Get the width and height of the window
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()

        # Calculate the center coordinates for placing the Tic Tac Toe grid
        grid_width = 3 * 100  # Assuming each button has a width of 100 pixels
        grid_height = 3 * 100  # Assuming each button has a height of 100 pixels
        x_center = (window_width - grid_width) / 2 + 200
        y_center = (window_height - grid_height) / 2 + 350

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.master, text='', font=('Arial', 30), width=3, height=1,
                                   bg="black",fg="red",
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                # Place the button at the calculated center coordinates
                button.place(x=x_center + j * 100, y=y_center + i * 100)
                self.buttons.append(button)

    def on_button_click(self, row, col):
        index = row * 3 + col
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Alhamdulillah!",  "I can go to the Mosque now.")
                self.open_new_window()  # Call the method to open a new window                
                self.reset_board()
            elif ' ' not in self.board:
                messagebox.showinfo("Allahuakhbar!", "I am about to win. Never mind lets try again!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.ai_make_move()

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def reset_board(self):
        for i in range(9):
            self.board[i] = ' '
            self.buttons[i].config(text='')
        self.current_player = 'X'

    def ai_make_move(self):
        empty_indices = [i for i, val in enumerate(self.board) if val == ' ']
        if empty_indices:
            best_move = self.heuristic_search(self.board, 'O')
            self.board[best_move] = 'O'
            self.buttons[best_move].config(text='O')
            if self.check_winner('O'):
                messagebox.showinfo("Astagfirullah!", "Please help me Allah to win this.")
                self.reset_board()
                return
            self.current_player = 'X'

    def heuristic_search(self, board, player):
        best_score = float('-inf')
        best_move = None
        for spot in [i for i, val in enumerate(board) if val == ' ']:
            board[spot] = player
            score = self.evaluate(board)
            board[spot] = ' '
            if score > best_score:
                best_score = score
                best_move = spot
        return best_move

    def evaluate(self, board):
        # Simple evaluation function:
        # +1 if 'O' wins, -1 if 'X' wins, 0 for a draw or game still in progress
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        else:
            return 0
    
    def open_new_window(self):
      # Close the current Tic Tac Toe window
       self.master.destroy()
       new_window = tk.Toplevel()              
       new_window.geometry("600x600")
    
       # Read and execute the code from another Python file
       filename = "main.py"
       exec(open(filename).read(), globals(), globals())   
          


def main():
    root = tk.Tk()
    height = 600
    width = 600
    
  # Add a title label
    title_label = tk.Label(root, text="~ Mosque Mission: Defeat TTT to Attend Prayer ~", font=('Comic Sans MS', 18), bg="lightblue")
    title_label.pack(pady=0)  # Add some padding below the title
    canvas = tk.Canvas(root, height=height, width=width)
    img = Image.open("mosque.jpg")
    img_resized = img.resize((width, height), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)
    canvas_width = img_resized.width
    canvas_height = img_resized.height
    x_offset = (width - canvas_width) // 2 +300
    y_offset = (height - canvas_height) // 2 +300
    canvas.create_image(x_offset, y_offset, anchor=tk.CENTER, image=img_tk)
    canvas.pack()
    game = TicTacToe(root)  
    root.geometry(f"{width}x{height}")
    root.mainloop()


if __name__ == "__main__":
    main()
