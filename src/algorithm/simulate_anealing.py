# viết như cấu trúc backtracking
# vẽ đồ thị phân tích trong utils_ai_screen.py phần biểu đồ (vẽ theo logic thuật toán: biểu diễn số bước , thời gian ,...)
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

    def Random_3x3Blocks(sudoku, listOfBlocks):
        for block in listOfBlocks:
            for box in block:
                if sudoku[box[0], box[1]] == 0:
                    currentBlock = sudoku[block[0][0]:(block[-1][0]+1), block[0][1]:(block[-1][1]+1)]
                    sudoku[box[0], box[1]] = random.choice([i for i in range(1, 10) if i not in currentBlock])
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

    solutionFound = (score == 0)

    while not solutionFound:
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
            sigma += 2

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