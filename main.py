# Ori kenigsbuch 206594590
import random
import tkinter as tk
from tkinter import messagebox

class cell:
    def __init__(self, is_bomb=False):
        self.is_bomb = is_bomb
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_bombs = 0

class Minesweeper:
    def __init__(self, root, size, bomb_count):
        self.root = root
        self.size = size
        self.bomb_count = bomb_count
        self.board = [[cell() for _ in range(size)] for _ in range(size)]
        self.buttons = []
        self._place_bombs()
        self._calculate_neighbors()
        self._create_buttons()

    def _place_bombs(self):
        positions = random.sample(range(self.size * self.size), self.bomb_count)
        for pos in positions:
            x, y = divmod(pos, self.size)
            self.board[x][y].is_bomb = True

    def _calculate_neighbors(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y].is_bomb:
                    continue
                count = 0
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny].is_bomb:
                        count += 1
                self.board[x][y].neighbor_bombs = count


    def _create_buttons(self):
        for x in range(self.size):
            row = []
            for y in range(self.size):
                btn = tk.Button(self.root, width=2, height=1, bg="light gray", command=lambda x=x, y=y: self._reveal_cell(x, y))
                btn.bind("<Button-3>", lambda e, x=x, y=y: self._toggle_flag(x, y))
                btn.grid(row=x, column=y)
                row.append(btn)
            self.buttons.append(row)



    def _reveal_cell(self, x, y):
        cell = self.board[x][y]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True
        if cell.is_bomb:
            self.buttons[x][y].config(bg="red", text="B")
            messagebox.showinfo("Game Over", "You hit a bomb!")
            self.root.quit()
        else:
            self.buttons[x][y].config(bg="white", state=tk.DISABLED, text=str(cell.neighbor_bombs) if cell.neighbor_bombs > 0 else "")
            if cell.neighbor_bombs == 0:
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        self._reveal_cell(nx, ny)
        self._check_win()

    def _toggle_flag(self, x, y):
        cell = self.board[x][y]
        if cell.is_revealed:
            return

        cell.is_flagged = not cell.is_flagged
        self.buttons[x][y].config(text="F" if cell.is_flagged else "", bg="yellow" if cell.is_flagged else "light gray")
        self._check_win()

    def _check_win(self):
        flagged_bombs = sum(1 for x in range(self.size) for y in range(self.size) if self.board[x][y].is_bomb and self.board[x][y].is_flagged)
        if flagged_bombs == self.bomb_count:
            messagebox.showinfo("Congratulations", "You won the game!")
            self.root.quit()

if __name__ == "__main__":
    s = int(input("Enter the size of the board: "))
    b = int(input("Enter the number of bombs: "))
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root, size=s, bomb_count=b)
    root.mainloop()
