# import random
# import numpy as np

# class HillClimbingSolver:
#     def __init__(self, sudoku):
#         self.sudoku = sudoku
#         self.current_state = self.initialize_state()

#     def initialize_state(self):
#         """Khởi tạo trạng thái ban đầu bằng cách điền ngẫu nhiên các số hợp lệ vào ô trống."""
#         state = self.sudoku.grid.copy()
#         for row, col in self.sudoku.get_empty_cells():
#             state[row, col] = random.randint(1, 9)  # Gán số ngẫu nhiên từ 1-9
#         return state

#     def heuristic(self, state):
#         """Hàm đánh giá: Đếm số lần vi phạm quy tắc Sudoku."""
#         errors = 0
#         for i in range(9):
#             errors += (9 - len(set(state[i, :])))  # Đếm số trùng trong hàng
#             errors += (9 - len(set(state[:, i])))  # Đếm số trùng trong cột
#         return errors

#     def generate_neighbor(self):
#         """Tạo trạng thái lân cận bằng cách hoán đổi hai ô trống bất kỳ."""
#         neighbor = self.current_state.copy()
#         empty_cells = self.sudoku.get_empty_cells()
#         if len(empty_cells) < 2:
#             return neighbor

#         (r1, c1), (r2, c2) = random.sample(empty_cells, 2)
#         neighbor[r1, c1], neighbor[r2, c2] = neighbor[r2, c2], neighbor[r1, c1]
#         return neighbor

#     def solve(self, max_iterations=1000):
#         """Giải Sudoku bằng thuật toán Hill-Climbing."""
#         for _ in range(max_iterations):
#             new_state = self.generate_neighbor()
#             if self.heuristic(new_state) < self.heuristic(self.current_state):
#                 self.current_state = new_state  # Chấp nhận trạng thái tốt hơn
#         return self.current_state


import random
import numpy as np

class HillClimbingSolver:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.current_state = self.initialize_state()

    def get_empty_cells(self):
        """Trả về danh sách các ô trống trong Sudoku."""
        empty_cells = []
        for r in range(9):
            for c in range(9):
                if self.sudoku.grid[r][c] == 0:  # Nếu ô này trống
                    empty_cells.append((r, c))
        return empty_cells

    def initialize_state(self):
        """Khởi tạo trạng thái ban đầu bằng cách điền ngẫu nhiên các số hợp lệ vào ô trống."""
        state = np.array(self.sudoku.grid)  # Chuyển thành mảng NumPy để dễ xử lý
        for row, col in self.get_empty_cells():
            state[row, col] = random.randint(1, 9)  # Gán số ngẫu nhiên từ 1-9
        return state

    def heuristic(self, state):
        """Hàm đánh giá: Đếm số lần vi phạm quy tắc Sudoku."""
        errors = 0
        for i in range(9):
            errors += (9 - len(set(state[i, :])))  # Đếm số trùng trong hàng
            errors += (9 - len(set(state[:, i])))  # Đếm số trùng trong cột
        return errors

    def generate_neighbor(self):
        """Tạo trạng thái lân cận bằng cách hoán đổi hai ô trống bất kỳ."""
        neighbor = self.current_state.copy()
        empty_cells = self.get_empty_cells()
        if len(empty_cells) < 2:
            return neighbor
    
        (r1, c1), (r2, c2) = random.sample(empty_cells, 2)
        neighbor[r1, c1], neighbor[r2, c2] = neighbor[r2, c2], neighbor[r1, c1]
        return neighbor

    def solve(self, max_iterations=1000):
        """Giải Sudoku bằng thuật toán Hill-Climbing."""
        for _ in range(max_iterations):
            new_state = self.generate_neighbor()
            if self.heuristic(new_state) < self.heuristic(self.current_state):
                self.current_state = new_state  # Chấp nhận trạng thái tốt hơn
        return self.current_state.tolist()  # Chuyển về danh sách trước khi trả về
