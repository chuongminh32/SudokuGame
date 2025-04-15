import pygame, sys, os, time, random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.utils_ai_screen import * 
from src.algorithm.generate_sudoku import *
from src.algorithm.backtracking import *
from src.algorithm.hill_climbing import *


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

        # nút 
        self.nut_ss, self.reset_btn, self.ai_btn, self.back_btn, self.nut_dd_cap_do, self.nut_dd_alg = [None] * 6 

        # -----------thông báo giải xong -------------
        self.hien_thong_bao_ai = False
        self.thoi_gian_giai = 0
        self.thoat_btn = None

        # giao diện mở rộng 
        self.nut_mo_rong = None 
        self.bat_giao_dien_mo_rong = False



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

    def giai_sudoku(self, chon_val_alg, bang_goc, cap_nhat_gui):
        if chon_val_alg == "B":
            giai_sudoku_backtracking_visual(bang_goc, cap_nhat_gui)
        # elif chon_val_alg == "HC":
        #     giai_sudoku_hill_climbing_visual(bang_goc, cap_nhat_gui)
    
              
    def xuLiSuKienClickChuot(self, vitri_click):

        x = vitri_click[0]
        y = vitri_click[1]

        # click nút back -> home
        if (self.back_btn is not None and self.back_btn.collidepoint(vitri_click)):
            self.dangChayGame = False

        # click ô trong bảng (cho click khi đã ẩn bảng chọn)
        elif (DEM <= x <= DEM + KT_LUOI * KT_O and DEM <= y <= DEM + KT_LUOI * KT_O  and not self.hien_bang_cap_do and not self.hien_bang_chon_alg and not self.hien_thong_bao_ai):
            cot = (x - DEM) // KT_O
            dong = (y - DEM) // KT_O
            self.o_chon = (dong, cot) # chọn ô

        # Trong xử lý click nút "So sánh"
        elif self.nut_ss.collidepoint(vitri_click):
            self.so_sanh_mode = True
            from src.gui import compare_screen
            compare_screen.KhoiDongManHinhSS()
    
        # click nút cấp độ 
        elif self.nut_dd_cap_do.collidepoint(vitri_click):
            self.hien_bang_cap_do = not self.hien_bang_cap_do # toggle hien bang cap do 

        # click nút alg 
        elif self.nut_dd_alg.collidepoint(vitri_click):
            self.hien_bang_chon_alg = not self.hien_bang_chon_alg # toggle hien bang cap do 
        
        # click nút ai giải 
        elif self.ai_btn.collidepoint(vitri_click):
            # # Disable nút làm mới và so sánh
            self.reset_btn = None
            self.nut_ss = None
            # Xoá bàn cờ hiện tại để bắt đầu giải từ đầu
            self.bang = [[0 for _ in range(9)] for _ in range(9)]

            # Ghi lại thời gian bắt đầu
            tg_bat_dau = time.time()

            # Hàm cập nhật GUI từng bước giải
            def cap_nhat_gui(row, col, value, trang_thai):
                if trang_thai == "thu":
                    mau = (255, 243, 176)  # Vàng nhạt
                elif trang_thai == "sai":
                    mau = (255, 193, 193)  # Đỏ nhạt
                elif trang_thai == "dung":
                    mau = (195, 247, 202)  # Xanh nhạt
                else:
                    mau = TRANG  # Mặc định

                # Vẽ một ô tại vị trí (row, col) với màu `mau`, viền nhỏ (để nhìn đẹp hơn)
                pygame.draw.rect(self.screen, mau, pygame.Rect(
                    DEM + col * KT_O + 1,             # Toạ độ X của ô cộng thêm 1 pixel để tạo khoảng viền
                    DEM + row * KT_O + 1,             # Toạ độ Y của ô cộng thêm 1 pixel để tạo khoảng viền
                    KT_O - 2,                         # Chiều rộng ô (giảm 2 pixel để giữ viền)
                    KT_O - 2                          # Chiều cao ô (giảm 2 pixel để giữ viền)
                ))

                # Nếu ô có giá trị (khác 0), thì hiển thị số đó lên ô
                if value != 0:
                    text = self.font.render(str(value), True, DEN)  # Tạo đối tượng văn bản với màu đen
                    rect = text.get_rect(center=(
                        DEM + col * KT_O + KT_O // 2,             # Tọa độ X chính giữa ô
                        DEM + row * KT_O + KT_O // 2              # Tọa độ Y chính giữa ô
                    ))
                    self.screen.blit(text, rect)  # Vẽ số lên ô Sudoku tại vị trí căn giữa

                # Cập nhật lại phần màn hình vừa vẽ để hiển thị ngay lập tức
                pygame.display.update()

                # Tạm dừng 10 mili giây để người dùng nhìn thấy bước này (hiệu ứng minh họa quá trình giải)
                pygame.time.delay(10)

            # Gọi thuật toán giải có hiệu ứng
            self.giai_sudoku(self.chon_val_alg, self.bang_goc, cap_nhat_gui)

            # Ghi lại thời gian kết thúc và tính tổng thời gian
            tg_ket_thuc = time.time()
            self.thoi_gian_giai = round(tg_ket_thuc - tg_bat_dau, 2)

            self.hien_thong_bao_ai = True  # Cờ để hiện bảng thông báo

            self.bang = [row[:] for row in self.bang_giai]  # Hiển thị lời giải bang hien tai

        # click nút thoát -> ẩn bảng thông báo 
        elif self.thoat_btn != None:
            if self.thoat_btn.collidepoint(vitri_click):
                self.hien_thong_bao_ai = False
                self.thoat_btn = None

        # click nút reset
        elif self.reset_btn is not None and self.reset_btn.collidepoint(vitri_click):
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
        
       # click nut mo rong 
        if self.nut_mo_rong and self.nut_mo_rong.collidepoint(vitri_click):
            self.bat_giao_dien_mo_rong = not self.bat_giao_dien_mo_rong
            if self.bat_giao_dien_mo_rong:
                self.screen = pygame.display.set_mode((RONG * 2, CAO))
            else:
                self.screen = pygame.display.set_mode((RONG, CAO))


        
    def veCauTrucBang(self):
        ve_luoi(self.screen)
        ve_so(self.screen, self.bang, self.bang_goc, self.font, self.bang_giai)
        self.nut_ss, self.reset_btn, self.ai_btn, self.back_btn = ve_nut(self.screen)
        self.nut_dd_cap_do = ve_nut_dd_bang_cap_do(self.screen, self.ten_cap_do)
        self.nut_dd_alg = ve_nut_dd_bang_alg(self.screen, self.ten_alg)
        self.nut_mo_rong = ve_nut_mo_rong(self.screen, RONG, CAO)

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

            # Xử lý sự kiện
            self.xuLiSuKien()

            # vẽ bảng chọn level 
            if self.hien_bang_cap_do:
                self.bang_cap_do, self.rect_bang_cap_do = ve_bang_chia_cap_do(self.screen)

            # vẽ bảng chọn alg 
            if self.hien_bang_chon_alg:
                self.bang_alg, self.rect_bang_alg = ve_bang_chon_alg(self.screen)

            # Nếu giải xong thì hiện thông báo
            if self.hien_thong_bao_ai:
                self.thoat_btn = ve_thong_bao_giai_xong(self.screen, RONG, CAO, self.thoi_gian_giai, self.ten_alg)

            pygame.display.update()

    pygame.quit()



def KhoiDongManHinhAI():
    sdk = Ai_Screen()
    sdk.run()

if __name__ == "__main__":
    KhoiDongManHinhAI()
