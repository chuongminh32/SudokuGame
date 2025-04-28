import random
import math

def sinh_bang_sudoku_ngau_nhien(side):
    """Tạo một bảng Sudoku hoàn chỉnh với kích thước bất kỳ (base x base)."""
    # Kiểm tra xem side có phải là số nguyên không, nếu là chuỗi thì chuyển thành số nguyên
    try:
        side = int(side)
    except ValueError:
        raise ValueError("Kích thước side phải là một số nguyên hợp lệ.")

    base = int(math.isqrt(side))

    # Kiểm tra xem side có phải là một số chính phương không
    if base * base != side:
        raise ValueError("Kích thước side phải là một số chính phương.")

    # Hàm này tính toán vị trí của mỗi số trong bảng Sudoku
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # Hàm xáo trộn các danh sách, giúp tạo ra sự ngẫu nhiên
    def shuffle(s):
        return random.sample(s, len(s))  # Trả về danh sách xáo trộn ngẫu nhiên

    r_base = range(base)  # Dãy số từ 0 đến base-1

    # Tạo danh sách các hàng và cột ngẫu nhiên dựa trên các số từ r_base
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]

    # Xáo trộn các số từ 1 đến side để sử dụng trong bảng
    nums = shuffle(range(1, side + 1))

    # Tạo bảng Sudoku hoàn chỉnh bằng cách áp dụng hàm pattern cho từng hàng, cột
    sudoku = []
    for r in rows:
        sudoku_row = []
        for c in cols:
            sudoku_row.append(nums[pattern(r, c)])  # Sắp xếp các số vào bảng
        sudoku.append(sudoku_row)

    return sudoku

def xoaSoNgauNhien(board, num_to_remove):
    """Xóa một số lượng ô khỏi bảng Sudoku."""
    positions = [(i, j) for i in range(len(board)) for j in range(len(board[0]))]
    random.shuffle(positions)

    board_copy = [row[:] for row in board]  # Tạo bản sao tránh sửa bảng gốc

    for _ in range(num_to_remove):
        row, col = positions.pop()
        board_copy[row][col] = 0

    return board_copy

def layBangSuDoKuTheoCapDo(side, level="E"):
    """Tạo bảng Sudoku theo cấp độ và kích thước tùy chọn."""
    c = side * side
    b = sinh_bang_sudoku_ngau_nhien(side)

    CapDo = {
    "E": int(0.2 * c),  # 60% ô giữ lại cho cấp độ dễ
    "M": int(0.3 * c),  # 30% ô giữ lại cho cấp độ trung bình
    "H": int(0.4 * c),  # Giảm số lượng ô xóa cho cấp độ khó (chỉ xóa 50%)
}


    if level not in CapDo:
        raise ValueError("Cấp độ không hợp lệ. Chọn 'E', 'M', 'H'.")

    return xoaSoNgauNhien(b, CapDo[level])
