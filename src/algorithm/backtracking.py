# import sys, os, math
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# from src.algorithm.generate_sudoku import *
# from src.utils.utils_ai_screen import *
# import time

# def backtracking_core(board, size, callback=None, delay=0):

#     SIZE_BOX = math.isqrt(size)
#     VALID_NUMS = list(range(1, size + 1))

#     rows = [set() for _ in range(size)]
#     cols = [set() for _ in range(size)]
#     boxes = [[set() for _ in range(SIZE_BOX)] for _ in range(SIZE_BOX)]

#     # tạo tập giá trị có sẵn của đề 
#     for r in range(size):
#         for c in range(size):
#             val = board[r][c]
#             if val:
#                 rows[r].add(val)
#                 cols[c].add(val)
#                 boxes[r // SIZE_BOX][c // SIZE_BOX].add(val)

#     start = time.perf_counter() # bắt đầu đếm tg 
#     buoc = 0

#     def solve():
#         nonlocal buoc
#         for r in range(size):
#             for c in range(size):
#                 if board[r][c] == 0:
#                     for n in VALID_NUMS:
#                         if n not in rows[r] and n not in cols[c] and n not in boxes[r // SIZE_BOX][c // SIZE_BOX]:
#                             # gán giá trị hợp lệ vào bảng 
#                             board[r][c] = n
#                             # cập nhật tập giá trị có sẵn 
#                             rows[r].add(n)
#                             cols[c].add(n)
#                             boxes[r // SIZE_BOX][c // SIZE_BOX].add(n)

#                             buoc += 1

#                             if callback: # có cập nhật gui -> thực hiện callback 
#                                 callback(r, c, n, "thu", buoc, time.perf_counter() - start)

#                             # delay -> xem log từng bước trên gui 
#                             if delay > 0:
#                                 time.sleep(delay)

#                             if solve():
#                                 if callback:
#                                     callback(r, c, n, "dung", buoc, time.perf_counter() - start)
#                                 return True

#                             # trường hợp bước tiếp theo k có lời giải(k có số nào hợp lệ) -> đệ quy xong -> return false -> thực hiện bước quay lại bước trước đó: 
#                             board[r][c] = 0 # gỡ giá trị hiện thử giá trị hợp lệ khác 
#                             rows[r].remove(n)
#                             cols[c].remove(n)
#                             boxes[r // SIZE_BOX][c // SIZE_BOX].remove(n)
#                             buoc += 1
#                             if callback:
#                                 callback(r, c, n, "sai", buoc, time.perf_counter() - start)
#                             if delay > 0:
#                                 time.sleep(delay)
#                     return False
#         return True

#     return solve(), buoc, time.perf_counter() - start

# # hàm giải sudoku, tính số bước, cờ có giải được k 
# def giai_sudoku_backtracking(bang, size=9, delay=0, cap_nhat_gui=None, isSolve=False):
#     def gui_callback(r, c, n, status, buoc, _):
#         if cap_nhat_gui:
#             cap_nhat_gui(r, c, n, status, buoc)

#     bang_copy = [row[:] for row in bang]
#     isSolve, buoc, _ = backtracking_core(bang_copy, size, gui_callback, delay)
#     return bang_copy, buoc, isSolve

# # hàm ghi log và tính tg 
# def ghi_log_backtracking(bang, size):
#     # Lấy đường dẫn tương đối đến file log trong thư mục data
#     log_path = os.path.join("Sudoku", "data", "log_giai_sudoku.txt")
#     # write -> ghi mới 
#     with open(log_path, "w", encoding="utf-8") as f:
#         f.write("")

#     def log_callback(r, c, n, status, buoc, t):
#         # từ điển ánh xạ trạng thái tướng ứng, nếu k có trạng thái hợp lệ -> return "" 
#         status_txt = {
#             "thu": "Thử giá trị",
#             "dung": "Đúng",
#             "sai": "Sai - backtracking step"
#         }.get(status, "")
#         # append -> thêm vào  
#         with open(log_path, "a", encoding="utf-8") as f: 
#             f.write(f"{buoc}:{t:.4f} ({r},{c}) <- {n} --> {status_txt}\n")

