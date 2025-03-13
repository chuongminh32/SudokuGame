import unittest
import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.sudoku import Sudoku

class TestSudoku(unittest.TestCase):
    def setUp(self):
        self.sudoku = Sudoku()
    
    def test_generate_puzzle(self):
        self.sudoku.generate_puzzle()
        self.assertTrue(np.any(self.sudoku.get_board() != 0))
    
    def test_is_editable(self):
        self.sudoku.generate_puzzle()
        board = self.sudoku.get_board()
        non_zero = np.where(board != 0)
        self.assertFalse(self.sudoku.is_editable(non_zero[0][0], non_zero[1][0]))

if __name__ == '__main__':
    unittest.main()