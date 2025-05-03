import pygame, sys, os
# Thêm đường dẫn gốc vào sys.path để có thể import module từ thư mục cha
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.gui.home_screen import HomeScreen

def main():
    """
    Entry point cho trò chơi Sudoku
    """
    # Khởi động trực tiếp home screen
    home_screen = HomeScreen()
    home_screen.run()

if __name__ == "__main__":
    main()
