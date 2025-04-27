import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *
from src.utils.utils_ai_screen import *

import time

# Trả về bảng giải, số bước và log (nếu có)
def giai_sudoku_backtracking(bang, cap_nhat_gui=None, delay=0.0, isSolve = False):
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

    so_buoc = 0
    ds_log = []
    start_time = time.perf_counter()

    def solve(bang):
        nonlocal so_buoc
        for row in range(9):
            for col in range(9):
                if bang[row][col] == 0:
                    for num in range(1, 10):
                        if hop_le(bang, row, col, num):
                            bang[row][col] = num
                            so_buoc += 1

                            # Nếu có GUI -> cập nhật hiệu ứng
                            if cap_nhat_gui:
                                current_time = time.perf_counter()
                                ds_log.append((so_buoc, current_time - start_time))
                                cap_nhat_gui(row, col, num, "thu", so_buoc)
                                time.sleep(delay)

                            if solve(bang):
                                if cap_nhat_gui:
                                    cap_nhat_gui(row, col, num, "dung", so_buoc)
                                return True

                            bang[row][col] = 0
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, 0, "sai", so_buoc)
                                time.sleep(delay)
                    return False
        return True

    bang_copy = [row[:] for row in bang]  # Copy bảng ban đầu để giữ nguyên
    if solve(bang_copy):
        isSolve = True

    if cap_nhat_gui:
        return bang_copy, so_buoc, ds_log, isSolve
    else:
        return bang_copy, so_buoc, None, isSolve
