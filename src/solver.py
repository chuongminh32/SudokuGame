from src.hill_climbing import HillClimbing
from src.utils.logger import logger
from src.sudoku import Sudoku

class Solver:
    def __init__(self, board):
        self.sudoku = Sudoku(board)  # Tạo đối tượng Sudoku từ bảng đầu vào
    
    def solve(self):
        logger.info("Starting to solve Sudoku puzzle")
        solver = HillClimbing(self.sudoku)
        solution = solver.solve()
        logger.info("Sudoku solving completed")
        return solution