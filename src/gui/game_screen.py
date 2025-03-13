import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from src.sudoku import Sudoku
from src.solver import Solver
from src.utils.logger import logger

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.sudoku = Sudoku()
        self.sudoku.generate_puzzle()
        self.board = self.sudoku.get_board()
        self.cell_size = 70
        self.grid_size = 9 * self.cell_size  # Kích thước lưới: 9 ô x 70 pixel = 630 pixel
        
        # Căn giữa lưới theo chiều ngang và dọc
        screen_width, screen_height = self.screen.get_size()
        self.grid_pos = ((screen_width - self.grid_size) // 2, 50)  # Căn giữa theo chiều ngang, cách đỉnh 80px
        
        self.selected = None
        self.running = True
        self.next_screen = None
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 24)
        self.message = ""
        self.message_timer = 0

    def check_valid_move(self, row, col, value):
        """Kiểm tra xem số nhập vào có hợp lệ không (không trùng hàng, cột, vùng 3x3)"""
        # Kiểm tra hàng
        if value in self.board[row]:
            return False
        # Kiểm tra cột
        if value in [self.board[i][col] for i in range(9)]:
            return False
        # Kiểm tra vùng 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == value:
                    return False
        return True

    def draw_grid(self):
        # Vẽ lưới Sudoku
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0),
                           (self.grid_pos[0] + i * self.cell_size, self.grid_pos[1]),
                           (self.grid_pos[0] + i * self.cell_size, self.grid_pos[1] + 9 * self.cell_size),
                           line_width)
            pygame.draw.line(self.screen, (0, 0, 0),
                           (self.grid_pos[0], self.grid_pos[1] + i * self.cell_size),
                           (self.grid_pos[0] + 9 * self.cell_size, self.grid_pos[1] + i * self.cell_size),
                           line_width)

        # Vẽ số
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    color = (0, 0, 0) if (i, j) in self.sudoku.fixed_cells else (0, 128, 255)
                    text = self.font.render(str(self.board[i][j]), True, color)
                    text_rect = text.get_rect(center=(self.grid_pos[0] + j * self.cell_size + self.cell_size // 2,
                                                    self.grid_pos[1] + i * self.cell_size + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

        # Highlight ô được chọn
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0),
                           (self.grid_pos[0] + self.selected[1] * self.cell_size,
                            self.grid_pos[1] + self.selected[0] * self.cell_size,
                            self.cell_size, self.cell_size), 3)

    def draw_buttons(self):
        # Căn giữa các nút
        screen_width, _ = self.screen.get_size()
        button_width = 100
        button_height = 40
        button_spacing = 20  # Khoảng cách giữa các nút
        
        # Tính vị trí để căn giữa hai nút
        total_buttons_width = 2 * button_width + button_spacing
        start_x = (screen_width - total_buttons_width) // 2

        # Nút Solve
        solve_btn = pygame.Rect(start_x, 700, button_width, button_height)
        pygame.draw.rect(self.screen, (0, 255, 0), solve_btn)
        text = self.font.render("Solve", True, (0, 0, 0))
        text_rect = text.get_rect(center=solve_btn.center)
        self.screen.blit(text, text_rect)

        # Nút Reset
        reset_btn = pygame.Rect(start_x + button_width + button_spacing, 700, button_width, button_height)
        pygame.draw.rect(self.screen, (255, 165, 0), reset_btn)
        text = self.font.render("Reset", True, (0, 0, 0))
        text_rect = text.get_rect(center=reset_btn.center)
        self.screen.blit(text, text_rect)

        return solve_btn, reset_btn

    def reset_board(self):
        self.board = self.sudoku.get_board().copy()
        self.selected = None
        self.message = "Board reset!"
        self.message_timer = 60

    def run(self):
        self.screen.fill((255, 255, 255))

        # Căn giữa tiêu đề
        screen_width, _ = self.screen.get_size()
        title = self.font.render("Sudoku Game", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen_width // 2, 30))
        self.screen.blit(title, title_rect)

        # Hiển thị thông báo (nếu có)
        if self.message and self.message_timer > 0:
            msg_text = self.small_font.render(self.message, True, (255, 0, 0))
            msg_rect = msg_text.get_rect(center=(screen_width // 2, 90))
            self.screen.blit(msg_text, msg_rect)
            self.message_timer -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.grid_pos[0] <= x < self.grid_pos[0] + 9 * self.cell_size and \
                   self.grid_pos[1] <= y < self.grid_pos[1] + 9 * self.cell_size:
                    row = (y - self.grid_pos[1]) // self.cell_size
                    col = (x - self.grid_pos[0]) // self.cell_size
                    if self.sudoku.is_editable(row, col):
                        self.selected = (row, col)
                solve_btn, reset_btn = self.draw_buttons()
                if solve_btn.collidepoint(x, y):
                    logger.info("Solving Sudoku")
                    solver = Solver(self.sudoku)
                    solution = solver.solve()
                    from src.gui.result_screen import ResultScreen
                    self.next_screen = ResultScreen(self.screen, solution)
                    logger.info("Transitioning to ResultScreen")
                    self.running = False
                elif reset_btn.collidepoint(x, y):
                    self.reset_board()
                    logger.info("User reset the board")
            elif event.type == pygame.KEYDOWN and self.selected:
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                    row, col = self.selected
                    value = int(event.unicode)
                    if self.check_valid_move(row, col, value):
                        self.board[row][col] = value
                        logger.info(f"User entered {self.board[row][col]} at position ({row}, {col})")
                    else:
                        self.message = "Invalid move! Number already exists."
                        self.message_timer = 60
                elif event.key == pygame.K_BACKSPACE:
                    row, col = self.selected
                    self.board[row][col] = 0
                    logger.info(f"User cleared position ({row}, {col})")

        self.draw_grid()
        self.draw_buttons()
        pygame.display.flip()
        return self.running