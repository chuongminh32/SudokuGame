import pygame, sys, os, time, random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.gui_common import * 

class SudokuGame:
    def __init__(self):
        self.screen = init_pygame()
        pygame.display.set_caption("Sudoku - Chơi Game")
        self.font = pygame.font.SysFont("verdana", 25)  
        self.board_original = layBangSuDoKuTheoCapDo()
        self.board = [row[:] for row in self.board_original]
        self.board_solution = [row[:] for row in self.board_original]
        solve_sudoku(self.board_solution)
        
        # phân câp độ 
        self.hien_bang_cap_do = False # mặc định không hiện bảng cấp độ 
        self.ten_cap_do = "Dễ"
        
        self.running = True
        self.hints_left = 5
    def get_hint(self):
        empty_cells = [(i, j) for i in range(KT_LUOI) for j in range(KT_LUOI) 
                      if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            return i, j, self.board_solution[i][j]
        return None

    def reset_game(self):
        self.board = [row[:] for row in self.board_original]
        self.selected_cell = None
        self.hints_left = 3
        self.game_over = False
        self.errors = 0
        self.start_time = time.time()
        self.wrong_cells = []
        self.correct_cells = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.selected_cell and not self.game_over:
                self.handle_key_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        hint_btn, reset_btn, ai_btn, back_btn = ve_nut(self.screen)
        nut_cap_do = ve_nut_phan_chia_cap_do(self.screen)
        
        if hint_btn.collidepoint(pos) and self.hints_left > 0:
            hint = self.get_hint()
            if hint:
                i, j, value = hint
                self.board[i][j] = value
                self.hints_left -= 1
        elif reset_btn.collidepoint(pos):
            self.reset_game()
        elif ai_btn.collidepoint(pos) and solve_sudoku(self.board):
            self.game_over = True
        elif back_btn.collidepoint(pos):
            from src.gui import home_screen
            home_screen.runHome()
        
        # click nút cấp độ 
        elif nut_cap_do.collidepoint(pos):
            hien_bang_cap_do = not hien_bang_cap_do # toggle hien bang cap do 

    def run(self):
        while self.running:

            self.screen.fill(TRANG)
            ve_luoi(self.screen)
            ve_so(self.screen, self.board, self.board_original, self.font)
            ve_nut(self.screen)

            # phân cấp độ 
            ve_bang_chia_cap_do(self.screen)
            ve_nut_phan_chia_cap_do(self.screen,self.ten_cap_do)

            # xử lí sự kiện click nút 
            self.handle_events()

            pygame.display.update()

        pygame.quit()

def khoiDongManHinhChoiGame():
    sdk = SudokuGame()
    sdk.run()

if __name__ == "__main__":
    khoiDongManHinhChoiGame()