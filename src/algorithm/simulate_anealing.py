# viết như cấu trúc backtracking
# vẽ đồ thị phân tích trong utils_ai_screen.py phần biểu đồ (vẽ theo logic thuật toán: biểu diễn số bước , thời gian ,...)

import os
import time
import math
import random
import numpy as np

import statistics
def giai_sudoku_simulated_annealing(bang, size, cap_nhat_gui=None, delay=0.0, isSolve=False):
    log_path = os.path.join("Sudoku", "data", "log_giai_sudoku.txt")

    n = int(size ** 0.5)  # Kích thước khối (block)
    sigma = 100

    def tao_khoi_nxn():
        blocks = []
        for bi in range(n):
            for bj in range(n):
                block = [(i, j) for i in range(bi * n, (bi + 1) * n)
                                for j in range(bj * n, (bj + 1) * n)]
                blocks.append(block)
        return blocks

    def danh_dau_o_co_dinh(sudoku):
        return (sudoku != 0).astype(int)

    def dien_ngau_nhien_vao_khoi(sudoku, khoi):
        for block in khoi:
            cac_gia_tri = set(range(1, size + 1))

            # Giá trị đã có trong khối do đề bài cho
            da_co = set()
            o_can_dien = []
            for i, j in block:
                if fixed[i, j]:
                    da_co.add(sudoku[i, j])
                else:
                    sudoku[i, j] = 0  # đảm bảo reset các ô không cố định
                    o_can_dien.append((i, j))

            gia_tri_con_lai = list(cac_gia_tri - da_co)

            if len(gia_tri_con_lai) != len(o_can_dien):
                raise ValueError("Khối có các giá trị cố định không hợp lệ (trùng lặp).")

            random.shuffle(gia_tri_con_lai)
            for (i, j), val in zip(o_can_dien, gia_tri_con_lai):
                sudoku[i, j] = val
        return sudoku


    def tinh_loi(sudoku):
        loi = 0
        for i in range(size):
            loi += (size - len(np.unique(sudoku[i, :])))
            loi += (size - len(np.unique(sudoku[:, i])))
        return loi

    def cac_o_conflict(sudoku):
        conflict = set()
        for i in range(size):
            row = sudoku[i, :]
            col = sudoku[:, i]
            for j in range(size):
                if list(row).count(row[j]) > 1:
                    conflict.add((i, j))
                if list(col).count(col[j]) > 1:
                    conflict.add((j, i))
        return list(conflict)

    def hoan_vi_trong_khoi(sudoku, fixed, khoi):
        block = random.choice(khoi)
        o_swap = [box for box in block if fixed[box[0], box[1]] == 0]
        if len(o_swap) < 2:
            return sudoku.copy(), None
        (i1, j1), (i2, j2) = random.sample(o_swap, 2)
        moi = sudoku.copy()
        moi[i1, j1], moi[i2, j2] = moi[i2, j2], moi[i1, j1]
        return moi, ((i1, j1), (i2, j2))

    sudoku = np.array(bang)
    fixed = danh_dau_o_co_dinh(sudoku)
    khoi = tao_khoi_nxn()
    sudoku = dien_ngau_nhien_vao_khoi(sudoku, khoi)

    sigma = max(sigma * 0.99, 0.001)  # giữ sigma ≥ 0.001
    max_steps = 10000
    max_time = 1200

    score = tinh_loi(sudoku)
    buoc = 0
    start_time = time.perf_counter()

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"=== Log giải Sudoku {size}x{size} bằng Simulated Annealing ===\n")

    while score > 0 and buoc < max_steps and (time.perf_counter() - start_time) < max_time:

        de_xuat, vi_tri = hoan_vi_trong_khoi(sudoku, fixed, khoi)
        if vi_tri is None:
            continue
        i1, j1 = vi_tri[0]
        i2, j2 = vi_tri[1]
        v1 = de_xuat[i1, j1]
        v2 = de_xuat[i2, j2]

        loi_moi = tinh_loi(de_xuat)
        delta = loi_moi - score
        chap_nhan = delta < 0 or random.random() < math.exp(-delta / sigma)

        if chap_nhan:
            sudoku = de_xuat
            score = loi_moi
            buoc += 1

            thoi_gian_tong = time.perf_counter() - start_time
            conflicts = cac_o_conflict(sudoku)
            s_cf = len(conflicts)

            log_msg = f"Bước {buoc}: Swap ({i1},{j1}) = {v1} <=> ({i2},{j2}) = {v2} | Lỗi: {score:2} | Conflicts: {s_cf} | Tổng: {thoi_gian_tong:.4f}s | Sigma: {sigma:.4f}\n"
            print(log_msg)
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_msg)

            if cap_nhat_gui:
                cap_nhat_gui(i1, j1, i2, j2, v1, v2, score, s_cf, thoi_gian_tong, sigma, "thu", buoc)
                time.sleep(delay)

        sigma *= 0.99

    isSolve = True
    ket_qua = sudoku.tolist()
    tong_thoi_gian = time.perf_counter() - start_time

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"Hoàn tất sau {buoc} bước. Tổng thời gian: {tong_thoi_gian:.4f} giây.\n")

    return ket_qua, buoc, isSolve, tong_thoi_gian