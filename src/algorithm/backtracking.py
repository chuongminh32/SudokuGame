# def is_valid(board, row, col, num):
#     """
#     Kiểm tra nếu có thể đặt số vào ô.
#     Hàm này kiểm tra xem có thể đặt số 'num' vào vị trí (row, col) trên bảng 'board' hay không.
#     Điều kiện để đặt số hợp lệ là:
#     - Số 'num' không xuất hiện trong hàng 'row'.
#     - Số 'num' không xuất hiện trong cột 'col'.
#     - Số 'num' không xuất hiện trong ô vuông 3x3 chứa vị trí (row, col).
#     Args:
#         board (list of list of int): Bảng Sudoku hiện tại.
#         row (int): Chỉ số hàng của ô cần kiểm tra.
#         col (int): Chỉ số cột của ô cần kiểm tra.
#         num (int): Số cần kiểm tra.
#     Returns:
#         bool: Trả về True nếu có thể đặt số 'num' vào ô (row, col), ngược lại trả về False.
#     """
#     """Kiểm tra nếu có thể đặt số vào ô"""
#     for i in range(9):
#         if board[row][i] == num or board[i][col] == num:
#             return False
    
#     start_row, start_col = (row // 3) * 3, (col // 3) * 3
#     for i in range(3):
#         for j in range(3):
#             if board[start_row + i][start_col + j] == num:
#                 return False
#     return True

# def solve_sudoku(board):
#     """Giải Sudoku bằng thuật toán Backtracking"""
#     for row in range(9):
#         for col in range(9):
#             # Nếu ô hiện tại trống (giá trị là 0)
#             if board[row][col] == 0:
#                 # Thử các số từ 1 đến 9
#                 for num in range(1, 10):
#                     # Kiểm tra nếu số có thể đặt vào ô
#                     if is_valid(board, row, col, num):
#                         # Đặt số vào ô
#                         board[row][col] = num
#                         # Đệ quy để tiếp tục giải các ô tiếp theo
#                         if solve_sudoku(board):
#                             return True
#                         # Nếu không giải được, quay lui và đặt lại ô về 0
#                         board[row][col] = 0
#                 # Nếu không có số nào hợp lệ, trả về False
#                 return False
#     # Nếu tất cả các ô đã được điền hợp lệ, trả về True
#     return True


