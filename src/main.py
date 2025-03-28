import pygame, sys, os 
# Thêm đường dẫn gốc vào sys.path để có thể import module từ thư mục cha
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Sudoku_Test.src.gui.main_screen import main_player
from src.gui.tutorial_screen import show_tutorial

def khoiDongManHinhChoiGame():
    """Khởi động game ở chế độ người chơi"""
    main_player()

def khoiDongManHinhHuongDan():
    """ Khởi động hướng dẫn chơi """
    show_tutorial()

def main():
    """
    Entry point cho trò chơi Sudoku
    """
    # Khởi động trực tiếp home screen
    from src.gui.home_screen import HomeScreen
    home_screen = HomeScreen()
    home_screen.run()

if __name__ == "__main__":
    main() 
