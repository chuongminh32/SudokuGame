import sys, os, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *
from src.utils.utils_ai_screen import *

import time

# Trả về bảng giải, số bước và log (nếu có)
def giai_sudoku_backtracking(bang, size, delay, cap_nhat_gui=None , isSolve = False):
    
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

    def solve(bang):
        nonlocal so_buoc
        for row in range(size):
            for col in range(size):
                if bang[row][col] == 0:
                    for num in range(1, size + 1):
                        if hop_le(bang, row, col, num):
                            bang[row][col] = num
                            so_buoc += 1

                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, num, "thu", so_buoc)
                                time.sleep(delay)

                            if solve(bang):
                                if cap_nhat_gui:
                                    cap_nhat_gui(row, col, num, "dung", so_buoc)
                                    time.sleep(delay)
                                return True

                            # Quay lui
                            bang[row][col] = 0
                            so_buoc += 1
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, num, "sai", so_buoc)
                                time.sleep(delay)
                    return False
        return True


    bang_copy = [row[:] for row in bang]  # Copy bảng ban đầu để giữ nguyên
    if solve(bang_copy):
        isSolve = True  

    return bang_copy, so_buoc, isSolve


def ghi_log_backtracking(b, size):
    from src.utils.utils_ai_screen import get_relative_path
    import os, math, time

    log_path = get_relative_path("data", "log_giai_sudoku.txt")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8"): pass  # clear log

    box = math.isqrt(size)

    def ghi_log(dong):
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(dong + "\n")

    def hop_le(b, r, c, n):
        if any(b[r][i] == n or b[i][c] == n for i in range(size)): return False
        sr, sc = box * (r // box), box * (c // box)
        return all(b[i][j] != n for i in range(sr, sr + box) for j in range(sc, sc + box))

    buoc = 0
    start = time.perf_counter()

    def solve(b):
        nonlocal buoc
        for r in range(size):
            for c in range(size):
                if b[r][c] == 0:
                    for n in range(1, size + 1):
                        if hop_le(b, r, c, n):
                            b[r][c] = n
                            buoc += 1
                            t = time.perf_counter() - start
                            ghi_log(f"[Bước {buoc}] [Time: {t:.4f}s] ({r},{c}) <- {n} --> Thử giá trị")
                            if solve(b): 
                                ghi_log(f"[Bước {buoc}] [Time: {t:.4f}s] ({r},{c}) <- {n} --> Đúng")
                                return True
                            b[r][c] = 0
                            buoc += 1
                            t = time.perf_counter() - start
                            ghi_log(f"[Bước {buoc}] [Time: {t:.4f}s] ({r},{c}) <- {n} --> Sai - backtracking step")
                    return False
        return True

    b_copy = [row[:] for row in b]  # tránh thay đổi bảng gốc
    solve(b_copy)
    return time.perf_counter() - start
