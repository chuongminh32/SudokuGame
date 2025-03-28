# # src/algorithm/solver.py
# import sys, os 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from src.algorithm.hill_climbing import hill_climbing_sudoku
# from src.algorithm.backtracking import backtracking_sudoku

# def solve_sudoku(board, method="hill_climbing"):
#     """
#     Giải bài toán Sudoku với phương pháp được chọn.
    
#     Args:
#         board (list[list[int]]): Bảng Sudoku 9x9.
#         method (str): 'hill_climbing' hoặc 'backtracking'.
    
#     Returns:
#         list[list[int]] hoặc None nếu không tìm thấy lời giải.
#     """
#     if method == "hill_climbing":
#         return hill_climbing_sudoku(board)
#     elif method == "backtracking":
#         return backtracking_sudoku(board)
#     else:
#         raise ValueError("Phương pháp không hợp lệ!")
