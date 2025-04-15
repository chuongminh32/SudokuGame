
import sys, os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *

# trả về bảng giải 
def giai_sudoku_backtracking(board):
    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve(board):
                                return True
                            board[row][col] = 0 # quay lui nếu k tìm được lời giải hợp lệ 
                    return False
        return True

    board_copy = [row[:] for row in board]  # Sao chép để không sửa bảng gốc
    solve(board_copy)
    return board_copy
def giai_sudoku_backtracking_visual(board, cap_nhat_gui=None, delay=0.05):
    import time

    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, num, "thu")
                                time.sleep(delay)

                            if solve(board):
                                if cap_nhat_gui:
                                    cap_nhat_gui(row, col, num, "dung")
                                return True

                            board[row][col] = 0
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, 0, "sai")
                                time.sleep(delay)
                    return False
        return True

    board_copy = [row[:] for row in board]
    solve(board_copy)
    return board_copy


