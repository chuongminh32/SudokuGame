import pygame
import numpy as np
from sudoku import Sudoku
from solver import solve_sudoku  # Hàm giải Sudoku

pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 600, 700
WHITE, BLACK, GRAY, BLUE, GREEN, RED = (255, 255, 255), (0, 0, 0), (200, 200, 200), (0, 0, 255), (0, 128, 0), (200, 0, 0)

# Tạo cửa sổ trò chơi
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku AI - Hill Climbing")

# Biến toàn cục
grid = np.zeros((9, 9), dtype=int)  # Sudoku rỗng
solution = None  # Lưu lời giải
fixed_cells = set()  # Lưu các ô có giá trị ban đầu
selected_cell = None  # Vị trí ô đang chọn
font = pygame.font.Font(None, 40)

def draw_grid():
    """Vẽ lưới Sudoku."""
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (60 * i, 0), (60 * i, 540), thickness)
        pygame.draw.line(screen, BLACK, (0, 60 * i), (540, 60 * i), thickness)

def draw_numbers():
    """Vẽ số Sudoku lên màn hình."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                color = BLUE if (r, c) in fixed_cells else BLACK  # Ô gốc màu xanh, ô thêm màu đen
                text = font.render(str(grid[r][c]), True, color)
                screen.blit(text, (c * 60 + 20, r * 60 + 15))

def draw_buttons():
    """Vẽ các nút bấm trên màn hình."""
    pygame.draw.rect(screen, GREEN, (30, 560, 120, 50))  # Nút Dễ
    pygame.draw.rect(screen, GRAY, (160, 560, 120, 50))  # Nút Trung bình
    pygame.draw.rect(screen, RED, (290, 560, 120, 50))  # Nút Khó
    pygame.draw.rect(screen, BLUE, (420, 560, 150, 50))  # Nút Giải
    pygame.draw.rect(screen, BLACK, (420, 620, 150, 50))  # Nút Xóa

    screen.blit(font.render("Easy", True, BLACK), (75, 575))
    screen.blit(font.render("Medium", True, BLACK), (165, 575))
    screen.blit(font.render("Hard", True, WHITE), (335, 575))
    screen.blit(font.render("Solve", True, WHITE), (465, 575))
    screen.blit(font.render("Del", True, WHITE), (465, 635))

def handle_mouse_click(pos):
    """Xử lý sự kiện khi click chuột."""
    global selected_cell

    x, y = pos
    if y < 540:  # Click trong lưới Sudoku
        selected_cell = (y // 60, x // 60)
    elif 30 < x < 150 and 560 < y < 610:  # Click nút Dễ
        generate_sudoku("easy")
    elif 160 < x < 280 and 560 < y < 610:  # Click nút Trung bình
        generate_sudoku("medium")
    elif 290 < x < 410 and 560 < y < 610:  # Click nút Khó
        generate_sudoku("hard")
    elif 420 < x < 570 and 560 < y < 610:  # Click nút Giải
        solve()
    elif 420 < x < 570 and 620 < y < 670:  # Click nút Xóa
        reset_grid()

def handle_key_press(key):
    """Xử lý nhập số từ bàn phím."""
    if selected_cell and pygame.K_1 <= key <= pygame.K_9:
        r, c = selected_cell
        if (r, c) not in fixed_cells:  # Chỉ cho phép nhập vào ô trống
            grid[r][c] = key - pygame.K_0  # Chuyển key thành số

def generate_sudoku(level):
    """Tạo đề Sudoku theo cấp độ."""
    global grid, fixed_cells
    difficulties = {"easy": 30, "medium": 40, "hard": 50}
    sudoku = Sudoku(9).difficulty(difficulties[level])
    grid = np.array(sudoku.board)  # Chuyển thành numpy array để dễ thao tác
    fixed_cells = {(r, c) for r in range(9) for c in range(9) if grid[r][c] != 0}  # Lưu các ô đã có số

def solve():
    """Giải Sudoku bằng AI và hiển thị kết quả."""
    global grid, solution
    solution = solve_sudoku(grid.copy())  # Gọi thuật toán Hill-Climbing
    if solution is not None:
        for r in range(9):
            for c in range(9):
                if (r, c) not in fixed_cells:  # Chỉ cập nhật ô trống
                    grid[r][c] = solution[r][c]

def reset_grid():
    """Xóa bảng Sudoku."""
    global grid, solution, fixed_cells
    grid = np.zeros((9, 9), dtype=int)
    solution = None
    fixed_cells.clear()

def main():
    """Vòng lặp chính của trò chơi."""
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_numbers()
        draw_buttons()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                handle_key_press(event.key)

    pygame.quit()

if __name__ == "__main__":
    main()
