import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.logger import setup_logger

def main():
    pygame.init()
    logger = setup_logger()
    logger.info("Starting Sudoku Solver application")
    
    # Initialize main screen
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Sudoku Solver")
    
    # Nhập MenuScreen tại đây để phá vỡ circular import
    from src.gui.menu_screen import MenuScreen
    current_screen = MenuScreen(screen)
    
    # Main game loop
    running = True
    while running:
        running = current_screen.run()
        if current_screen.next_screen:
            current_screen = current_screen.next_screen
    
    pygame.quit()
    logger.info("Application closed")

if __name__ == "__main__":
    main()