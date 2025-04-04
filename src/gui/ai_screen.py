import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.gui_common import RONG, CAO  # Đảm bảo đã có RONG, CAO

class AI_Sudoku:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("AI Sudoku Demo")
        self.screen = pygame.display.set_mode((RONG, CAO))
        self.clock = pygame.time.Clock()

        # Khởi tạo font chữ
        self.font = pygame.font.SysFont("verdana", 48)

    def draw_title(self):
        title_surface = self.font.render("AI Sudoku Solver", True, (0, 0, 128))
        title_rect = title_surface.get_rect(center=(RONG // 2, 60))
        self.screen.blit(title_surface, title_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))  # Nền trắng

            self.draw_title()  # Gọi hàm vẽ tiêu đề

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

def KhoiDongManHinhAI():
    game = AI_Sudoku()
    game.run()

if __name__ == "__main__":
    KhoiDongManHinhAI()