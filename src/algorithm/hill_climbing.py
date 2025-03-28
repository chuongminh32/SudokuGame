# from src.sudoku import Sudoku
# import numpy as np
# class HillClimbing:
#     def __init__(self, sudoku, max_iterations=1000):
#         self.sudoku = sudoku
#         self.max_iterations = max_iterations
    
#     def evaluate(self, board):
#         conflicts = 0
#         for i in range(9):
#             # Kiểm tra hàng
#             row_values = board[i][board[i] != 0]
#             conflicts += len(row_values) - len(set(row_values))
#             # Kiểm tra cột
#             col_values = board[:, i][board[:, i] != 0]
#             conflicts += len(col_values) - len(set(col_values))
#         return conflicts
    
#     def solve(self):
#         current_board = self.sudoku.get_board().copy()
#         current_score = self.evaluate(current_board)
        
#         for _ in range(self.max_iterations):
#             if current_score == 0:
#                 return current_board
            
#             neighbor = current_board.copy()
#             i, j = np.random.randint(0, 9, 2)
#             if self.sudoku.is_editable(i, j):
#                 neighbor[i][j] = np.random.randint(1, 10)
            
#             neighbor_score = self.evaluate(neighbor)
#             if neighbor_score < current_score:
#                 current_board = neighbor
#                 current_score = neighbor_score
        
#         return current_board


# Bước 1: Nhận bảng Sudoku đầu vào (9x9) với một số ô trống
# Bước 2: Khởi tạo giá trị ngẫu nhiên cho các ô trống
# Bước 3: Lặp lại quá trình tối ưu, cải thiện lời giải
# Bước 4: Trả về bảng Sudoku đã giải
