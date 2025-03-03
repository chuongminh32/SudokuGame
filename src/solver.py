
from hill_climbing import HillClimbingSolver
from sudoku import Sudoku

def solve_sudoku(grid):
    sudoku = Sudoku(grid)  # Tạo đối tượng Sudoku
    solver = HillClimbingSolver(sudoku)
    return solver.solve()  # Trả về lời giải Sudoku
