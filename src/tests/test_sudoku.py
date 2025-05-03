import time
import math
from copy import deepcopy

def giai_sudoku_nangcap(bang, size, delay=0):
    KT_box = math.isqrt(size)
    domains = [[set(range(1, size + 1)) if bang[r][c] == 0 else set() for c in range(size)] for r in range(size)]

    def update_domains(row, col, num, remove=True):
        for i in range(size):
            if remove:
                domains[row][i].discard(num)
                domains[i][col].discard(num)
            else:
                if bang[row][i] == 0:
                    domains[row][i].add(num)
                if bang[i][col] == 0:
                    domains[i][col].add(num)

        start_row, start_col = KT_box * (row // KT_box), KT_box * (col // KT_box)
        for i in range(start_row, start_row + KT_box):
            for j in range(start_col, start_col + KT_box):
                if remove:
                    domains[i][j].discard(num)
                else:
                    if bang[i][j] == 0:
                        domains[i][j].add(num)

    def select_unassigned_cell():
        min_len = size + 1
        selected = None
        for r in range(size):
            for c in range(size):
                if bang[r][c] == 0:
                    l = len(domains[r][c])
                    if l < min_len:
                        min_len = l
                        selected = (r, c)
                        if l == 1:
                            return selected
        return selected

    def get_used(row, col):
        used = set()
        for i in range(size):
            used.add(bang[row][i])
            used.add(bang[i][col])
        start_row, start_col = KT_box * (row // KT_box), KT_box * (col // KT_box)
        for i in range(start_row, start_row + KT_box):
            for j in range(start_col, start_col + KT_box):
                used.add(bang[i][j])
        used.discard(0)
        return used

    so_buoc = 0

    def solve():
        nonlocal so_buoc
        pos = select_unassigned_cell()
        if not pos:
            return True
        row, col = pos
        for num in sorted(domains[row][col]):
            if num not in get_used(row, col):
                bang[row][col] = num
                snapshot = deepcopy(domains)
                update_domains(row, col, num, remove=True)
                so_buoc += 1
                print(f"[Bước {so_buoc}] ({row},{col}) <- {num}")

                if solve():
                    return True

                bang[row][col] = 0
                so_buoc += 1
                print(f"[Bước {so_buoc}] ({row},{col}) <- {num} BACKTRACK")
                domains[:] = snapshot
        return False

    for r in range(size):
        for c in range(size):
            if bang[r][c] != 0:
                update_domains(r, c, bang[r][c], remove=True)

    bang_copy = deepcopy(bang)
    solved = solve()
    return bang_copy, so_buoc, solved

#  Sudoku 9x9 dễ để test
bang_sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

#  In bảng ban đầu
print(" Bảng Sudoku ban đầu:")
for row in bang_sudoku:
    print(row)

#  Giải
print("\nBắt đầu giải...")
ketqua, sobuoc, thanhcong = giai_sudoku_nangcap(bang_sudoku, 9)

#  In kết quả
print("\n Bảng kết quả:")
for row in ketqua:
    print(row)

print(f"\n Tổng số bước: {sobuoc}")
print(f"Giải thành công: {'Có' if thanhcong else 'Không'}")





