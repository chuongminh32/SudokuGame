
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
    tong_so_o = size * size  # Tổng số ô trong bảng
    cap_do = {
        "E": int(tong_so_o * 0.2),  # Cấp độ dễ, xóa 20% số ô
        "M": int(tong_so_o * 0.4),  # Cấp độ trung bình, xóa 40% số ô
        "H": int(tong_so_o * 0.6)   # Cấp độ khó, xóa 60% số ô
    }
    sudoku_day_du = sinh_bang_sudoku_day_du(size)  # Sinh bảng Sudoku đầy đủ
    sudoku_thieu = xoa_o_ngau_nhien(sudoku_day_du, cap_do[level])  # Xóa các ô ngẫu nhiên theo cấp độ
    return sudoku_thieu  # Trả về bảng Sudoku thiếu -> đề

def sinh_va_luu_de(size=9, tong_so_de=100):
    """Hàm sinh và lưu đề Sudoku + lời giải vào file JSON."""
    file_name = f"sudoku_{size}x{size}_dataset.json"
    output_path = os.path.join("SudokuGame", "data", file_name)
    print(output_path)

    dataset = {"E": [], "M": [], "H": []}

    for level in ["E", "M", "H"]:
        print(f"Sinh {tong_so_de} đề cấp độ {level} ({size}x{size})...")
        tong_so_o = size * size
        # từ điển ánh xạ tương ứng với cấp độ
        so_o_xoa = {
            "E": int(tong_so_o * 0.2),
            "M": int(tong_so_o * 0.4),
            "H": int(tong_so_o * 0.6)
        }[level]

        for _ in range(tong_so_de):
            bang_giai = sinh_bang_sudoku_day_du(size)
            bang_de = xoa_o_ngau_nhien(bang_giai, so_o_xoa)
            dataset[level].append({
                "question": bang_de,
                "solution": bang_giai
            })
    #os.makedirs(...): Tạo toàn bộ đường dẫn thư mục nếu chưa tồn tại.
    #os.path.dirname(output_path): Lấy ra thư mục cha của file output_path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f)

    print(f"Đã lưu dữ liệu Sudoku vào: {output_path}")


def tao_sudoku_theo_cap_do(size, level):
    """Lấy ngẫu nhiên 1 đề + lời giải từ file JSON."""
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

# ======= Chạy =======
if __name__ == "__main__":
    sinh_va_luu_de(size=4)
    sinh_va_luu_de(size=9)
    sinh_va_luu_de(size=16)
    sinh_va_luu_de(size=25)