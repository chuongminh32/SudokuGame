import pygame, sys, os, time, random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.utils_ai_screen import * 
from src.algorithm.generate_sudoku import *
from src.algorithm.backtracking import *


class Ai_Screen:
    def __init__(self):
        self.screen = init_pygame()
        pygame.display.set_caption("Sudoku - Chơi Game")
        self.font = pygame.font.SysFont("verdana", 25)
        self.font_text = pygame.font.SysFont("verdana", 20)  
        self.bang_goc = layBangSuDoKuTheoCapDo()
        self.bang = [row[:] for row in self.bang_goc]
        self.bang_giai = giai_sudoku_backtracking(self.bang_goc)

        #------ chon cap do -------
        # khung bao quanh bang cap do
        self.rect_bang_cap_do = None
        # phân cấp độ 
        self.hien_bang_cap_do = False # mặc định không hiện bảng cấp độ 
        self.ten_cap_do = "Dễ"
        self.bang_cap_do = [] # luu ds cac lv 

        #------ chon alg ------
        # khung bao quanh bang alg
        self.rect_bang_alg = None
        # phân cấp độ 
        self.hien_bang_chon_alg = False # mặc định không hiện bảng cấp độ 
        self.ten_alg = "Backtracking"
        self.bang_alg = [] # luu ds cac alg 
        self.chon_val_alg = "B"


        # sự kiện click nút trong bảng 
        self.o_chinh_sua = [(i, j) for i in range(KT_LUOI) for j in range(KT_LUOI) if self.bang_goc[i][j] == 0] # ô có thể chỉnh sửa 
        self.o_sai = []
        self.o_dung = []
        self.o_chon = None

        self.so_loi = 0
        self.dangChayGame = True
        self.ket_thuc = False


    def xuLiSuKien(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.dangChayGame = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.xuLiSuKienClickChuot(e.pos)


    def reset_game(self):
        # Đặt lại bảng chơi về trạng thái ban đầu
        self.bang = [row[:] for row in self.bang_goc]  # Khôi phục lại bảng ban đầu
        self.o_chon = None  # Không có ô nào được chọn
        self.ket_thuc = False  # Đặt lại trạng thái thua game
        self.so_loi = 0  # Đặt lại số lỗi
        self.tg_bat_dau = time.time()  # Khởi tạo lại thời gian bắt đầu
        self.o_sai = []  # Xóa danh sách các ô sai
        self.o_dung = []  # Xóa danh sách các ô đúng

    def xuLiSuKienClickChuot(self, vitri_click):

        x = vitri_click[0]
        y = vitri_click[1]

        hint_btn, reset_btn, ai_btn, back_btn = ve_nut(self.screen)
        nut_dd_cap_do = ve_nut_dd_bang_cap_do(self.screen, self.ten_cap_do)

        nut_dd_alg = ve_nut_dd_bang_alg(self.screen, self.ten_cap_do)


    
        # click nút back -> home
        if (back_btn is not None and back_btn.collidepoint(vitri_click)):
            self.dangChayGame = False
        

        # click ô trong bảng (cho click khi đã ẩn bảng chọn)
        elif (DEM <= x <= DEM + KT_LUOI * KT_O and DEM <= y <= DEM + KT_LUOI * KT_O  and not self.hien_bang_cap_do and not self.hien_bang_chon_alg):
            cot = (x - DEM) // KT_O
            dong = (y - DEM) // KT_O
            self.o_chon = (dong, cot) # chọn ô
            
        # click nút cấp độ 
        elif nut_dd_cap_do.collidepoint(vitri_click):
            self.hien_bang_cap_do = not self.hien_bang_cap_do # toggle hien bang cap do 

        # click nút alg 
        elif nut_dd_alg.collidepoint(vitri_click):
            self.hien_bang_chon_alg = not self.hien_bang_chon_alg # toggle hien bang cap do 
        
        # click nút ai giải 
        elif ai_btn.collidepoint(vitri_click):
            self.bang = [row[:] for row in self.bang_giai]  # Hiển thị lời giải bang hien tai 
            self.an_bang_da_thang = False

        # click nút reset
        elif reset_btn is not None and reset_btn.collidepoint(vitri_click):
            self.reset_game()

        # Nếu click ra ngoài bảng cấp độ thì ẩn bảng cấp độ
        elif self.hien_bang_cap_do and not self.rect_bang_cap_do.collidepoint(vitri_click):
            self.hien_bang_cap_do = False
        
        # Nếu click ra ngoài bảng chọn alg thì ẩn đi
        elif self.hien_bang_chon_alg and not self.rect_bang_alg.collidepoint(vitri_click):
            self.hien_bang_chon_alg = False

        
        # Xử lí sự kiện click từng cấp độ trong bảng 
        elif self.hien_bang_cap_do == True:
            for cap_do in self.bang_cap_do:
                if cap_do["rect"].collidepoint(vitri_click):
                    self.chon_che_do = cap_do["value"] # cập nhất giá trị cấp độ đã chọn 
                    self.ten_cap_do = cap_do["text"] # hiển thị lên giao diện 
                    self.bang_cap_do = layBangSuDoKuTheoCapDo(self.chon_che_do)
                    self.bang_goc = self.bang_cap_do
                    self.bang = [row[:] for row in self.bang_goc]
                    # cập nhật lại từng ô trong bảng giải 
                    self.bang_giai = giai_sudoku_backtracking(self.bang)
                    self.o_chinh_sua = [(i,j) for i in range(KT_LUOI) for j in range (KT_LUOI) if self.bang_goc[i][j] == 0]
                    self.hien_bang_cap_do = False
                    break
        # Xử lí sự kiện click chọn alg
        elif self.hien_bang_chon_alg == True:
            for alg in self.bang_alg:
                if alg["rect"].collidepoint(vitri_click):
                    self.chon_val_alg = alg["value"] # cập nhất giá trị cấp độ đã chọn 
                    self.ten_alg = alg["text"] # hiển thị lên giao diện 
                    # cập nhật lại từng ô trong bảng giải 
                    self.hien_bang_chon_alg = False
                    break
        
    def veCauTrucBang(self):
        ve_luoi(self.screen)
        ve_so(self.screen, self.bang, self.bang_goc, self.font, self.bang_giai)

    def ve_lai_cac_o_sai(self):
        for r, c in self.o_sai:
            pygame.draw.rect(self.screen,  (250, 180, 180) , pygame.Rect(DEM + c*KT_O, DEM + r*KT_O, KT_O, KT_O))
        self.veCauTrucBang()
    
    def ve_lai_cac_o_dung(self):
        for r, c in self.o_dung:
            pygame.draw.rect(self.screen, ((180, 230, 200)), pygame.Rect(DEM + c*KT_O, DEM + r*KT_O, KT_O, KT_O))
        self.veCauTrucBang()

 
   
    def run(self):
        while self.dangChayGame:
            self.screen.fill(TRANG)

           
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
            ve_nut_dd_bang_cap_do(self.screen, self.ten_cap_do)
            ve_nut_dd_bang_alg(self.screen, self.ten_alg)

            # Xử lý sự kiện
            self.xuLiSuKien()

            # Vẽ các ô nếu sai/đúng 
            self.ve_lai_cac_o_dung()
            self.ve_lai_cac_o_sai()

            # vẽ bảng chọn level 
            if self.hien_bang_cap_do:
                self.bang_cap_do, self.rect_bang_cap_do = ve_bang_chia_cap_do(self.screen)

            # vẽ bảng chọn alg 
            if self.hien_bang_chon_alg:
                self.bang_alg, self.rect_bang_alg = ve_bang_chon_alg(self.screen)

            pygame.display.update()

    pygame.quit()



def KhoiDongManHinhAI():
    sdk = Ai_Screen()
    sdk.run()

if __name__ == "__main__":
    KhoiDongManHinhAI()
