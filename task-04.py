import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.grid_locked = False
        self.create_grid()

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                # Configure the entry widget for each cell
                entry = tk.Entry(self.root, width=3, font=("Arial", 18), justify="center", bd=1)
                entry.grid(row=row, column=col, padx=(3, 3 if (col + 1) % 3 else 8), 
                           pady=(3, 3 if (row + 1) % 3 else 8))
                entry.bind("<KeyRelease>", self.validate_entry)
                self.entries[row][col] = entry

        # Button to lock the grid
        lock_button = tk.Button(self.root, text="Lock Grid", command=self.lock_grid)
        lock_button.grid(row=10, column=0, columnspan=4, pady=10)

        # Button to validate user inputs after the grid is locked
        validate_button = tk.Button(self.root, text="Check Solution", command=self.check_solution)
        validate_button.grid(row=10, column=5, columnspan=4, pady=10)

    def validate_entry(self, event):
        entry = event.widget
        value = entry.get()

        # Ensure the input is a digit between 1 and 9, or empty
        if value.isdigit() and 1 <= int(value) <= 9:
            row, col = self.get_entry_location(entry)
            if self.is_valid_move(self.get_board(), row, col, int(value)):
                entry.config(bg="white")
            else:
                entry.config(bg="red")
        elif value == "":
            entry.config(bg="white")
        else:
            entry.delete(0, tk.END)
            entry.config(bg="white")

    def lock_grid(self):
        self.grid_locked = True
        messagebox.showinfo("Grid Locked", "The grid is locked. You can now solve the Sudoku puzzle manually.")

    def is_valid_move(self, board, row, col, num):
        for i in range(9):
            if i != col and board[row][i] == num:
                return False
            if i != row and board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                r, c = start_row + i, start_col + j
                if (r != row or c != col) and board[r][c] == num:
                    return False

        return True

    def check_solution(self):
        board = self.get_board()
        is_valid = True
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num != 0 and not self.is_valid_move(board, row, col, num):
                    self.entries[row][col].config(bg="red")
                    is_valid = False
                else:
                    self.entries[row][col].config(bg="white")

        if is_valid:
            messagebox.showinfo("Success", "All entries are valid!")
        else:
            messagebox.showerror("Invalid", "Some entries violate Sudoku rules.")

    def get_entry_location(self, entry):
        for row in range(9):
            for col in range(9):
                if self.entries[row][col] == entry:
                    return row, col
        return -1, -1

    def get_board(self):
        board = []
        for row in range(9):
            row_vals = []
            for col in range(9):
                val = self.entries[row][col].get()
                if val.isdigit():
                    row_vals.append(int(val))
                else:
                    row_vals.append(0)
            board.append(row_vals)
        return board

def main():
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()

if __name__ == "__main__":
    main()
