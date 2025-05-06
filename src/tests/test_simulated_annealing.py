import unittest, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.simulate_anealing import (
    simulated_annealing_core,
    giai_sudoku_simulated_annealing,
    ghi_log_simulated_annealing
)

class TestSimulatedAnnealingSudoku(unittest.TestCase):
    def setUp(self):
        # Bảng Sudoku hợp lệ (từ Leetcode)
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

        # Bảng Sudoku không hợp lệ (trùng số 5)
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

    def test_simulated_annealing_core_valid(self):
        """
        Test simulated_annealing_core với bảng hợp lệ.
        Kỳ vọng: giải được, số bước > 0, thời gian hợp lý.
        """
        solved, steps, is_solved, duration = simulated_annealing_core(self.valid_board, 9)
        self.assertTrue(is_solved)
        self.assertGreater(steps, 0)
        self.assertLess(duration, 5.0)

    def test_simulated_annealing_core_invalid(self):
        """
        Với bảng không hợp lệ, kỳ vọng giải vẫn kết thúc nhưng không đảm bảo chính xác.
        """
        with self.assertRaises(ValueError):
            simulated_annealing_core(self.invalid_board, 9)
        # solved, steps, is_solved, duration = simulated_annealing_core(self.invalid_board, 9)
        #SA có thể cố gắng giải nhưng không đảm bảo chính xác
        # self.assertIsInstance(solved, list)
        # self.assertGreaterEqual(duration, 0)
        # self.assertGreater(steps, 0)

    def test_giai_sudoku_simulated_annealing(self):
        """
        Test hàm giai_sudoku_simulated_annealing với bảng hợp lệ.
        Kỳ vọng: không còn ô trống, isSolve = True.
        """
        result, steps, is_solved = giai_sudoku_simulated_annealing(self.valid_board)
        self.assertTrue(is_solved)
        for row in result:
            self.assertNotIn(0, row)

    def test_ghi_log_simulated_annealing(self):
        """
        Test ghi_log_simulated_annealing: kiểm tra thời gian trả về > 0.
        """
        duration = ghi_log_simulated_annealing(self.valid_board, 9)
        self.assertGreater(duration, 0)
        log_file = os.path.join("SudokuGame", "data", "log_SA.txt")
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Log giải Sudoku bằng Simulated Annealing", content)

if __name__ == '__main__':
    unittest.main()
