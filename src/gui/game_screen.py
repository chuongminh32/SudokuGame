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
        self.bang_cap_do = [] # luu ds cac bang 
        
        self.running = True
        self.hints_left = 5

    def layGoiY(self):
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

    def xuLiSuKien(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.selected_cell and not self.game_over:
                self.handle_key_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.xuLiSuKienClickChuot(event.pos)

    def xuLiSuKienClickChuot(self, vitri_click):
        hint_btn, reset_btn, ai_btn, back_btn = ve_nut(self.screen)

        nut_cap_do = ve_nut_phan_chia_cap_do(self.screen, self.ten_cap_do)
        
        if hint_btn.collidepoint(vitri_click) and self.hints_left > 0:
            hint = self.layGoiY()
            if hint:
                i, j, value = hint
                self.board[i][j] = value
                self.hints_left -= 1
        elif reset_btn.collidepoint(vitri_click):
            self.reset_game()
        elif ai_btn.collidepoint(vitri_click) and solve_sudoku(self.board):
            self.game_over = True
        elif back_btn.collidepoint(vitri_click):
            from src.gui import home_screen
            home_screen.runHome()
        
        # click nút cấp độ 
        elif nut_cap_do.collidepoint(vitri_click):
            self.hien_bang_cap_do = not self.hien_bang_cap_do # toggle hien bang cap do 

         # Nếu click ra ngoài bảng cấp độ thì ẩn bảng cấp độ
        elif self.hien_bang_cap_do and not pygame.Rect(RONG - 270, 50, 200, 200).collidepoint(vitri_click):
            self.hien_bang_cap_do = False
        
        # Xử lí sự kiện click từng cấp độ trong bảng 
        elif self.hien_bang_cap_do == True:
            for cap_do in self.bang_cap_do:
                if cap_do["rect"].collidepoint(vitri_click):
                    self.chon_che_do = cap_do["value"] # cập nhất giá trị cấp độ đã chọn 
                    self.ten_cap_do = cap_do["text"] # hiển thị lên giao diện 
                    self.bang_goc = layBangSuDoKuTheoCapDo(self.chon_che_do)
                    self.bang = [row[:] for row in self.bang_goc]
                    self.bang_giai = [row[:] for row in self.bang_goc]
                    solve_sudoku(self.bang_giai)
                    # cập nhật lại từng ô trong bảng giải 
                    self.o_chinh_sua = [(i,j) for i in range(KT_LUOI) for j in range (KT_LUOI) if self.bang_goc[i][j] == 0]

                    self.hien_bang_cap_do = False
                    break


    def run(self):
        while self.running:

            self.screen.fill(TRANG)
            ve_luoi(self.screen)
            ve_so(self.screen, self.board, self.board_original, self.font)
            ve_nut(self.screen)

            # phân cấp độ 
            if self.hien_bang_cap_do == True:
                self.bang_cap_do = ve_bang_chia_cap_do(self.screen)

            ve_nut_phan_chia_cap_do(self.screen,self.ten_cap_do)

            # xử lí sự kiện click nút 
            self.xuLiSuKien()

            pygame.display.update()

        pygame.quit()

def khoiDongManHinhChoiGame():
    sdk = SudokuGame()
    sdk.run()

if __name__ == "__main__":
    khoiDongManHinhChoiGame()