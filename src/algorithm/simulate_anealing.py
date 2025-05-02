
# viết như cấu trúc backtracking
# vẽ đồ thị phân tích trong utils_ai_screen.py phần biểu đồ (vẽ theo logic thuật toán: biểu diễn số bước , thời gian ,...)

import os
import time
import math
import random
import numpy as np

import statistics

def giai_sudoku_simulatedanealing(bang, size, cap_nhat_gui=None, delay=0.0, isSolve=False):
    KT_box = math.isqrt(size)

    def Tao_3x3Blocks():
        finalListOfBlocks = []
        for r in range(0, 9):
            tmpList = []
            block1 = [i + 3*((r) % 3) for i in range(0, 3)]
            block2 = [i + 3*(r // 3) for i in range(0, 3)]
            for x in block1:
                for y in block2:
                    tmpList.append((x, y))
            finalListOfBlocks.append(tmpList)
        return finalListOfBlocks

    def Sua_Values(fixed_sudoku):
        for i in range(0, 9):
            for j in range(0, 9):
                if fixed_sudoku[i, j] != 0:
                    fixed_sudoku[i, j] = 1
        return fixed_sudoku

    # def Random_3x3Blocks(sudoku, listOfBlocks):
        # for block in listOfBlocks:
            # for box in block:
                # if sudoku[box[0], box[1]] == 0:
                    # currentBlock = sudoku[block[0][0]:(block[-1][0]+1), block[0][1]:(block[-1][1]+1)]
                    # sudoku[box[0], box[1]] = random.choice([i for i in range(1, 10) if i not in currentBlock])
        # return sudoku
    def Random_3x3Blocks(sudoku, listOfBlocks):
      for block in listOfBlocks:
        nums = [sudoku[r, c] for r, c in block if sudoku[r, c] != 0]
        available_nums = [i for i in range(1, 10) if i not in nums]
        random.shuffle(available_nums)
        idx = 0
        for (r, c) in block:
            if sudoku[r, c] == 0:
                sudoku[r, c] = available_nums[idx]
                idx += 1
      return sudoku


    def Tinh_So_trung_ColRow(row, col, sudoku):
        return (9 - len(np.unique(sudoku[row, :]))) + (9 - len(np.unique(sudoku[:, col])))

    def Tinh_So_trung(sudoku):
        errors = 0
        for i in range(9):
            errors += Tinh_So_trung_ColRow(i, i, sudoku)
        return errors

    def TwoRandomBoxesWithinBlock(fixedSudoku, block):
        while True:
            firstBox = random.choice(block)
            secondBox = random.choice([box for box in block if box != firstBox])
            if fixedSudoku[firstBox[0], firstBox[1]] == 0 and fixedSudoku[secondBox[0], secondBox[1]] == 0:
                return (firstBox, secondBox)

    def FlipBoxes(sudoku, boxesToFlip):
        new_sudoku = sudoku.copy()
        (r1, c1), (r2, c2) = boxesToFlip
        new_sudoku[r1, c1], new_sudoku[r2, c2] = new_sudoku[r2, c2], new_sudoku[r1, c1]
        return new_sudoku

    def ProposedState(sudoku, fixedSudoku, listOfBlocks):
        randomBlock = random.choice(listOfBlocks)
        if sum(fixedSudoku[box[0], box[1]] for box in randomBlock) > 6:
            return sudoku, None  # Nếu block quá cố định, bỏ qua
        boxesToFlip = TwoRandomBoxesWithinBlock(fixedSudoku, randomBlock)
        proposedSudoku = FlipBoxes(sudoku, boxesToFlip)
        return proposedSudoku, boxesToFlip

    def CalculateInitialSigma(sudoku, fixedSudoku, listOfBlocks):
        list_deltas = []
        tmp = sudoku.copy()
        for _ in range(10):
            proposal, _ = ProposedState(tmp, fixedSudoku, listOfBlocks)
            if proposal is not None:
                list_deltas.append(Tinh_So_trung(proposal))
        return statistics.pstdev(list_deltas) or 1

    so_buoc = 0
    ds_log = []
    start_time = time.perf_counter()

    sudoku_np = np.array(bang)
    fixedSudoku = sudoku_np.copy()
    Sua_Values(fixedSudoku)
    listOfBlocks = Tao_3x3Blocks()
    sudoku_np = Random_3x3Blocks(sudoku_np, listOfBlocks)
    sigma = CalculateInitialSigma(sudoku_np, fixedSudoku, listOfBlocks)
    score = Tinh_So_trung(sudoku_np)
    decreaseFactor = 0.99
    stuckCount = 0

    max_steps = 100000  # tối đa 100k bước
    max_time = 60  # tối đa 300 giây (5 phút)

    start_time = time.perf_counter()
    so_buoc = 0
    solutionFound = (score == 0)

    while not solutionFound and so_buoc < max_steps and (time.perf_counter() - start_time) < max_time:
        previousScore = score
        for _ in range(ChooseNumberOfItterations(fixedSudoku)):
            proposal, boxes = ProposedState(sudoku_np, fixedSudoku, listOfBlocks)
            if boxes is None:
                continue
            newCost = sum(Tinh_So_trung_ColRow(r, c, proposal) for r, c in boxes)
            currentCost = sum(Tinh_So_trung_ColRow(r, c, sudoku_np) for r, c in boxes)
            costDifference = newCost - currentCost
            rho = math.exp(-costDifference / sigma)

            if random.random() < rho:
                sudoku_np = proposal
                score += costDifference
                so_buoc += 1

                # cập nhật GUI
                if cap_nhat_gui:
                    for (r, c) in boxes:
                        cap_nhat_gui(r, c, sudoku_np[r, c], "thu", so_buoc)
                    current_time = time.perf_counter()
                    ds_log.append((so_buoc, current_time - start_time))
                    time.sleep(delay)

                if score <= 0:
                    solutionFound = True
                    break

        sigma *= decreaseFactor
        if score <= 0:
            solutionFound = True
            break
        if score >= previousScore:
            stuckCount += 1
        else:
            stuckCount = 0
        if stuckCount > 80:
            sigma += 10

    bang_giai = sudoku_np.tolist()
    if solutionFound:
        isSolve = True

    if cap_nhat_gui:
        return bang_giai, so_buoc, ds_log, isSolve
    else:
        return bang_giai, so_buoc, None, isSolve


def ChooseNumberOfItterations(fixed_sudoku):
    count = 0
    for i in range(9):
        for j in range(9):
            if fixed_sudoku[i, j] != 0:
                count += 1
    return count


#TEST-------------------------------------
# bang = [
    # [0, 2, 4, 0, 0, 7, 0, 0, 0],
    # [6, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 3, 6, 8, 0, 4, 1, 5],
    # [4, 3, 1, 0, 0, 5, 0, 0, 0],
    # [5, 0, 0, 0, 0, 0, 0, 3, 2],
    # [7, 9, 0, 0, 0, 0, 0, 6, 0],
    # [2, 0, 9, 7, 1, 0, 8, 0, 0],
    # [0, 4, 0, 0, 9, 3, 0, 0, 0],
    # [3, 1, 0, 0, 0, 4, 7, 5, 0]
# ]
#
# bang_giai, so_buoc, ds_log, isSolve = giai_sudoku_simulated_annealing(bang, 9, cap_nhat_gui=None, delay=0.05)
# print(bang_giai, "\n", "so buoc: ", so_buoc, "\n ds_log:", ds_log, "\n issSolve: ", isSolve)

def giai_sudoku_simulated_annealing(bang, size, cap_nhat_gui=None, delay=0.0, isSolve=False):
    log_path = os.path.join("Sudoku", "data", "log_giai_sudoku.txt")

    n = int(size ** 0.5)  # Kích thước khối (block)

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
            co_dinh = [sudoku[i, j] for i, j in block if sudoku[i, j] != 0]
            chua_dien = [pos for pos in block if sudoku[pos[0], pos[1]] == 0]
            gia_tri_con_lai = list(cac_gia_tri - set(co_dinh))
            random.shuffle(gia_tri_con_lai)
            for (i, j), val in zip(chua_dien, gia_tri_con_lai):
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

    # Khởi tạo sudoku
    sudoku = np.array(bang)
    fixed = danh_dau_o_co_dinh(sudoku)
    khoi = tao_khoi_nxn()
    sudoku = dien_ngau_nhien_vao_khoi(sudoku, khoi)

    sigma = max(sigma * 0.99, 0.001)  # giữ sigma ≥ 0.001

    score = tinh_loi(sudoku)
    buoc = 0
    start_time = time.perf_counter()

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"=== Log giải Sudoku {size}x{size} bằng Simulated Annealing ===\n")

    while score > 0:

        de_xuat, vi_tri = hoan_vi_trong_khoi(sudoku, fixed, khoi)
        if vi_tri is None:
            continue
        i1, j1 = vi_tri[0]
        i2, j2 = vi_tri[1]
        v1 = sudoku[i1, j1]
        v2 = sudoku[i2, j2]

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

