import json  # Thư viện để làm việc với định dạng dữ liệu JSON
import random  # Thư viện để sinh số ngẫu nhiên
import math  # Thư viện toán học, dùng để tính căn bậc hai
import os  # Thư viện để làm việc với hệ thống tệp tin và thư mục

def sinh_bang_sudoku_day_du(side):
    """Hàm sinh bảng Sudoku đầy đủ với kích thước side x side."""
    base = int(math.isqrt(side))  # Tính căn bậc hai của side, đây là kích thước của mỗi ô vuông nhỏ
    if base * base != side:  # Kiểm tra xem side có phải là số chính phương không
        raise ValueError("Kích thước phải là số chính phương.")  # Nếu không phải, ném lỗi

    def pattern(r, c):
        """Hàm xác định vị trí của một số trong bảng Sudoku đầy đủ."""
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        """Hàm xáo trộn danh sách s ngẫu nhiên."""
        return random.sample(s, len(s))  # Trả về một phiên bản xáo trộn ngẫu nhiên của danh sách s

    r_base = range(base)  # Tạo dãy các giá trị từ 0 đến base-1
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]  # Tạo các hàng ngẫu nhiên
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]  # Tạo các cột ngẫu nhiên
    nums = shuffle(range(1, side + 1))  # Xáo trộn các số từ 1 đến side
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]  # Tạo bảng Sudoku đầy đủ theo mẫu
    return board  # Trả về bảng Sudoku đầy đủ

def xoa_o_ngau_nhien(board, so_o_can_xoa):
    """Hàm xóa các ô ngẫu nhiên trong bảng Sudoku."""
    n = len(board)  # Lấy kích thước bảng
    board_copy = [row[:] for row in board]  # Tạo bản sao của bảng Sudoku
    positions = [(i, j) for i in range(n) for j in range(n)]  # Tạo danh sách tất cả các vị trí trong bảng
    random.shuffle(positions)  # Xáo trộn danh sách vị trí
    removed = 0  # Biến đếm số ô đã bị xóa
    while removed < so_o_can_xoa and positions:  # Vòng lặp xóa ô cho đến khi đủ số lượng cần xóa
        i, j = positions.pop()  # Lấy ngẫu nhiên một vị trí
        if board_copy[i][j] != 0:  # Nếu ô không phải là ô đã xóa (có giá trị khác 0)
            board_copy[i][j] = 0  # Đặt ô này thành 0 (xóa)
            removed += 1  # Tăng số lượng ô đã xóa lên
    return board_copy  # Trả về bảng đã xóa ô ngẫu nhiên

def tao_sudoku_theo_cap_do(size, level="E"):
    """Hàm tạo một bảng Sudoku thiếu với cấp độ khó từ cấp độ 'E', 'M', 'H'."""
    total_cells = size * size  # Tổng số ô trong bảng
    tile_to_remove = {
        "E": int(total_cells * 0.2),  # Cấp độ dễ, xóa 20% số ô
        "M": int(total_cells * 0.4),  # Cấp độ trung bình, xóa 40% số ô
        "H": int(total_cells * 1)   # Cấp độ khó, xóa 80% số ô
    }
    sudoku_day_du = sinh_bang_sudoku_day_du(size)  # Sinh bảng Sudoku đầy đủ
    sudoku_thieu = xoa_o_ngau_nhien(sudoku_day_du, tile_to_remove[level])  # Xóa các ô ngẫu nhiên theo cấp độ
    return sudoku_thieu  # Trả về bảng Sudoku thiếu

def sinh_va_luu_de(size=9, num_bo_moi_cap_do=100):
    """Hàm sinh và lưu bộ dữ liệu Sudoku vào file JSON."""
    file_name = f"sudoku_{size}x{size}_dataset.json"  # Đặt tên file lưu dữ liệu
    output_path = os.path.join("Sudoku", "data", file_name)  # Đường dẫn file

    dataset = {"E": [], "M": [], "H": []}  # Khởi tạo từ điển để lưu bộ dữ liệu cho từng cấp độ
    for level in ["E", "M", "H"]:  # Lặp qua các cấp độ dễ, trung bình và khó
        print(f"Sinh {num_bo_moi_cap_do} đề cấp độ {level} ({size}x{size})...")  # In thông báo sinh dữ liệu
        for _ in range(num_bo_moi_cap_do):  # Lặp số lần cần sinh bộ đề
            board = tao_sudoku_theo_cap_do(size, level)  # Sinh một bảng Sudoku thiếu theo cấp độ
            dataset[level].append(board)  # Thêm bảng vào danh sách cấp độ tương ứng

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f)  # Lưu bộ dữ liệu vào file JSON
    print(f"Đã lưu vào: {output_path}")  # In thông báo hoàn thành lưu file

def tao_sudoku_theo_cap_do(size, level):
    """Lấy ngẫu nhiên 1 đề từ file JSON tương ứng với size và cấp độ."""
    file_path = os.path.join("Sudoku", "data", f"sudoku_{size}x{size}_dataset.json")  # Đường dẫn tới file dữ liệu

    if not os.path.exists(file_path):  # Kiểm tra xem file có tồn tại không
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")  # Nếu không có file, ném lỗi

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)  # Đọc dữ liệu từ file JSON

    if level not in data:  # Kiểm tra xem cấp độ có hợp lệ không
        raise ValueError(f"Cấp độ '{level}' không hợp lệ. Các cấp độ hợp lệ: {list(data.keys())}")  # Nếu không hợp lệ, ném lỗi

    danh_sach_de = data[level]  # Lấy danh sách các đề của cấp độ
    de_ngau_nhien = random.choice(danh_sach_de)  # Chọn ngẫu nhiên một đề từ danh sách
    return de_ngau_nhien  # Trả về đề ngẫu nhiên

# ======= Chạy =======
if __name__ == "__main__":
    sinh_va_luu_de(size=9)
    sinh_va_luu_de(size=16)
    sinh_va_luu_de(size=25)
