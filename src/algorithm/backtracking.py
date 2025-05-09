import os
import math
import time
from src.algorithm.generate_sudoku import *  # Hàm tạo bảng Sudoku
from src.gui.generate__gui.gen_aiScreen import *  # Giao diện hiển thị quá trình giải

def backtracking_core(bang, kich_thuoc, ham_goi_ve=None, tre=0):
    """
    Giải Sudoku sử dụng thuật toán Backtracking kết hợp chiến lược MRV.
    - bang: bảng Sudoku (2D list)
    - kich_thuoc: kích thước bảng (thường là 9)
    - ham_goi_ve: hàm gọi cập nhật GUI/log sau mỗi bước
    - tre: thời gian chờ mỗi bước (để hiển thị animation)
    - CÁC BƯỚC GIẢI:
   1. Tìm ô trống có ít khả năng nhất để thử trước (chiến lược MRV).
   2. Thử điền từng số hợp lệ vào ô đó.
   3. Gọi đệ quy để giải tiếp.
   4. Nếu gặp lỗi (không còn ô nào hợp lệ) → quay lui (backtrack).
   5. Kết thúc khi không còn ô trống → trả về True.
    """
    kich_thuoc_o = math.isqrt(kich_thuoc)  # Kích thước của 1 ô vuông nhỏ (3 với Sudoku 9x9)
    cac_so_hop_le = list(range(1, kich_thuoc + 1))  # Danh sách số hợp lệ [1..9]

    hang = [set() for _ in range(kich_thuoc)]
    cot = [set() for _ in range(kich_thuoc)]
    o_vuong = [[set() for _ in range(kich_thuoc_o)] for _ in range(kich_thuoc_o)]

    """ [[set(), set(), set()],
        [set(), set(), set()],
        [set(), set(), set()]]
        |     |     |     |
        | --- | --- | --- |
        | 0,0 | 0,1 | 0,2 |
        | 1,0 | 1,1 | 1,2 |
        | 2,0 | 2,1 | 2,2 |
    """

    # Khởi tạo các tập hợp từ bảng ban đầu
    for i in range(kich_thuoc):
        for j in range(kich_thuoc):
            gia_tri = bang[i][j]
            if gia_tri:
                hang[i].add(gia_tri)
                cot[j].add(gia_tri)
                o_vuong[i // kich_thuoc_o][j // kich_thuoc_o].add(gia_tri)

    thoi_gian_bat_dau = time.perf_counter()
    so_buoc = 0

    def solve():
        nonlocal so_buoc

        so_lua_chon_nho_nhat = kich_thuoc + 1
        o_tiep_theo = None
        cac_phan_tu_co_the = {} # key: (i, j) ; val = ô

        # ----- chiến lược MRV(Minimum Remaining Value): Tìm ô trống có ít khả năng nhất để thử trước ------
        for i in range(kich_thuoc):
            for j in range(kich_thuoc):
                if bang[i][j] == 0:
                    
                    # thêm các số có thể điền vào ô vào 1 danh sách cac_so_kha_dung
                    cac_so_kha_dung = []
                    for so in cac_so_hop_le:
                        if(so not in hang[i]) and (so not in cot[j]) and (so not in o_vuong[i // kich_thuoc_o][j//kich_thuoc_o]):
                            cac_so_kha_dung.append(so)

                    cac_phan_tu_co_the[(i, j)] = cac_so_kha_dung

                    # không có số nào hợp lệ -> false (BACKTRACK)
                    if len(cac_so_kha_dung) == 0:
                        return False
                    
                    # kt nếu ds là nhỏ nhất -> chọn đi ô đó trước (ít lựa chọn) - MRV 
                    if 0 < len(cac_so_kha_dung) < so_lua_chon_nho_nhat:
                        so_lua_chon_nho_nhat = len(cac_so_kha_dung)
                        o_tiep_theo = (i, j)

        if not o_tiep_theo:
            return True  # Đã điền xong

        # ----- Thử điền từng số hợp lệ vào ô đó --------
        i, j = o_tiep_theo
        for so in cac_phan_tu_co_the[(i, j)]:

            # truyền giá trị và cập nhật các giá trị có sẵn trong hàng(i), cột(j)
            bang[i][j] = so
            hang[i].add(so)
            cot[j].add(so)
            o_vuong[i // kich_thuoc_o][j // kich_thuoc_o].add(so)
            so_buoc += 1

            # nếu có gọi hàm cập nhật giao diện -> cập nhật giá trị để hiển thị lên gui
            # ---- GIAO DIỆN --------
            if ham_goi_ve:
                ham_goi_ve(i, j, so, "thu", so_buoc, time.perf_counter() - thoi_gian_bat_dau)
            if tre > 0:
                time.sleep(tre)
            # ---- GIAO DIỆN --------

            # gọi đệ quy nếu điền hợp lệ để giải tiếp
            if solve():
                if ham_goi_ve:
                    ham_goi_ve(i, j, so, "dung", so_buoc, time.perf_counter() - thoi_gian_bat_dau)
                return True

            # backtracking lại bước hiện tại (reset giá trị ô, xóa ô có sẵn tại hàng(i), cột (j) nếu nước đi tiếp theo không hợp lệ (solve())
            bang[i][j] = 0
            hang[i].remove(so)
            cot[j].remove(so)
            o_vuong[i // kich_thuoc_o][j // kich_thuoc_o].remove(so)
            so_buoc += 1

            # ---- GIAO DIỆN --------
            if ham_goi_ve:
                ham_goi_ve(i, j, so, "sai", so_buoc, time.perf_counter() - thoi_gian_bat_dau)
            if tre > 0:
                time.sleep(tre)
            # ---- GIAO DIỆN --------

        # KHÔNG CÓ LỜI GIẢI HỢP LỆ -> BACKTRACK LÊN NHÁNH TRƯỚC ĐÓ (THỬ GIÁ TRỊ KHÁC HỢP LỆ -> SINH NHỮNG GIÁ TRỊ HỢP LỆ MỚI CHO NHÁNH CON)
        return False 

    return solve(), so_buoc, time.perf_counter() - thoi_gian_bat_dau

# Hàm giải Sudoku cho giao diện (có hỗ trợ GUI cập nhật)
def giai_sudoku_backtracking(bang_dau_vao, kich_thuoc=9, tre=0, cap_nhat_giao_dien=None, da_giai=False):
    def goi_lai_giao_dien(dong, cot, gia_tri, trang_thai, buoc, _):
        if cap_nhat_giao_dien:
            cap_nhat_giao_dien(dong, cot, gia_tri, trang_thai, buoc)

    bang_sao = [hang[:] for hang in bang_dau_vao]
    da_giai, so_buoc, _ = backtracking_core(bang_sao, kich_thuoc, goi_lai_giao_dien, tre)
    return bang_sao, so_buoc, da_giai

# Ghi log lời giải bằng thuật toán Backtracking
def ghi_log_backtracking(bang_dau_vao, kich_thuoc):
    duong_dan_log = os.path.join("SudokuGame", "data", "log_B.txt")
    with open(duong_dan_log, "w", encoding="utf-8") as tep:
        tep.write("")

    def ghi_log(dong, cot, gia_tri, trang_thai, buoc, thoi_gian):
        mo_ta_trang_thai = {
            "thu": "Thử giá trị",
            "dung": "Đúng",
            "sai": "Sai - quay lui"
        }.get(trang_thai, "")
        with open(duong_dan_log, "a", encoding="utf-8") as tep:
            tep.write(f"{buoc}:{thoi_gian:.4f} ({dong},{cot}) <- {gia_tri} --> {mo_ta_trang_thai}\n")

    bang_sao = [hang[:] for hang in bang_dau_vao]
    _, _, tong_thoi_gian = backtracking_core(bang_sao, kich_thuoc, ghi_log)
    return tong_thoi_gian


"""
- Tài liệu tham khảo:
GeeksForGeeks: https://www.geeksforgeeks.org/sudoku-backtracking-7/

Peter Norvig, "Solving Every Sudoku Puzzle", 2006 – Bài viết hướng dẫn chi tiết về Backtracking kết hợp MRV và kỹ thuật loại trừ (constraint propagation).
https://norvig.com/sudoku.html

Wikipedia - Sudoku Solving Algorithms – Tổng quan nhiều thuật toán giải Sudoku, bao gồm Backtracking, MRV, Forward Checking.
https://en.wikipedia.org/wiki/Sudoku_solving_algorithms"""