
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

def print_board(board):
    for row in board:
        print(" ".join(str(cell) if cell != 0 else "." for cell in row))
    print()

def test_hill_climbing_4x4():
    board_4x4 = [
        [1, 0, 0, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [3, 0, 0, 2]
    ]

    print("Input Board:")
    print_board(board_4x4)

    result_board, steps, elapsed = hill_climbing_core(board_4x4, 4)

    print("Result Board:")
    print_board(result_board)

    print(f"Solved in {steps} steps, Time: {elapsed:.4f} seconds")

# Chạy test
test_hill_climbing_4x4()
