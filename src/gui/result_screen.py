import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.logger import logger

class ResultScreen:
    def __init__(self, screen, solution):
        self.screen = screen
        self.solution = solution
        self.cell_size = 70  # Tăng kích thước ô
        self.grid_pos = (50, 100)
        self.running = True
        self.next_screen = None
        self.font = pygame.font.Font(None, 40)  # Tăng kích thước chữ
        self.small_font = pygame.font.Font(None, 24)

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
                if self.solution[i][j] != 0:
                    text = self.font.render(str(self.solution[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(self.grid_pos[0] + j * self.cell_size + self.cell_size // 2,
                                                    self.grid_pos[1] + i * self.cell_size + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

    def draw_buttons(self):
        # Nút Back to Menu
        menu_btn = pygame.Rect(50, 650, 150, 40)
        pygame.draw.rect(self.screen, (0, 255, 0), menu_btn)
        text = self.font.render("Back to Menu", True, (0, 0, 0))
        self.screen.blit(text, menu_btn.move(10, 10))
        return menu_btn

    def run(self):
        self.screen.fill((255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                menu_btn = self.draw_buttons()
                if menu_btn.collidepoint(x, y):
                    logger.info("Returning to main menu")
                    from src.gui.menu_screen import MenuScreen
                    self.next_screen = MenuScreen(self.screen)
                    self.running = False

        # Vẽ tiêu đề
        title = self.font.render("Solution", True, (0, 128, 0))  # Màu xanh lá cho tiêu đề
        self.screen.blit(title, (250, 50))

        # Hướng dẫn
        instruction = self.small_font.render("Click 'Back to Menu' to play again!", True, (0, 0, 0))
        self.screen.blit(instruction, (150, 80))

        self.draw_grid()
        self.draw_buttons()
        pygame.display.flip()
        return self.running