#     bang_copy = [row[:] for row in bang]
#     _, _, duration = backtracking_core(bang_copy, size, log_callback)
#     return duration

# # https://stackoverflow.com/questions/1518346/optimizing-the-backtracking-algorithm-solving-sudoku
# """Chiến lược MRV giúp giải bài Sudoku nhanh hơn, vì:

# Chọn ô có ràng buộc cao → dễ xác định đúng/sai sớm

# Giảm số lượng nhánh trong cây tìm kiếm → tiết kiệm thời gian

# Là kỹ thuật cốt lõi trong Constraint Satisfaction Problem (CSP)"""

import  os, math
from src.algorithm.generate_sudoku import *
from src.utils.utils_ai_screen import *
import time
def backtracking_core(board, size, callback=None, delay=0):
    SIZE_BOX = math.isqrt(size)
    VALID_NUMS = list(range(1, size + 1))

    rows = [set() for _ in range(size)]
    cols = [set() for _ in range(size)]
    boxes = [[set() for _ in range(SIZE_BOX)] for _ in range(SIZE_BOX)]

    for r in range(size):
        for c in range(size):
            val = board[r][c]
            if val:
                rows[r].add(val)
                cols[c].add(val)
                boxes[r // SIZE_BOX][c // SIZE_BOX].add(val)

    start = time.perf_counter()
    buoc = 0

    def solve():
        nonlocal buoc

        min_options = size + 1
        next_cell = None
        candidates = {}

        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    possible = [n for n in VALID_NUMS 
                                if n not in rows[r] 
                                and n not in cols[c] 
                                and n not in boxes[r // SIZE_BOX][c // SIZE_BOX]]
                    candidates[(r, c)] = possible
                    if len(possible) == 0:
                        # Phát hiện ô không thể điền, dừng và backtrack
                        return False
                    if 0 < len(possible) < min_options:
                        min_options = len(possible)
                        next_cell = (r, c)

        if not next_cell:
            # Không còn ô trống, đã giải xong
            return True

        r, c = next_cell
        for n in candidates[next_cell]:
            board[r][c] = n
            rows[r].add(n)
            cols[c].add(n)
            boxes[r // SIZE_BOX][c // SIZE_BOX].add(n)
            buoc += 1

            if callback:
                callback(r, c, n, "thu", buoc, time.perf_counter() - start)
            if delay > 0:
                time.sleep(delay)

            if solve():
                if callback:
                    callback(r, c, n, "dung", buoc, time.perf_counter() - start)
                return True

            board[r][c] = 0
            rows[r].remove(n)
            cols[c].remove(n)
            boxes[r // SIZE_BOX][c // SIZE_BOX].remove(n)
            buoc += 1
            if callback:
                callback(r, c, n, "sai", buoc, time.perf_counter() - start)
            if delay > 0:
                time.sleep(delay)

        return False

    return solve(), buoc, time.perf_counter() - start
# Hàm giải Sudoku cho giao diện
def giai_sudoku_backtracking(bang, size=9, delay=0, cap_nhat_gui=None, isSolve=False):
    def gui_callback(r, c, n, status, buoc, _):
        if cap_nhat_gui:
            cap_nhat_gui(r, c, n, status, buoc)

    bang_copy = [row[:] for row in bang]
    isSolve, buoc, _ = backtracking_core(bang_copy, size, gui_callback, delay)
    return bang_copy, buoc, isSolve

# Ghi log lời giải
def ghi_log_backtracking(bang, size):
    log_path = os.path.join("Sudoku", "data", "log_giai_sudoku.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("")

    def log_callback(r, c, n, status, buoc, t):
        status_txt = {
            "thu": "Thử giá trị",
            "dung": "Đúng",
            "sai": "Sai - backtracking step"
        }.get(status, "")
        with open(log_path, "a", encoding="utf-8") as f: 
            f.write(f"{buoc}:{t:.4f} ({r},{c}) <- {n} --> {status_txt}\n")

    bang_copy = [row[:] for row in bang]
    _, _, duration = backtracking_core(bang_copy, size, log_callback)
    return duration
