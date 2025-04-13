import random 
# phan chia cấp ____________
def sinh_bang_sudoku_ngau_nhien():
    """Tạo một bảng Sudoku hoàn chỉnh.
    Được dùng để tính toán vị trí số cho từng ô trong bảng Sudoku, đảm bảo tuân thủ các quy tắc Sudoku. Cụ thể:
    base * (r % base): Tính vị trí của hàng trong mỗi khối 3x3 (chỉ lấy phần dư khi chia hàng cho base).
    r // base: Xác định khối (block) mà hàng thuộc về.
    c: Cộng cột vào để xác định vị trí chính xác của số.
    % side: Đảm bảo kết quả nằm trong phạm vi 9x9 bằng cách lấy phần dư với side (tức 9).
    Công thức này giúp đảm bảo các số được sắp xếp hợp lý theo các khối và quy tắc của Sudoku.
    """
    base = 3  # Kích thước của khu vực 3x3 (tức là Sudoku 9x9)
    side = base * base  # Tổng số hàng và cột là 9

    # Hàm này tính toán vị trí của mỗi số trong bảng Sudoku
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # Hàm xáo trộn các danh sách, giúp tạo ra sự ngẫu nhiên
    def shuffle(s):
        return random.sample(s, len(s))  # Trả về danh sách xáo trộn ngẫu nhiên

    r_base = range(base)  # Dãy số từ 0 đến base-1 (từ 0 đến 2)
    
    # Tạo danh sách các hàng và cột ngẫu nhiên dựa trên các số từ r_base
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]

    # Xáo trộn các số từ 1 đến 9 để sử dụng trong bảng
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
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    board_copy = [row[:] for row in board]  # Tạo bản sao tránh sửa bảng gốc
    
    for _ in range(num_to_remove):
        row, col = positions.pop()
        board_copy[row][col] = 0
    
    return board_copy

def layBangSuDoKuTheoCapDo(level="E"):
    """Tạo bảng Sudoku theo cấp độ."""
    bangDaGiai = sinh_bang_sudoku_ngau_nhien()

    CapDo = {
        "E": 20,
        "M": 30,
        "H": 40,
    }
    
    if level not in CapDo:
        raise ValueError("Cấp độ không hợp lệ. Chọn 'E', 'M', 'H'.")

    return xoaSoNgauNhien(bangDaGiai, CapDo[level])