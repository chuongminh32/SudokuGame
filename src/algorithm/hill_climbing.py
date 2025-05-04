import sys, os, math, random, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *
from src.utils.utils_ai_screen import *

# Trả về các giá trị hợp lệ chưa xuất hiện trong hàng, cột, và ô vuông
def get_safe_values(board, n, row, col):
    sqrt_n = int(math.sqrt(n))
    start_row = (row // sqrt_n) * sqrt_n
    start_col = (col // sqrt_n) * sqrt_n

    used = set()

    # Trong hàng
    used.update(board[row])

    # Trong cột
    used.update(board[i][col] for i in range(n))

    # Trong ô vuông
    for i in range(sqrt_n):
        for j in range(sqrt_n):
            used.add(board[start_row + i][start_col + j])

    return [val for val in range(1, n + 1) if val not in used]

def count_conflicts(board, n):
    conflicts = 0

    # Đếm mỗi ô 0 là một xung đột
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                conflicts += 1

    # Kiểm tra xung đột trong hàng
    for i in range(n):
        nums = [x for x in board[i] if x != 0]
        conflicts += len(nums) - len(set(nums))  # Số lần trùng trong hàng

    # Kiểm tra xung đột trong cột
    for j in range(n):
        nums = [board[i][j] for i in range(n) if board[i][j] != 0]
        conflicts += len(nums) - len(set(nums))  # Số lần trùng trong cột

    # Kiểm tra xung đột trong các ô vuông con sqrt(n) x sqrt(n)
    sqrt_n = int(math.sqrt(n))
    for row_start in range(0, n, sqrt_n):
        for col_start in range(0, n, sqrt_n):
            block = []
            for i in range(sqrt_n):
                for j in range(sqrt_n):
                    val = board[row_start + i][col_start + j]
                    if val != 0:
                        block.append(val)
            conflicts += len(block) - len(set(block))  # Số lần trùng trong block

    return conflicts


# Hàm kiểm tra lời giải hợp lệ
def is_valid_solution(board, n):
    return count_conflicts(board, n) == 0

# Hill Climbing core (chấp nhận <= conflict và chỉ dùng số hợp lệ)
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
                    available_values = get_safe_values(board, size, r, c)

                    for n in available_values:
                        board[r][c] = n
                        new_conflicts = count_conflicts(board, size)
                        buoc += 1

                        if callback:
                            status = "improved" if new_conflicts < current_conflicts else "conflict"
                            callback(r, c, n, status, buoc, time.perf_counter() - start, new_conflicts)
                        if delay > 0:
                            time.sleep(delay)

                        if new_conflicts <= current_conflicts:
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

# Giải Sudoku dùng Hill Climbing cho giao diện
def giai_sudoku_hill_climbing(bang, size=9, delay=0, cap_nhat_gui=None, isSolve=False):
    def gui_callback(r, c, n, status, buoc, thoi_gian, conflicts):
        if cap_nhat_gui:
            cap_nhat_gui(r, c, n, status, buoc, thoi_gian, conflicts)

    bang_copy = [row[:] for row in bang]
    ketqua, buoc, _ = hill_climbing_core(bang_copy, size, gui_callback, delay)
    is_valid = is_valid_solution(ketqua, size)
    return ketqua, buoc, is_valid

# Ghi log quá trình Hill Climbing và kiểm tra hợp lệ cuối cùng
def ghi_log_hill_climbing(bang, size):
    log_path = os.path.join("Sudoku", "data", "log_hill_climbing.txt")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("")

    def log_callback(r, c, n, status, buoc, t, conflicts):
        status_txt = {
            "improved": "Cải thiện",
            "no_improvement": "Không cải thiện",
            "conflict": "Lỗi - Vi phạm quy tắc"
        }.get(status, "")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{buoc}:{t:.4f}s | Conflicts: {conflicts} | ({r},{c}) <- {n} --> {status_txt}\n")

    bang_copy = [row[:] for row in bang]
    ketqua, _, duration = hill_climbing_core(bang_copy, size, log_callback)
    is_valid = is_valid_solution(ketqua, size)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n==> Lời giải {'HỢP LỆ' if is_valid else 'KHÔNG hợp lệ'} sau {duration:.4f}s\n")

    return duration

