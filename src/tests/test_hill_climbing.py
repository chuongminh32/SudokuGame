import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.hill_climbing import (
    hill_climbing_core, ghi_log_hill_climbing, is_valid_solution
)
# Đề hợp lệ
valid_board_4x4 = [
    [1, 0, 3, 4],
    [0, 4, 0, 0],
    [0, 0, 0, 3],
    [4, 3, 0, 0]
]

# Đề không hợp lệ
invalid_board_4x4 = [
    [4, 0, 3, 4],
    [0, 4, 0, 0],
    [0, 0, 0, 3],
    [4, 3, 0, 0]
]

def print_board(board):
    for row in board:
        print(" ".join(str(cell) if cell != 0 else '.' for cell in row))
    print()

def test_board(title, board):
    print(f"--- {title} ---")
    print("Input board:")
    print_board(board)

    solved_board, steps, duration = hill_climbing_core(board, 4)
    is_valid = is_valid_solution(solved_board, 4)

    print("Solved board:")
    print_board(solved_board)
    print(f"Steps: {steps}")
    print(f"Duration: {duration:.4f}s")
    print(f"Valid Solution: {'Yes' if is_valid else 'No'}\n")

    # Ghi log cho đề đó
    print(f"Đang ghi log vào file log_HC.txt...\n")
    ghi_log_hill_climbing(board, 4)

if __name__ == "__main__":
    os.makedirs("SudokuGame/data", exist_ok=True)

    # Test đề hợp lệ
    test_board("Test đề hợp lệ", valid_board_4x4)

    # Test đề không hợp lệ
    test_board("Test đề không hợp lệ", invalid_board_4x4)
