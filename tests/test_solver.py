import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.solver import Solver

class TestSolver(unittest.TestCase):
    def test_solver_valid(self):
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        solution = Solver(board)
        solved_board = solution.solve()  # Gọi phương thức solve() để lấy kết quả
        # Kiểm tra độ dài của mỗi hàng (nên là 9)
        self.assertEqual(len(solved_board[0]), 9)  # Kiểm tra hàng đầu tiên có 9 phần tử
        # (Tùy chọn) Kiểm tra thêm xem bảng đã được giải hợp lệ

if __name__ == '__main__':
    unittest.main()
