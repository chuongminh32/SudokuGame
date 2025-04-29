import sys, os, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *
from src.utils.utils_ai_screen import *

import time

# Trả về bảng giải, số bước và log (nếu có)
def giai_sudoku_backtracking(bang, size, cap_nhat_gui=None, delay=0.0, isSolve = False):
    KT_box = math.isqrt(size)
    def hop_le(bang, row, col, num):
        for i in range(size):
            if bang[row][i] == num or bang[i][col] == num:
                return False
        start_row, start_col = KT_box * (row // KT_box), KT_box * (col // KT_box)
        for i in range(start_row, start_row + KT_box):
            for j in range(start_col, start_col + KT_box):
                if bang[i][j] == num:
                    return False
        return True

    so_buoc = 0
    ds_log = []
    start_time = time.perf_counter()

    def solve(bang):
        nonlocal so_buoc
        for row in range(size):
            for col in range(size):
                if bang[row][col] == 0:
                    for num in range(1, size + 1):
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

# import sys, os, math
# import time

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# from src.algorithm.generate_sudoku import *
# from src.utils.utils_ai_screen import *

# # Trả về bảng giải, số bước và log (nếu có)
# def giai_sudoku_backtracking(bang, size, cap_nhat_gui=None, delay=0.0, isSolve=False):
#     KT_box = math.isqrt(size)

#     def hop_le(bang, row, col, num):
#         for i in range(size):
#             if bang[row][i] == num or bang[i][col] == num:
#                 return False
#         start_row, start_col = KT_box * (row // KT_box), KT_box * (col // KT_box)
#         for i in range(start_row, start_row + KT_box):
#             for j in range(start_col, start_col + KT_box):
#                 if bang[i][j] == num:
#                     return False
#         return True

#     def tim_o_trong_it_lua_chon_nhat(bang):
#         min_options = size 
#         best_cell = None
#         for row in range(size):
#             for col in range(size):
#                 if bang[row][col] == 0:
#                     count = 0
#                     for num in range(1, size + 1):
#                         if hop_le(bang, row, col, num):
#                             count += 1
#                     if count < min_options:
#                         min_options = count
#                         best_cell = (row, col)
#                         if min_options == 1:
#                             return best_cell
#         return best_cell

#     so_buoc = 0
#     ds_log = []
#     start_time = time.perf_counter()  # Bắt đầu đo thời gian

#     def solve(bang):
#         nonlocal so_buoc
#         empty_cell = tim_o_trong_it_lua_chon_nhat(bang)
#         if not empty_cell:
#             return True  # Đã giải xong

#         row, col = empty_cell

#         for num in range(1, size + 1):
#             if hop_le(bang, row, col, num):
#                 bang[row][col] = num
#                 so_buoc += 1

#                 # Không cập nhật GUI khi đo thời gian
#                 if cap_nhat_gui:
#                     cap_nhat_gui(row, col, num, "thu", so_buoc)

#                 if solve(bang):
#                     if cap_nhat_gui:
#                         cap_nhat_gui(row, col, num, "dung", so_buoc)
#                     return True

#                 bang[row][col] = 0
#                 if cap_nhat_gui:
#                     cap_nhat_gui(row, col, 0, "sai", so_buoc)

#         return False

#     bang_copy = [row[:] for row in bang]  # Copy bảng ban đầu để giữ nguyên
#     solve(bang_copy)

#     end_time = time.perf_counter()  # Kết thúc đo thời gian
#     elapsed_time = end_time - start_time

#     if cap_nhat_gui:
#         return bang_copy, so_buoc, ds_log, isSolve, elapsed_time
#     else:
#         return bang_copy, so_buoc, None, isSolve, elapsed_time


# def test_giai_sudoku(bang, size, repeat_times=10):
#     total_time = 0
#     for _ in range(repeat_times):
#         _, _, _, _, elapsed_time = giai_sudoku_backtracking(bang, size, cap_nhat_gui=None)
#         total_time +=     elapsed_time

#     avg_time = total_time / repeat_times
#     print(f"Thời gian trung bình cho {repeat_times} lần chạy: {avg_time:.6f} giây")

# # Chạy thử
# bang = [[...]]  # Bảng Sudoku cần giải
# size = 9  # Kích thước Sudoku (9x9)

# test_giai_sudoku(bang, size, repeat_times=5)  # Lặp lại 5 lần để tính thời gian trung bình
