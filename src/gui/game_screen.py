import pygame, sys, os, time, random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.utils_game_screen import * 

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
        
        # phân cấp độ 
        self.hien_bang_cap_do = False # mặc định không hiện bảng cấp độ 
        self.ten_cap_do = "Dễ"
        self.bang_cap_do = [] # luu ds cac bang 

        # sự kiện click nút trong bảng 
        self.o_chinh_sua = [(i, j) for i in range(KT_LUOI) for j in range(KT_LUOI) if self.bang_goc[i][j] == 0] # ô có thể chỉnh sửa 
        self.o_sai = []
        self.o_dung = []
        self.o_chon = None

        # nút gợi ý 
        self.so_goi_y = 3
        self.iconGoiY = None 

        # nút pause 
        self.iconPause_Play = None
        self.isPause = False 
        self.tg_pause = 0 # thời điểm dừng 
        self.tg_da_troi = 0
        self.tg_bat_dau = time.time()


        # gõ số lên bảng 
        self.so_loi = 0
        self.ket_thuc = False
        self.running = True

        # thua/thang game 
        self.choilai_btn, self.thoat_btn = None, None
    

    def layGoiY(self):
        empty_cells = [(i, j) for i in range(KT_LUOI) for j in range(KT_LUOI) 
                      if self.bang[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            return i, j, self.bang_giai[i][j]
        return None

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

    def xuLiSuKienNhanPhim(self, vitri_go):
        if self.o_chon != None:
            i, j = self.o_chon
            # Kiểm tra phím nhập số từ 1-9
            if (i, j) in self.o_chinh_sua and (
                (pygame.K_1 <= vitri_go.key <= pygame.K_9) or
                (pygame.K_KP1 <= vitri_go.key <= pygame.K_KP9)
            ):
                if pygame.K_1 <= vitri_go.key <= pygame.K_9:
                    gia_tri = vitri_go.key - pygame.K_0
                    if(buocDiHopLe(self.bang, i, j, gia_tri)):
                        self.bang[i][j] = vitri_go.key - pygame.K_0
                    else : 
                        self.so_loi += 1
                        self.bang[i][j] = vitri_go.key - pygame.K_0
                else:
                    gia_tri = vitri_go.key - pygame.K_0
                    if(viTriHopLe(self.bang, i, j, gia_tri)):
                        self.bang[i][j] = vitri_go.key - pygame.KP_0  # Chuyển số từ numpad
                    else : 
                        self.so_loi += 1
                        self.bang[i][j] = vitri_go.key - pygame.K_0

                self.o_sai = []  # Xóa danh sách cũ
                self.o_dung = [] 
                for x in range(KT_LUOI):
                    for y in range(KT_LUOI):
                        if self.bang[x][y] != 0:
                            # nếu ds ô lỗi != None -> lưu vào ds o_sai 
                            if viTriHopLe(self.bang, x, y, self.bang[x][y]):
                                self.o_sai.append((x, y))
                                # nếu k 23 và các ô là đang sửa -> đúng 
                            elif (x,y) in self.o_chinh_sua:
                                self.o_dung.append((x,y))

        # Xóa số nếu nhấn DELETE hoặc BACKSPACE
        elif vitri_go.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
            self.bang[i][j] = 0
                # Xóa ô khỏi danh sách lỗi nếu xóa số
            o_sai_moi = []
            for r, c in self.o_sai:
                if(r,c) != (i,j):
                    o_sai_moi.append((r,c))
            self.o_sai = o_sai_moi 

    def xuLiSuKienClickChuot(self, vitri_click):

        x = vitri_click[0]
        y = vitri_click[1]

        hint_btn, reset_btn, ai_btn, back_btn = ve_nut(self.screen)

        nut_cap_do = ve_nut_phan_chia_cap_do(self.screen, self.ten_cap_do)

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
        elif self.iconPause_Play.collidepoint(vitri_click):
            """
            tg_bat_dau += tg_hien_tai(time.time()) - tg_pause 
            tg_da_troi = tg_hien_tai - tg_bat_dau -> thoi diem chay tiep theo 

            vd:
            tg_bat_dau = 0
            tg_pause = 10s 
            tg_play = 14s = tg_hien_tai 
            tg_bat_dau += tg_hien_tai - tg_pause = 0 + (14-10) = 4s 
            tg_da_troi = 14 - 4 = 10s (đồng hồ sẽ tiếp tục tính tại thời điểm này) 
            """
            self.isPause = not self.isPause
            if self.isPause:
                self.tg_pause = time.time()  # Lưu thời điểm pause
            else:
                self.tg_bat_dau += time.time() - self.tg_pause  # Cập nhật lại thời gian bắt đầu

        # click ô trong bảng 
        elif DEM <= x <= DEM + KT_LUOI * KT_O and DEM <= y <= DEM + KT_LUOI * KT_O  and not self.hien_bang_cap_do and not self.ket_thuc:
            cot = (x - DEM) // KT_O
            dong = (y - DEM) // KT_O
            self.o_chon = (dong, cot) # chọn ô
            
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
            if self.tg_bat_dau is None:
                self.tg_bat_dau = time.time()
            if not self.ket_thuc and not self.isPause and self.tg_bat_dau is not None:
                self.tg_da_troi = time.time() - self.tg_bat_dau  # cập nhật thời gian đã trôi 
            hienThiTGChoi(self.screen, self.tg_da_troi, self.font)

            # vẽ icon gợi ý 
            self.iconGoiY = ve_icon_goi_y(self.screen, self.font_text, self.so_goi_y, self.so_loi)
            
            # vẽ icon pause/play 
            self.iconPause_Play = ve_icon_pause(self.screen, self.isPause)

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
            ve_nut_phan_chia_cap_do(self.screen, self.ten_cap_do)

            # Xử lý sự kiện
            self.xuLiSuKien()

            # Vẽ các ô nếu sai/đúng 
            self.ve_lai_cac_o_dung()
            self.ve_lai_cac_o_sai()

            # nếu thua game -> hiện bảng lựa chọn sau khi thua 
            if self.so_loi > 5:
                self.so_loi = 0
                self.ket_thuc = True
            if self.ket_thuc == True:
                self.isPause = True
                self.choilai_btn, self.thoat_btn = hien_thi_bang_thua(self.screen, RONG, CAO)
            
            if self.isWin() == True:
                self.isPause = True
                self.choilai_btn, self.thoat_btn = hien_thi_bang_thang(self.screen, RONG, CAO, self.tg_da_troi)
                self.ket_thuc = True

            # Vẽ bảng cấp độ SAU CÙNG
            if self.hien_bang_cap_do:
                self.bang_cap_do = ve_bang_chia_cap_do(self.screen)

            pygame.display.update()

    pygame.quit()


def khoiDongManHinhChoiGame():
    sdk = SudokuGame()
    sdk.run()

if __name__ == "__main__":
    khoiDongManHinhChoiGame()
