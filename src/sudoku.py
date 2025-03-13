import numpy as np

class Sudoku:
    def __init__(self, board=None):
        if board is None:
            self.board = np.zeros((9, 9), dtype=int)
            self.fixed_cells = set()
        else:
            self.board = np.array(board, dtype=int)
            # Đánh dấu các ô có giá trị ban đầu là cố định
            self.fixed_cells = {(i, j) for i in range(9) for j in range(9) if board[i][j] != 0}
    
    def generate_puzzle(self, difficulty=0.5):
        # Chỉ chạy nếu bảng ban đầu là rỗng
        if np.all(self.board == 0):
            for i in range(0, 9, 3):
                nums = np.random.permutation(range(1, 10))
                self.board[i:i+3, i:i+3] = nums.reshape(3, 3)
            # Cập nhật fixed_cells sau khi tạo puzzle
            self.fixed_cells = {(i, j) for i in range(9) for j in range(9) if self.board[i][j] != 0}
    
    def get_board(self):
        return self.board
    
    def is_editable(self, row, col):
        return (row, col) not in self.fixed_cells
    
    def is_valid(self):
        # Kiểm tra hàng và cột, bỏ qua số 0
        for i in range(9):
            row_values = [x for x in self.board[i] if x != 0]
            col_values = [self.board[j][i] for j in range(9) if self.board[j][i] != 0]
            if len(set(row_values)) != len(row_values) or len(set(col_values)) != len(col_values):
                return False
        return True