# viết như cấu trúc backtracking 
# vẽ đồ thị phân tích trong utils_ai_screen.py phần biểu đồ (vẽ theo logic thuật toán: biểu diễn số bước , thời gian ,...)
import random
import math

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

# Hàm kiểm tra nếu có thể điền số vào ô (i, j)
def is_safe(board, n, row, col, num):
    # Kiểm tra hàng
    if num in board[row]:
        return False

    # Kiểm tra cột
    for i in range(n):
        if board[i][col] == num:
            return False

    # Kiểm tra khối con
    sqrt_n = int(math.sqrt(n))
    start_row, start_col = (row // sqrt_n) * sqrt_n, (col // sqrt_n) * sqrt_n
    for i in range(sqrt_n):
        for j in range(sqrt_n):
            if board[start_row + i][start_col + j] == num:
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

# Hàm thực hiện thuật toán Hill Climbing
def hill_climbing(board, n):
    current_conflicts = count_conflicts(board, n)
    best_board = [row[:] for row in board]
    best_conflicts = current_conflicts

    while current_conflicts > 0:
        improved = False

        # Duyệt qua các ô trống trong bảng để tìm cách thay đổi
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    # Lưu lại giá trị ban đầu
                    original_value = board[i][j]
                    available_values = list(range(1, n + 1))

                    # Thử các giá trị có thể đi vào ô trống
                    for new_value in available_values:
                        board[i][j] = new_value
                        new_conflicts = count_conflicts(board, n)

                        # Nếu số lỗi giảm, cập nhật bảng
                        if new_conflicts < current_conflicts:
                            current_conflicts = new_conflicts
                            if new_conflicts < best_conflicts:
                                best_conflicts = new_conflicts
                                best_board = [row[:] for row in board]
                            improved = True
                            break

                    # Khôi phục giá trị ban đầu nếu không có cải thiện
                    if not improved:
                        board[i][j] = original_value

            if improved:
                break

        if not improved:
            break

    return best_board

# Hàm in bảng Sudoku
def print_board(board, n):
    for row in board:
        print(" ".join(str(cell) if cell != 0 else '.' for cell in row))

def ghi_log_hill_climbing(bang, size):
    # Lấy đường dẫn tương đối đến file log trong thư mục data
    log_path = os.path.join("Sudoku", "data", "log_hill_climbing.txt")
    
    # Ghi mới nội dung của file log
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("")  # Xóa nội dung file log cũ nếu có

    def log_callback(r, c, n, status, buoc, t):
        # Từ điển ánh xạ trạng thái tương ứng, nếu không có trạng thái hợp lệ -> return ""
        status_txt = {
            "improved": "Cải thiện",
            "no_improvement": "Không cải thiện",
            "conflict": "Lỗi - Vi phạm quy tắc"
        }.get(status, "")
        
        # Ghi vào log
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{buoc}:{t:.4f} ({r},{c}) <- {n} --> {status_txt}\n")
    
    bang_copy = [row[:] for row in bang]  # Sao chép bảng Sudoku ban đầu
    duration = hill_climbing_with_logging(bang_copy, size, log_callback)  # Hàm thực hiện Hill Climbing có logging
    return duration

# Hàm Hill Climbing với logging
def hill_climbing_with_logging(board, n, log_callback):
    current_conflicts = count_conflicts(board, n)
    best_board = [row[:] for row in board]
    best_conflicts = current_conflicts
    step = 1  # Biến đếm số bước
    start_time = time.time()  # Lấy thời gian bắt đầu

    while current_conflicts > 0:
        improved = False

        # Duyệt qua các ô trống trong bảng để tìm cách thay đổi
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    original_value = board[i][j]
                    available_values = list(range(1, n + 1))

                    # Thử các giá trị có thể đi vào ô trống
                    for new_value in available_values:
                        board[i][j] = new_value
                        new_conflicts = count_conflicts(board, n)

                        # Kiểm tra nếu số lỗi giảm
                        if new_conflicts < current_conflicts:
                            current_conflicts = new_conflicts
                            if new_conflicts < best_conflicts:
                                best_conflicts = new_conflicts
                                best_board = [row[:] for row in board]
                            improved = True
                            log_callback(i, j, new_value, "improved", step, time.time() - start_time)
                            break
                        else:
                            log_callback(i, j, new_value, "conflict", step, time.time() - start_time)

                    # Khôi phục giá trị ban đầu nếu không có cải thiện
                    if not improved:
                        board[i][j] = original_value

            if improved:
                break

        if not improved:
            log_callback(i, j, original_value, "no_improvement", step, time.time() - start_time)
            break
        
        step += 1  # Tăng số bước sau mỗi vòng lặp

    return time.time() - start_time  # Trả về thời gian chạy

