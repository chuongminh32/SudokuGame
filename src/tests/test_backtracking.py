import unittest, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.backtracking import backtracking_core, giai_sudoku_backtracking, ghi_log_backtracking

class TestBacktrackingSudoku(unittest.TestCase):
    def setUp(self):
        # Bảng Sudoku có thể giải được (bài toán chuẩn từ Leetcode)
        self.valid_board = [
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

        # Bảng Sudoku không thể giải do có 2 số 5 trùng hàng ở dòng đầu
        self.invalid_board = [
            [5, 5, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

    def test_backtracking_core_valid(self):
        """
        Test thuật toán backtracking_core với một bảng hợp lệ.
        Kỳ vọng: giải thành công, có bước thực hiện, thời gian giải nhỏ.
        """
        result, buoc, duration = backtracking_core(self.valid_board, 9)
        self.assertTrue(result)             # Bảng phải được giải thành công
        self.assertGreater(buoc, 0)         # Số bước phải > 0
        self.assertLess(duration, 2)        # Thời gian nhỏ (nếu không bị delay)

    def test_backtracking_core_invalid(self):
        """
        Test với bảng Sudoku không hợp lệ (trùng số).
        Kỳ vọng: thuật toán trả về False.
        """
        result, buoc, duration = backtracking_core(self.invalid_board, 9)
        self.assertFalse(result)            # Không giải được bảng sai

    def test_giai_sudoku_backtracking(self):
        """
        Test hàm giao diện giai_sudoku_backtracking với bảng hợp lệ.
        Kỳ vọng: bảng được giải, không còn ô 0.
        """
        solved_board, steps, is_solved = giai_sudoku_backtracking(self.valid_board)
        self.assertTrue(is_solved)                      # Giải thành công
        for row in solved_board:
            self.assertNotIn(0, row)                    # Không còn ô trống

    def test_ghi_log_backtracking(self):
        """
        Test hàm ghi_log_backtracking có tạo log và đo thời gian.
        Kỳ vọng: thời gian trả về > 0 nghĩa là có thực hiện thuật toán.
        """
        duration = ghi_log_backtracking(self.valid_board, 9)
        self.assertGreater(duration, 0)                 # Có mất thời gian giải nghĩa là đã chạy

if __name__ == '__main__':
    unittest.main()

# Python unittest module documentation: https://docs.python.org/3/library/unittest.html