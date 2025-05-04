import sys, os, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *
from src.utils.utils_ai_screen import *

import time

# Trả về bảng giải, số bước và log (nếu có)
def giai_sudoku_backtracking(bang, size, cap_nhat_gui=None, delay=0.01, isSolve=False):
    import time
    KT_box = math.isqrt(size)

    def hop_le(bang, row, col, num):
        for i in range(size):
            if bang[row][i] == num or bang[i][col] == num:
                return False
        start_row, start_col = KT_box * (row // KT_box), KT_box * (col // KT_box)
        for i in range(start_row, start_row + KT_box):
            for j in range(start_col, start_col + KT_box):
                if bang[i][j] == num:
                    return False
        return True

    so_buoc = 0
    start_time = time.perf_counter()

    def solve(bang):
        nonlocal so_buoc
        for row in range(size):
            for col in range(size):
                if bang[row][col] == 0:
                    for num in range(1, size + 1):
                        if hop_le(bang, row, col, num):
                            bang[row][col] = num
                            elapsed = time.perf_counter() - start_time
                            so_buoc += 1

                            print(f"[Bước {so_buoc}] [Time: {elapsed:.4f}s] ({row},{col}) <- {num} --> Đúng")
                            
                            dong_log = f"[Bước {so_buoc}] [Time: {elapsed:.4f}s] ({row},{col}) <- {num} --> Đúng"
                            log_file_path = get_relative_path("data", "log_giai_sudoku.txt")
                            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
                            with open(log_file_path, "a", encoding="utf-8") as f:
                                f.write(dong_log + "\n")

                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, num, "dung", so_buoc, elapsed)
                                time.sleep(delay)

                            if solve(bang):
                                return True

                            # Quay lui
                            bang[row][col] = 0
                            so_buoc += 1 
                            elapsed = time.perf_counter() - start_time
                            print(f"[Bước {so_buoc}] ({row},{col}) <- {num} --> Sai ")
                            dong_log = f"[Bước {so_buoc}] [Time: {elapsed:.4f}s] ({row},{col}) <- {num} --> Sai"
                            log_file_path = get_relative_path("data", "log_giai_sudoku.txt")
                            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
                            with open(log_file_path, "a", encoding="utf-8") as f:
                                f.write(dong_log + "\n")
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, 0, "sai", so_buoc, elapsed)
                                time.sleep(delay)
                    return False  
        return True

    bang_copy = [row[:] for row in bang]  # Copy bảng ban đầu để giữ nguyên
    if solve(bang_copy):
        isSolve = True  

    return bang_copy, so_buoc, isSolve
    

def in_bang(bang):
    for row in bang:
        print(" ".join(str(num) if num != 0 else "." for num in row))
    print()

def so_sanh_bang(b1, b2):
    return all(b1[i][j] == b2[i][j] for i in range(len(b1)) for j in range(len(b1[0])))

def main():
    # Xóa log cũ nếu có
    try:
        log_file_path = get_relative_path("data", "log_giai_sudoku.txt")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("")
    except Exception as e:
        print("Không thể xóa log:", e)
    # ==== BƯỚC 1: Tạo một số bài Sudoku mẫu và đáp án ====
    danh_sach_bai = [
        {
            "de_bai": [
                [5, 1, 7, 6, 0, 0, 0, 3, 4],
                [2, 8, 9, 0, 0, 4, 0, 0, 0],
                [3, 4, 6, 2, 0, 5, 0, 9, 0],
                [6, 0, 2, 0, 0, 0, 0, 1, 0],
                [0, 3, 8, 0, 0, 6, 0, 4, 7],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 9, 0, 0, 0, 0, 0, 7, 8],
                [7, 0, 3, 4, 0, 0, 5, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "dap_an": [
                [5, 1, 7, 6, 9, 8, 2, 3, 4],
                [2, 8, 9, 1, 3, 4, 7, 5, 6],
                [3, 4, 6, 2, 7, 5, 8, 9, 1],
                [6, 7, 2, 8, 4, 9, 3, 1, 5],
                [1, 3, 8, 5, 2, 6, 9, 4, 7],
                [9, 5, 4, 7, 1, 3, 6, 8, 2],
                [4, 9, 5, 3, 6, 2, 1, 7, 8],
                [7, 2, 3, 4, 8, 1, 5, 6, 9],
                [8, 6, 1, 9, 5, 7, 4, 2, 3]
            ]
        }
        # Có thể thêm nhiều bài khác tại đây
    ]

    tong_bai = len(danh_sach_bai)
    so_dung = 0

    print("== KIỂM TRA GIẢI SUDOKU BẰNG BACKTRACKING ==\n")

    for i, bai in enumerate(danh_sach_bai, start=1):
        print(f"---> Đang giải bài {i}/{tong_bai}...\nĐề bài:")
        in_bang(bai["de_bai"])

        start = time.perf_counter()
        ket_qua, so_buoc, danh_sach_log, isSolve = giai_sudoku_backtracking(
            bai["de_bai"], size=9, cap_nhat_gui=None, delay=0
        )
        end = time.perf_counter()
        thoi_gian = end - start

        print("→ Bảng kết quả:")
        in_bang(ket_qua)

        dung = so_sanh_bang(ket_qua, bai["dap_an"])
        print(" Kết quả:", "ĐÚNG" if dung else "SAI")
        print(f" Thời gian: {thoi_gian:.4f} giây")
        print(f" Số bước: {so_buoc}\n")

        if danh_sach_log:
            print(" Log giải:")
            for dong in danh_sach_log:
                print(dong)
            print()

        if dung:
            so_dung += 1

    print(f"\n==> Đánh giá: {so_dung}/{tong_bai} bài đúng ({(so_dung / tong_bai) * 100:.1f}%)\n")


if __name__ == "__main__":
    main()
