import random
import math
import os
import json
from datetime import datetime
import time

# Tính số xung đột của bảng Sudoku
def count_conflicts(board, n):
    conflicts = 0
    for i in range(n):
        conflicts += n - len(set(board[i]))  # Hàng
        conflicts += n - len(set([board[j][i] for j in range(n)]))  # Cột

    sqrt_n = int(math.sqrt(n))
    for row_start in range(0, n, sqrt_n):
        for col_start in range(0, n, sqrt_n):
            block = []
            for i in range(sqrt_n):
                for j in range(sqrt_n):
                    block.append(board[row_start + i][col_start + j])
            conflicts += n - len(set(block))  # Vùng con

    return conflicts

def get_block_used_numbers(board, n, row, col):
    """
    Trả về tập hợp các số đã dùng trong khối con sqrt(n) x sqrt(n) chứa ô (row, col)
    """
    sqrt_n = int(math.sqrt(n))
    block_values = set()
    start_row, start_col = (row // sqrt_n) * sqrt_n, (col // sqrt_n) * sqrt_n
    for i in range(sqrt_n):
        for j in range(sqrt_n):
            val = board[start_row + i][start_col + j]
            if val != 0:
                block_values.add(val)
    return block_values


# Hàm giải Sudoku bằng thuật toán Hill Climbing và ghi log
def hill_climbing_solving(board, n, log_callback=None):
    """
    Giải bảng Sudoku bằng thuật toán Hill Climbing và ghi lại quá trình giải.
    
    Args:
        board (list): Bảng Sudoku ban đầu, là một danh sách 2D chứa các giá trị.
        n (int): Kích thước bảng Sudoku.
        log_callback (function, optional): Hàm callback để ghi log quá trình giải. Mặc định là None.

    Returns:
        list: Bảng Sudoku đã được giải, hoặc gần như giải được.
    """
    current_conflicts = count_conflicts(board, n)
    best_board = [row[:] for row in board]
    best_conflicts = current_conflicts

    steps = 0
    start_time = time.perf_counter()  # Thời gian bắt đầu
    while current_conflicts > 0:
        improved = False
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    original_value = board[i][j]
                    used_in_block = get_block_used_numbers(board, n, i, j)
                    available_values = [val for val in range(1, n + 1) if val not in used_in_block]
                    random.shuffle(available_values)

                    for new_value in available_values:
                        board[i][j] = new_value
                        new_conflicts = count_conflicts(board, n)

                        if new_conflicts < current_conflicts:
                            current_conflicts = new_conflicts
                            if new_conflicts < best_conflicts:
                                best_conflicts = new_conflicts
                                best_board = [row[:] for row in board]
                            improved = True
                            if log_callback:
                                log_callback(i, j, new_value, "thu", steps + 1, current_conflicts, time.perf_counter() - start_time)  # Thử giá trị
                            break

                    if not improved:
                        board[i][j] = original_value
                        if log_callback:
                            log_callback(i, j, new_value, "sai", steps + 1, current_conflicts, time.perf_counter() - start_time)  # Sai - backtracking

            if improved:
                break

        steps += 1
        if log_callback:
            log_callback(i, j, new_value, "dung", steps, current_conflicts, time.perf_counter() - start_time)  # Đúng

        if not improved:
            break

    end_time = time.perf_counter()  # Thời gian kết thúc
    total_time = end_time - start_time
    return best_board, total_time

# Ghi log ra file .txt trong thư mục sudoku/logs
def ghi_log_hill_climbing(board, n):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_folder = os.path.join("sudoku", "logs")
    os.makedirs(log_folder, exist_ok=True)
    log_path = os.path.join(log_folder, f"hill_climbing_log_{timestamp}.txt")

    with open(log_path, "w", encoding="utf-8") as log_file:
        def log_callback(r, c, n, status, step, conflicts, t):
            status_txt = {
                "thu": "Thử giá trị",
                "dung": "Đúng",
                "sai": "Sai"
            }.get(status, "")
            log_file.write(f"Step {step}: {t:.4f}s - ({r},{c}) <- {n} --> {status_txt} | Conflicts = {conflicts}\n")

        solved_board, total_time = hill_climbing_solving(board, n, log_callback)

    # In thời gian tổng sau khi kết thúc
    print(f"Total time for solving: {total_time:.4f}s")
    return solved_board

# Lấy đề và lời giải từ file JSON
def tao_sudoku_theo_cap_do(size, level):
    file_path = os.path.join("Sudoku", "data", f"sudoku_{size}x{size}_dataset.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if level not in data:
        raise ValueError(f"Cấp độ '{level}' không hợp lệ. Các cấp độ hợp lệ: {list(data.keys())}")

    danh_sach_de = data[level]
    de_ngau_nhien = random.choice(danh_sach_de)

    return de_ngau_nhien["question"], de_ngau_nhien["solution"]

# Hàm test để chạy thử Hill Climbing và ghi log
def test_hill_climbing():
    print("Testing Hill Climbing algorithm on Sudoku from JSON data...")
    # Lấy đề từ file JSON
    level = "E"  # Bạn có thể thay đổi cấp độ ở đây (E, M, H)
    size = 9  # Kích thước bảng Sudoku
    question, solution = tao_sudoku_theo_cap_do(size, level)

    print("Initial Sudoku Board (Question):")
    for row in question:
        print(row)

    solved_board = ghi_log_hill_climbing(question, size)

    print("\nSolved Sudoku Board:")
    for row in solved_board:
        print(row)

if __name__ == "__main__":
    test_hill_climbing()
