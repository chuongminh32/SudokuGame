import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gui.menu_screen import MenuScreen
from src.utils.logger import setup_logger

def main():
    pygame.init()
    logger = setup_logger()
    logger.info("Starting Sudoku Solver application")
    
    # Initialize main screen với kích thước lớn hơn
    screen = pygame.display.set_mode((700, 750))  # Tăng từ (600, 700) lên (700, 750)
    pygame.display.set_caption("Sudoku Solver")
    
    # Start with menu screen
    current_screen = MenuScreen(screen)
    
    # Main game loop
    running = True
    while running:
        try:
            running = current_screen.run()
            if current_screen.next_screen:
                current_screen = current_screen.next_screen
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            running = False
    
    pygame.quit()
    logger.info("Application closed")

if __name__ == "__main__":
    main()