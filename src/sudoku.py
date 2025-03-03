import numpy as np
import random

class Sudoku:
    def __init__(self, size=9):
        self.size = size
        self.grid = np.zeros((9, 9), dtype=int)

    def generate_full_grid(self):
        """Sinh bảng Sudoku hoàn chỉnh (đang dùng số ngẫu nhiên, cần cải thiện)."""
        for i in range(9):
            for j in range(9):
                self.grid[i][j] = random.randint(1, 9)

    def difficulty(self, level):
        """Tạo đề bài theo cấp độ khó"""
        self.generate_full_grid()

        difficulties = {"easy": 30, "medium": 40, "hard": 50}
        empty_cells = difficulties.get(level, 30)  # Nếu không tìm thấy level, mặc định là 30 ô trống

        while empty_cells > 0:
            i, j = random.randint(0, 8), random.randint(0, 8)
            if self.grid[i][j] != 0:
                self.grid[i][j] = 0
                empty_cells -= 1

        return self  # Trả về chính đối tượng Sudoku để có thể gọi .board

    @property
    def board(self):
        return self.grid
