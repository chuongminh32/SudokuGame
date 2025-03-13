import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.logger import logger

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.next_screen = None
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)

    def draw_menu(self):
        # Tiêu đề
        title = self.font.render("Sudoku Solver", True, (0, 0, 0))
        self.screen.blit(title, (150, 100))

        # Hướng dẫn
        instruction = self.small_font.render("Click 'New Game' to start!", True, (0, 0, 0))
        self.screen.blit(instruction, (180, 150))

        # Nút New Game
        new_game_btn = pygame.Rect(200, 300, 200, 50)
        pygame.draw.rect(self.screen, (0, 255, 0), new_game_btn)
        text = self.font.render("New Game", True, (0, 0, 0))
        self.screen.blit(text, new_game_btn.move(20, 10))

        # Nút Quit
        quit_btn = pygame.Rect(200, 400, 200, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), quit_btn)
        text = self.font.render("Quit", True, (0, 0, 0))
        self.screen.blit(text, quit_btn.move(50, 10))

        return new_game_btn, quit_btn

    def run(self):
        self.screen.fill((255, 255, 255))
        
        # Vẽ menu trước để lấy tọa độ nút
        new_game_btn, quit_btn = self.draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if new_game_btn.collidepoint(x, y):
                    logger.info("Starting new game - Creating GameScreen")
                    from src.gui.game_screen import GameScreen
                    self.next_screen = GameScreen(self.screen)
                    logger.info("GameScreen created, transitioning to next screen")
                    # Không đặt self.running = False ở đây, để main.py xử lý
                elif quit_btn.collidepoint(x, y):
                    logger.info("User quit from menu")
                    self.running = False

        pygame.display.flip()
        return self.running