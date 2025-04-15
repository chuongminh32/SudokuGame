
import sys, os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *

# trả về bảng giải 
def giai_sudoku_backtracking(bang):
    def hop_le(bang, row, col, num):
        for i in range(9):
            if bang[row][i] == num or bang[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if bang[i][j] == num:
                    return False

        return True

    def solve(bang):
        for row in range(9):
            for col in range(9):
                if bang[row][col] == 0:
                    for num in range(1, 10):
                        if hop_le(bang, row, col, num):
                            bang[row][col] = num
                            if solve(bang):
                                return True
                            bang[row][col] = 0 # quay lui nếu k tìm được lời giải hợp lệ 
                    return False
        return True

    bang_copy = [row[:] for row in bang]  # Sao chép để không sửa bảng gốc
    solve(bang_copy)
    return bang_copy


def giai_sudoku_backtracking_visual(bang, cap_nhat_gui=None, delay=0.05):
    import time

    def hop_le(bang, row, col, num):
        for i in range(9):
            if bang[row][i] == num or bang[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if bang[i][j] == num:
                    return False
        return True
    
    def solve(bang):
        cnt = 0 
        for row in range(9):
            for col in range(9):
                if bang[row][col] == 0:
                    for num in range(1, 10):
                        if hop_le(bang, row, col, num):
                            bang[row][col] = num
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, num, "thu")
                                time.sleep(delay)
                               

                            if solve(bang):
                                if cap_nhat_gui:
                                    cap_nhat_gui(row, col, num, "dung")
                                return True

                            bang[row][col] = 0
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, 0, "sai")
                                time.sleep(delay)
                    return False
        return True

    bang_copy = [row[:] for row in bang]
    solve(bang_copy)
    return bang_copy
