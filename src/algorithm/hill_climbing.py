import sys, os, math, random, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *
from src.utils.utils_ai_screen import *

 # Hàm kiểm tra tính hợp lệ của bảng Sudoku
def is_valid_sudoku(board, n):
     # Kiểm tra các hàng
     for i in range(n):
         if len(set(board[i])) != n:
             return False
 
     # Kiểm tra các cột
     for i in range(n):
         if len(set(board[j][i] for j in range(n))) != n:
             return False
 
     # Kiểm tra các khối con sqrt(n) x sqrt(n)
     sqrt_n = int(math.sqrt(n))
     for row_start in range(0, n, sqrt_n):
         for col_start in range(0, n, sqrt_n):
             block = []
             for i in range(sqrt_n):
                 for j in range(sqrt_n):
                     block.append(board[row_start + i][col_start + j])
             if len(set(block)) != n:
                 return False
 
     return True

 # Hàm tính số lỗi trong bảng (số vi phạm quy tắc về hàng, cột và vùng)
def count_conflicts(board, n):
     conflicts = 0
 
     # Kiểm tra hàng và cột
     for i in range(n):
         conflicts += n - len(set(board[i]))  # Vi phạm trong hàng
         conflicts += n - len(set([board[j][i] for j in range(n)]))  # Vi phạm trong cột
 
     # Kiểm tra các khối con sqrt(n) x sqrt(n)
     sqrt_n = int(math.sqrt(n))
     for row_start in range(0, n, sqrt_n):
         for col_start in range(0, n, sqrt_n):
             block = []
             for i in range(sqrt_n):
                 for j in range(sqrt_n):
                     block.append(board[row_start + i][col_start + j])
             conflicts += n - len(set(block))  # Vi phạm trong khối con
 
     return conflicts

def hill_climbing_core(board, size, callback=None, delay=0):
    start = time.perf_counter()
    buoc = 0
    current_conflicts = count_conflicts(board, size)
    best_board = [row[:] for row in board]
    best_conflicts = current_conflicts

    while current_conflicts > 0:
        improved = False

        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    original = board[r][c]
                    for n in range(1, size + 1):
                        board[r][c] = n
                        new_conflicts = count_conflicts(board, size)
                        buoc += 1

                        # ====== gui =====
                        if callback:
                            if new_conflicts < current_conflicts:
                                callback(r, c, n, "improved", buoc, time.perf_counter() - start, new_conflicts)
                            else:
                                callback(r, c, n, "conflict", buoc, time.perf_counter() - start, new_conflicts)
                        if delay > 0:
                            time.sleep(delay)
                        # ====== gui =====

                        if new_conflicts < current_conflicts:
                            current_conflicts = new_conflicts
                            best_conflicts = new_conflicts
                            best_board = [row[:] for row in board]
                            improved = True
                            break

                    if not improved:
                        board[r][c] = original
            if improved:
                break

        if not improved:
            if callback:
                callback(r, c, board[r][c], "no_improvement", buoc, time.perf_counter() - start, current_conflicts)
            break

    return best_board, buoc, time.perf_counter() - start

# Hàm giải Sudoku Hill Climbing dùng cho GUI
def giai_sudoku_hill_climbing(bang, size=9, delay=0, cap_nhat_gui=None, isSolve=False):
    def gui_callback(r, c, n, status, buoc, thoi_gian, conflicts):
        if cap_nhat_gui:
            cap_nhat_gui(r, c, n, status, buoc, thoi_gian, conflicts)

    bang_copy = [row[:] for row in bang]
    ketqua, buoc, _ = hill_climbing_core(bang_copy, size, gui_callback, delay)
    return ketqua, buoc, is_valid_solution(ketqua, size)

# Hàm ghi log thuật toán Hill Climbing
def ghi_log_hill_climbing(bang, size):
    log_path = os.path.join("Sudoku", "data", "log_hill_climbing.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("")

    def log_callback(r, c, n, status, buoc, t, conflicts):
        status_txt = {
            "improved": "Cải thiện",
            "no_improvement": "Không cải thiện",
            "conflict": "Lỗi - Vi phạm quy tắc"
        }.get(status, "")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{buoc}:{t:.4f} | conflicts: {conflicts} ({r},{c}) <- {n} --> {status_txt}\n")

    bang_copy = [row[:] for row in bang]
    _, _, duration = hill_climbing_core(bang_copy, size, log_callback)
    return duration

# Hàm kiểm tra nếu lời giải là hợp lệ (giống backtracking)
def is_valid_solution(board, n):
    return count_conflicts(board, n) == 0
