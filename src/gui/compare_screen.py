class Compare_Screen(Ai_Screen):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((RONG * 2, CAO))
        pygame.display.set_caption("So sánh thuật toán Sudoku")

        # --------- cấp độ dùng chung cho cả 2 bảng --------
        self.ten_cap_do = "Dễ"
        self.hien_bang_cap_do = False
        self.rect_bang_cap_do = None
        self.bang_cap_do = []
        
        # --------- thuật toán riêng biệt cho từng bảng --------
        self.ten_alg_1 = "Backtracking"
        self.ten_alg_2 = "Backtracking"
        self.chon_val_alg_1 = "B"
        self.chon_val_alg_2 = "B"
        self.hien_bang_chon_alg_1 = False
        self.hien_bang_chon_alg_2 = False
        self.rect_bang_alg_1 = None
        self.rect_bang_alg_2 = None
        self.bang_alg_1 = []
        self.bang_alg_2 = []

        # nút Run để bắt đầu so sánh
        self.run_btn = None

        # Khởi tạo 2 bảng sudoku
        self.bang_goc_1 = layBangSuDoKuTheoCapDo()
        self.bang_goc_2 = [row[:] for row in self.bang_goc_1]
        self.bang_1 = [row[:] for row in self.bang_goc_1]
        self.bang_2 = [row[:] for row in self.bang_goc_2]

    def veCauTrucBang(self):
        # bảng bên trái
        ve_luoi(self.screen, offset_x=0)
        ve_so(self.screen, self.bang_1, self.bang_goc_1, self.font, self.bang_giai, offset_x=0)
        self.nut_dd_cap_do = ve_nut_dd_bang_cap_do(self.screen, self.ten_cap_do, offset_x=20)
        self.nut_dd_alg_1 = ve_nut_dd_bang_alg(self.screen, self.ten_alg_1, offset_x=20)
        
        # bảng bên phải
        ve_luoi(self.screen, offset_x=RONG)
        ve_so(self.screen, self.bang_2, self.bang_goc_2, self.font, self.bang_giai, offset_x=RONG)
        self.nut_dd_alg_2 = ve_nut_dd_bang_alg(self.screen, self.ten_alg_2, offset_x=RONG + 20)

        # nút Run
        self.run_btn = ve_nut_run(self.screen, vi_tri=(RONG - 60, CAO - 60))

    def xuLiSuKienClickChuot(self, vitri_click):
        x, y = vitri_click

        if self.run_btn and self.run_btn.collidepoint(vitri_click):
            print("Bắt đầu so sánh hai thuật toán...")  # Xử lý chạy 2 thuật toán ở đây

        elif self.nut_dd_cap_do.collidepoint(vitri_click):
            self.hien_bang_cap_do = not self.hien_bang_cap_do

        elif self.nut_dd_alg_1.collidepoint(vitri_click):
            self.hien_bang_chon_alg_1 = not self.hien_bang_chon_alg_1

        elif self.nut_dd_alg_2.collidepoint(vitri_click):
            self.hien_bang_chon_alg_2 = not self.hien_bang_chon_alg_2

        # Xử lý các bảng chọn như bình thường...

    def run(self):
        while self.dangChayGame:
            self.screen.fill(TRANG)

            self.veCauTrucBang()
            self.xuLiSuKien()

            # vẽ các bảng chọn nếu đang bật
            if self.hien_bang_cap_do:
                self.bang_cap_do, self.rect_bang_cap_do = ve_bang_chia_cap_do(self.screen, offset_x=RONG//2 - 100)
            if self.hien_bang_chon_alg_1:
                self.bang_alg_1, self.rect_bang_alg_1 = ve_bang_chon_alg(self.screen, offset_x=20)
            if self.hien_bang_chon_alg_2:
                self.bang_alg_2, self.rect_bang_alg_2 = ve_bang_chon_alg(self.screen, offset_x=RONG + 20)

            pygame.display.update()

        pygame.quit()


def KhoiDongManHinhSS():
    ss = Compare_Screen()
    ss.run()
