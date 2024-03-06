# Author: 4sushi

from typing import List, Tuple
import random
import copy


class GameSudoku:

    SIZE = 3
    VALUE_MAX = SIZE * SIZE

    DIFFICULTIES = {
        1: "Easy",
        2: "Medium",
        3: "Hard",
        4: "Expert"
    }

    def __init__(self, difficulty: int):
        if difficulty not in self.DIFFICULTIES.keys():
            raise ValueError("Invalid difficulty")
        self.difficulty: int = difficulty
        self.grid: None | List[List[int]] = None
        self.generate_partial_grid(difficulty)
        self.base_grid = copy.deepcopy(self.grid)

    def generate_empty_grid(self):
        self.grid = [[0 for _ in range(0, self.VALUE_MAX)] for _ in range(0, self.VALUE_MAX)] 

    def generate_full_grid(self):
        self.generate_empty_grid()
        self.fill_diagonals()
        self.solve_sudoku()
        
    def generate_partial_grid(self, difficulty: int = 2):
        self.generate_full_grid()
        cells_to_remove = 30 + (difficulty*10)
        for _ in range(cells_to_remove):
            row, col = random.randint(0, self.VALUE_MAX-1), random.randint(0, self.VALUE_MAX-1)
            self.grid[row][col] = 0

    def fill_diagonals(self):
        for i in range(0, self.VALUE_MAX, self.SIZE):
            possible_values = list(range(1, self.VALUE_MAX+1))
            random.shuffle(possible_values)
            for j in range(self.SIZE):
                for k in range(self.SIZE):
                    self.grid[i+j][i+k] = possible_values.pop()

    def is_valid(self, i_row, i_col, value) -> bool:
        return value not in (self.get_row_values(i_row) + self.get_col_values(i_col) +
                             self.get_square_values(i_row, i_col))

    def get_row_values(self, i_row) -> List[int]:
        row: List[int] = self.grid[i_row]
        return row

    def get_col_values(self, i_col) -> List[int]:
        col: List[int] = [row[i_col] for row in self.grid]
        return col

    def get_square_values(self, i_row, i_col) -> List[int]:
        square: List[int] = []
        for i in range((i_row // self.SIZE) * self.SIZE, (i_row // self.SIZE) * self.SIZE + self.SIZE):
            for j in range((i_col // self.SIZE) * self.SIZE, (i_col // self.SIZE) * self.SIZE + self.SIZE):
                square.append(self.grid[i][j])
        return square

    def solve_sudoku(self):
        pos_empty_cell = self.get_empty_cell_pos()
        if not pos_empty_cell:
            return True
        i_row, i_col = pos_empty_cell

        for value in range(1, self.VALUE_MAX+1):
            if self.is_valid(i_row, i_col, value):
                # Assign value
                self.grid[i_row][i_col] = value
                if self.solve_sudoku():
                    return True
                # Rollback value if we can't solve the sudoku
                self.grid[i_row][i_col] = 0
        return False 

    def get_empty_cell_pos(self) -> None | Tuple[int, int]:
        for i_row in range(self.VALUE_MAX):
            for i_col in range(self.VALUE_MAX):
                if self.grid[i_row][i_col] == 0:
                    return (i_row, i_col)
        return None

    def get_sudoku_str(self) -> str:
        s: str = ('┏' + ('━━━┯'*(self.SIZE-1) + '━━━┳')*self.SIZE)[:-1] + '┓\n'
        for i_row, row in enumerate(self.grid):
            row_str = [str(cell).replace('0', ' ').center(3) for cell in row]
            s += (('┃' + ('{}│'*(self.SIZE-1) + '{}┃')*self.SIZE) + '\n').format(*row_str)
            if i_row == len(row) - 1:
                s += ''
            elif i_row % self.SIZE == self.SIZE - 1:
                s += ('┣' + ('━━━┿'*(self.SIZE-1) + '━━━╋')*self.SIZE)[:-1] + '┫\n'
            else:
                s += ('┠' + ('───┼'*(self.SIZE-1) + '───╂')*self.SIZE)[:-1] + '┨\n'
        s += ('┗' + ('━━━┷'*(self.SIZE-1) + '━━━┻')*self.SIZE)[:-1] + '┛\n'
        return s

    def is_game_won(self) -> bool:
        if self.get_empty_cell_pos():
            return False
        for i_row in range(0, self.VALUE_MAX):
            for i_col in range(0, self.VALUE_MAX):
                val: int = self.grid[i_row][i_col]
                self.grid[i_row][i_col] = 0
                if not self.is_valid(i_row, i_col, val):
                    return False
                self.grid[i_row][i_col] = val
        
        return True
    
    def get_difficulty(self) -> str:
        return self.DIFFICULTIES[self.difficulty]

