import os, time, math, random
import numpy as np

# Hàm cốt lõi thực hiện giải Sudoku bằng Simulated Annealing
def simulated_annealing_core(bang, size, callback=None, delay=0.0, max_steps=10000, max_time=1300.0):
    n = int(size ** 0.5)  # Kích thước khối n x n (ví dụ: 3x3 cho Sudoku 9x9)
    sigma = 100           # Nhiệt độ khởi tạo

    # Tạo danh sách các khối n x n trong bảng Sudoku
    def tao_khoi_nxn():
        blocks = []
        for bi in range(n):
            for bj in range(n):
                block = [(i, j) for i in range(bi * n, (bi + 1) * n)
                                  for j in range(bj * n, (bj + 1) * n)]
                blocks.append(block)
        return blocks

    # Đánh dấu các ô cố định (đã cho sẵn từ đầu) bằng ma trận nhị phân
    def danh_dau_o_co_dinh(sudoku):
        return (sudoku != 0).astype(int)

    # Điền ngẫu nhiên các giá trị còn thiếu trong từng khối sao cho không trùng trong khối đó
    def dien_ngau_nhien_vao_khoi(sudoku, khoi):
        for block in khoi:
            cac_gia_tri = set(range(1, size + 1))  # Tập các số cần điền
            da_co = set()
            o_can_dien = []

            # Phân biệt ô cố định và ô cần điền
            for i, j in block:
                if fixed[i, j]:
                    da_co.add(sudoku[i, j])
                else:
                    sudoku[i, j] = 0  # Reset giá trị
                    o_can_dien.append((i, j))

            gia_tri_con_lai = list(cac_gia_tri - da_co)
            random.shuffle(gia_tri_con_lai)

            # Điền giá trị ngẫu nhiên vào ô cần điền
            for (i, j), val in zip(o_can_dien, gia_tri_con_lai):
                sudoku[i, j] = val
        return sudoku

    # Tính tổng lỗi: số lượng phần tử trùng lặp trong các hàng và cột
    def tinh_loi(sudoku):
        loi = 0
        for i in range(size):
            loi += (size - len(np.unique(sudoku[i, :])))  # lỗi hàng
            loi += (size - len(np.unique(sudoku[:, i])))  # lỗi cột
        return loi

    # Xác định các ô gây ra conflict (trùng lặp trong hàng/cột)
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

    # Hoán vị hai ô không cố định trong cùng một khối
    def hoan_vi_trong_khoi(sudoku):
        block = random.choice(khoi)
        o_swap = [box for box in block if fixed[box[0], box[1]] == 0]
        if len(o_swap) < 2:
            return sudoku.copy(), None
        (i1, j1), (i2, j2) = random.sample(o_swap, 2)
        moi = sudoku.copy()
        moi[i1, j1], moi[i2, j2] = moi[i2, j2], moi[i1, j1]
        return moi, ((i1, j1), (i2, j2))

    # Chuẩn bị dữ liệu và khởi tạo giải thuật
    sudoku = np.array(bang)
    fixed = danh_dau_o_co_dinh(sudoku)
    khoi = tao_khoi_nxn()
    sudoku = dien_ngau_nhien_vao_khoi(sudoku, khoi)

    score = tinh_loi(sudoku)  # Tính lỗi ban đầu
    buoc = 0
    start_time = time.perf_counter()

    # Vòng lặp chính của giải thuật Simulated Annealing
    while score > 0 and buoc < max_steps and (time.perf_counter() - start_time) < max_time:
        de_xuat, vi_tri = hoan_vi_trong_khoi(sudoku)
        if vi_tri is None:
            continue

        i1, j1 = vi_tri[0]
        i2, j2 = vi_tri[1]
        v1 = de_xuat[i1, j1]
        v2 = de_xuat[i2, j2]

        loi_moi = tinh_loi(de_xuat)
        delta = loi_moi - score

        # Quyết định có chấp nhận bước đi này không
        chap_nhan = delta < 0 or random.random() < math.exp(-delta / sigma)

        if chap_nhan:
            sudoku = de_xuat
            score = loi_moi
            buoc += 1

            # Gọi hàm callback để cập nhật GUI hoặc log (nếu có)
            conflicts = cac_o_conflict(sudoku)
            s_cf = len(conflicts)
            thoi_gian_tong = time.perf_counter() - start_time

            if callback:
                callback(i1, j1, i2, j2, v1, v2, score, s_cf, thoi_gian_tong, sigma, "thu", buoc)

            if delay > 0:
                time.sleep(delay)

        # Giảm nhiệt độ sau mỗi bước
        sigma = max(sigma * 0.99, 0.001)

    # Kết quả trả về
    isSolve = True
    tong_thoi_gian = time.perf_counter() - start_time
    return sudoku.tolist(), buoc, isSolve, tong_thoi_gian

# Hàm giải Sudoku bằng Simulated Annealing kèm GUI (nếu có)
def giai_sudoku_simulated_annealing(bang, size=9, delay=0.0, cap_nhat_gui=None, isSolve=False):
    # Gọi hàm cập nhật GUI nếu được cung cấp
    def gui_callback(i1, j1, i2, j2, v1, v2, score, s_cf, t, sigma, status, buoc):
        if cap_nhat_gui:
            cap_nhat_gui(i1, j1, i2, j2, v1, v2, score, s_cf, t, sigma, status, buoc)

    # Sao chép bảng đầu vào để không ảnh hưởng gốc
    bang_copy = [row[:] for row in bang]
    ket_qua, buoc, isSolve, _ = simulated_annealing_core(bang_copy, size, gui_callback, delay)
    return ket_qua, buoc, isSolve

# Ghi log quá trình giải Sudoku vào file log_SA.txt
def ghi_log_simulated_annealing(bang, size):
    log_path = os.path.join("SudokuGame", "data", "log_SA.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=== Log giải Sudoku bằng Simulated Annealing ===\n")

    # Callback để ghi log mỗi bước
    def log_callback(i1, j1, i2, j2, v1, v2, score, s_cf, t, sigma, status, buoc):
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"Bước {buoc}: Swap ({i1},{j1}) = {v1} <=> ({i2},{j2}) = {v2} | Lỗi: {score:2} | Conflicts: {s_cf} | Tổng: {t:.4f}s | Sigma: {sigma:.4f}\n")

    bang_copy = [row[:] for row in bang]
    _, _, _, duration = simulated_annealing_core(bang_copy, size, log_callback, delay=0.0)
    return duration
