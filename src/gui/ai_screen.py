import pygame, sys, os, time, random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.utils_ai_screen import * 

class SudokuGame:
    def __init__(self):
        self.screen = init_pygame()
        pygame.display.set_caption("Sudoku - Chơi Game")
        self.font = pygame.font.SysFont("verdana", 25)
        self.font_text = pygame.font.SysFont("verdana", 20)  
        self.bang_goc = layBangSuDoKuTheoCapDo()
        self.bang = [row[:] for row in self.bang_goc]
        self.bang_giai = [row[:] for row in self.bang_goc]
        solve_sudoku(self.bang_giai)
        
        # phân thuật toán 
        self.hien_bang_cap_do = False # mặc định không hiện bảng cấp độ 
        self.hien_bang_alg = False
        self.ten_cap_do = "Dễ"
        self.ten_alg = "HillClimbing"
        self.bang_cap_do = [] # luu ds cac bang 
        self.bang_alg = [] # luu ds cac bang alg 

        # sự kiện click nút trong bảng 
        self.o_chinh_sua = [(i, j) for i in range(KT_LUOI) for j in range(KT_LUOI) if self.bang_goc[i][j] == 0] # ô có thể chỉnh sửa 
        self.o_sai = []
        self.o_dung = []
        self.o_chon = None

        self.running = True
        self.ket_thuc = False 
        # nút pause 
        self.iconPause_Play = None
        self.isPause = False 
        self.tg_pause = 0 # thời điểm dừng 
        self.tg_da_troi = 0
        self.tg_bat_dau = time.time()

        # nút phân chia alg, cấp độ 
        self.nut_alg, self.nut_cap_do = None, None 
    
    def reset_game(self):
        # Đặt lại bảng chơi về trạng thái ban đầu
        self.bang = [row[:] for row in self.bang_goc]  # Khôi phục lại bảng ban đầu
        self.o_chon = None  # Không có ô nào được chọn
        self.so_goi_y = 3  # Khôi phục lại số gợi ý
        self.ket_thuc = False  # Đặt lại trạng thái thua game
        self.so_loi = 0  # Đặt lại số lỗi
        self.tg_bat_dau = time.time()  # Khởi tạo lại thời gian bắt đầu
        self.o_sai = []  # Xóa danh sách các ô sai
        self.o_dung = []  # Xóa danh sách các ô đúng
        self.isPause = False  # Khôi phục trạng thái chơi không pause2

        self.ket_thuc = False
        self.thoat_btn, self.choilai_btn = None, None

      

    def xuLiSuKien(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYDOWN  and not self.ket_thuc:
                self.xuLiSuKienNhanPhim(e)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.xuLiSuKienClickChuot(e.pos)

    def xuLiSuKienClickChuot(self, vitri_click):

        x = vitri_click[0]
        y = vitri_click[1]

        hint_btn, reset_btn, ai_btn, back_btn = ve_nut(self.screen)


        # click nút gợi ý 
        if hint_btn.collidepoint(vitri_click) and self.so_goi_y > 0:
            hint = self.layGoiY()
            if hint:
                i, j, value = hint
                self.bang[i][j] = value
                self.so_goi_y -= 1
        # click nút reset 
        elif reset_btn.collidepoint(vitri_click):
            self.reset_game()
        
        # click nút ai giải 
        elif ai_btn.collidepoint(vitri_click) and solve_sudoku(self.bang):
            self.ket_thuc = True
        
        # click nút back : click back hoạc click nút thoát nếu trò chơi kết thúc (win/lose)
        elif back_btn.collidepoint(vitri_click) or (self.ket_thuc == True and self.thoat_btn.collidepoint(vitri_click)):
            from src.gui import home_screen
            home_screen.runHome()
        
        # click nút pause 
        # elif self.iconPause_Play.collidepoint(vitri_click):
        
        #     self.isPause = not self.isPause
        #     if self.isPause:
        #         self.tg_pause = time.time()  # Lưu thời điểm pause
        #     else:
        #         self.tg_bat_dau += time.time() - self.tg_pause  # Cập nhật lại thời gian bắt đầu

        # click ô trong bảng 
        elif DEM <= x <= DEM + KT_LUOI * KT_O and DEM <= y <= DEM + KT_LUOI * KT_O  and not self.hien_bang_cap_do and not self.ket_thuc:
            cot = (x - DEM) // KT_O
            dong = (y - DEM) // KT_O
            self.o_chon = (dong, cot) # chọn ô
            
        # click nút cấp độ 
        elif self.nut_cap_do.collidepoint(vitri_click):
            self.hien_bang_cap_do = not self.hien_bang_cap_do # toggle hien bang cap do 
        
        # click nút chọn thuật toán 
        elif self.nut_alg.collidepoint(vitri_click):
            self.hien_bang_alg = not self.hien_bang_alg

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
        elif self.hien_bang_alg == True:
            for alg in self.bang_alg:
                if alg["rect"].collidepoint(vitri_click):
                    self.chon_che_do = alg["value"] # cập nhất giá trị cấp độ đã chọn 
                    self.ten_alg = alg["text"] # hiển thị lên giao diện 
                    print(alg["text"])
                    self.hien_bang_alg = False
                    break

        # click chơi lại khi end game 
        elif self.ket_thuc == True and self.choilai_btn.collidepoint(vitri_click):
            self.reset_game()

       
    def veCauTrucBang(self):
        ve_luoi(self.screen)
        if self.isPause == False:
            ve_so(self.screen, self.bang, self.bang_goc, self.font)

    def ve_lai_cac_o_sai(self):
        for r, c in self.o_sai:
            pygame.draw.rect(self.screen, (234, 100, 100), pygame.Rect(DEM + c*KT_O, DEM + r*KT_O, KT_O, KT_O))
        self.veCauTrucBang()
    
    def ve_lai_cac_o_dung(self):
        for r, c in self.o_dung:
            pygame.draw.rect(self.screen, (159, 220, 133), pygame.Rect(DEM + c*KT_O, DEM + r*KT_O, KT_O, KT_O))
        self.veCauTrucBang()

    # hàm kiểm tra đã thắng hay chưa 
    def isWin(self):
        cnt = 0
        for i in range(KT_LUOI):
            for j in range(KT_LUOI):
                if self.bang[i][j] == 0:
                    cnt += 1
        return (len(self.o_dung) == cnt)

    def run(self):
        while self.running:
            self.screen.fill(TRANG)
            
            # hiển thị thời gian chơi 
            # if self.tg_bat_dau is None:
            #     self.tg_bat_dau = time.time()
            # if not self.ket_thuc and not self.isPause and self.tg_bat_dau is not None:
            #     self.tg_da_troi = time.time() - self.tg_bat_dau  # cập nhật thời gian đã trôi 
            # hienThiTGChoi(self.screen, self.tg_da_troi, self.font)
            
            # vẽ icon pause/play 
            # self.iconPause_Play = ve_icon_pause(self.screen, self.isPause)

            # Vẽ nền, lưới và số
            self.veCauTrucBang()

            # Highlight nếu có ô chọn
            if self.o_chon and not self.ket_thuc:
                dong, cot = self.o_chon
                ve_highlight_cho_o(self.screen, dong, cot, self.bang)
                 # Vẽ nền, lưới và số
                self.veCauTrucBang()

            # Vẽ các nút
            ve_nut(self.screen)
            self.nut_cap_do = ve_nut_phan_chia_cap_do(self.screen, self.ten_cap_do)
            self.nut_alg  = ve_nut_lua_chon_alg(self.screen, self.ten_alg)

            
            # Vẽ các ô nếu sai/đúng 
            self.ve_lai_cac_o_dung()
            self.ve_lai_cac_o_sai()
            
            if self.isWin() == True:
                self.isPause = True
                self.choilai_btn, self.thoat_btn = hien_thi_bang_thang(self.screen, RONG, CAO, self.tg_da_troi)
                self.ket_thuc = True

            # Vẽ bảng cấp độ SAU CÙNG
            if self.hien_bang_cap_do:
                self.bang_cap_do = ve_bang_chia_cap_do(self.screen)


            # Vẽ bảng lựa chọn alg 
            if self.hien_bang_alg:
                self.bang_alg = ve_bang_chon_alg(self.screen)
            
            # Xử lý sự kiện
            self.xuLiSuKien()


            pygame.display.update()

    pygame.quit()


def KhoiDongManHinhAI():
    ai = SudokuGame()
    ai.run()

if __name__ == "__main__":
    KhoiDongManHinhAI()
