import pygame, os, sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# Kích thước chung cho màn hình chơi game 
RONG_GAME, CAO_GAME = 700, 750 
DEM_GAME = 30 

# Màu 
TRANG = (255, 255, 255)
DEN = (0, 0, 0)
XANH = (0, 100, 255)
XANH_SANG = (100, 150, 255)
XAM = (200, 200, 200)
XAM_DEN = (150, 150, 150)  # Màu khi kéo thanh cuộn

class Tutorial_Screen():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((RONG_GAME, CAO_GAME))
        pygame.display.set_caption("Hướng Dẫn SUDOKU")

        # font 
        self.font_tieu_de = pygame.font.SysFont('Verdana', 40)
        self.font_tieu_de_noi_dung = pygame.font.SysFont('Verdana', 28)
        self.font_chu_noi_dung = pygame.font.SysFont('Verdana', 20)

        # Nút quay lại 
        self.nut_quay_lai = pygame.Rect(15, 15, 40, 40)
        self.hover_nutquaylai = False 

        # Vị trí cố định cho tiêu đề và nội dung 
        self.tieude_y = 40 
        self.vitri_batdau_noidung_y = 80 

        # Cuộn nội dung 
        self.cuon_y = 0
        self.cuon_max = 0
        self.khung_thanh_cuon = None 
        self.dang_keo = False 

    def tao_noi_dung(self):
            return [
                {"kieu": "tieude", "noidung": "Cách Chơi Sudoku"},
                {"kieu": "noidung", "noidung": "Điền số 1-9 vào lưới 9x9 sao cho mỗi hàng, cột, ô 3x3 không lặp số. Số màu xanh là số có sẵn."},
                
                {"kieu": "tieude", "noidung": "Hướng Dẫn Chơi"},
                {"kieu": "noidung", "noidung": "- Chọn 'Chơi Game' để tự giải."},
                {"kieu": "noidung", "noidung": "- Nhấn ô trống, nhập số 1-9."},
                {"kieu": "noidung", "noidung": "- Xóa số bằng phím Delete."},
                {"kieu": "noidung", "noidung": "- Dùng 'Gợi Ý' nếu cần."},
                {"kieu": "noidung", "noidung": "- Chọn 'Máy Giải' để xem máy giải tự động."},
                
                {"kieu": "tieude", "noidung": "Mẹo Giải Sudoku"},
                {"kieu": "noidung", "noidung": "- Bắt đầu từ ô có nhiều số sẵn."},
                {"kieu": "noidung", "noidung": "- Loại trừ để tìm số đúng."},
                {"kieu": "noidung", "noidung": "- Tìm vị trí số theo từng số (1, 2, 3...)."},
                {"kieu": "noidung", "noidung": "- Chỉ điền khi chắc chắn."},
                
                {"kieu": "tieude", "noidung": "Cách AI Giải Sudoku"},
                {"kieu": "noidung", "noidung": "AI dùng nhiều thuật toán để giải Sudoku. Dưới đây là 4 thuật toán phổ biến:"},
                
                {"kieu": "tieude", "noidung": "1. Quay Lui (Backtracking)"},
                {"kieu": "noidung", "noidung": "- Tìm ô trống, thử số 1-9."},
                {"kieu": "noidung", "noidung": "- Kiểm tra hợp lệ (không lặp số)."},
                {"kieu": "noidung", "noidung": "- Nếu sai, quay lại thử số khác."},
                {"kieu": "noidung", "noidung": "- Lặp lại đến khi xong."},
                
                {"kieu": "tieude", "noidung": "2. Leo Đồi (Hill Climbing)"},
                {"kieu": "noidung", "noidung": "- Bắt đầu với lưới ngẫu nhiên."},
                {"kieu": "noidung", "noidung": "- Đánh giá số lỗi (lặp số)."},
                {"kieu": "noidung", "noidung": "- Thay đổi một ô để giảm lỗi."},
                {"kieu": "noidung", "noidung": "- Lặp lại đến khi không còn lỗi hoặc kẹt."},
                
                {"kieu": "tieude", "noidung": "3. Leo Đồi với Bước Ngang (Sideway Move)"},
                {"kieu": "noidung", "noidung": "- Như Leo Đồi, nhưng cho phép chọn bước ngang."},
                {"kieu": "noidung", "noidung": "- Nếu không giảm lỗi, thử thay đổi khác mà lỗi không tăng."},
                {"kieu": "noidung", "noidung": "- Giúp tránh kẹt ở giải pháp không tối ưu."},
                
                {"kieu": "tieude", "noidung": "4. Ủ Nóng (Simulated Annealing)"},
                {"kieu": "noidung", "noidung": "- Bắt đầu với lưới ngẫu nhiên."},
                {"kieu": "noidung", "noidung": "- Thay đổi ngẫu nhiên, chấp nhận cả bước xấu (tăng lỗi) lúc đầu."},
                {"kieu": "noidung", "noidung": "- Dần dần chỉ chọn bước tốt khi 'nguội đi'."},
                {"kieu": "noidung", "noidung": "- Tìm giải pháp tối ưu qua nhiều lần thử."}
            ]
    
    def ve_noidung(self):
        
        self.screen.fill(TRANG) 

        # Tiêu đề 
        tieude = self.font_tieu_de.render("Hướng Dẫn", True, XANH)

        # Hàm vẽ tiêu đề lên giao diện chính 
        self.screen.blit(tieude, tieude.get_rect(center = (RONG_GAME//2, self.tieude_y)))

        # Tính toán vị trí nội dung 
        noidung = self.tao_noi_dung()
        vitri_y = self.vitri_batdau_noidung_y - self.cuon_y

        # Giới hạn vị trí cuộn để không vượt qua vitri_batdau_noidung_y khi cuộn lên 
        if self.cuon_y < 0:
            self.cuon_y = 0
            vitri_y = self.vitri_batdau_noidung_y

        # Vẽ nội dung 
        for nd in noidung:
            if nd["kieu"] == "tieude":
                vitri_y += 20 
                # tiêu đề nội dung 
                chu_tieu_de = self.font_tieu_de_noi_dung.render(nd["noidung"], True, DEN)
                # kiểm tra vị trí nếu nằm trong vùng hiển thị nd 
                if vitri_y >= self.vitri_batdau_noidung_y - 30 and vitri_y < CAO_GAME - DEM_GAME:
                    self.screen.blit(chu_tieu_de, (DEM_GAME, vitri_y)) # vẽ chữ lên màn hình nd(x,y)
                vitri_y += 40
            else:
                # chia các dòng trong phạm vi chiều rộng game 
                ds_dong = self.dong_goi_chu(nd["noidung"], RONG_GAME - 2 * DEM_GAME)
                # hiển thị các dong nd lên màn hình 
                for dong in ds_dong: 
                    # chuyen vb -> hinh anh (True-< khu rang cua -> chu muot hon)   
                    chu_nd = self.font_chu_noi_dung.render(dong, True, DEN)
                    # kt vi tri hop le de hien thi vb
                    # vitriNoidung_y >= self.vitri_batdau_noidung_y - 30: Đảm bảo dòng văn bản không bị hiển thị quá sớm (giữ khoảng cách ban đầu).
                    if vitri_y >= self.vitri_batdau_noidung_y - 30 and vitri_y < CAO_GAME - DEM_GAME:
                        self.screen.blit(chu_nd, (DEM_GAME ,vitri_y))
                        # k/c cac dong 
                    vitri_y += 25
                    # k/c doan van 
                vitri_y += 10 
            self.cuon_max = max(0, vitri_y - CAO_GAME + DEM_GAME)

        # thanh cuộn 
        if self.cuon_max > 0:
            chieucao_thanhcuon = CAO_GAME * (CAO_GAME - DEM_GAME) / (vitri_y + DEM_GAME)

            vitri_y_thanhcuon = DEM_GAME + (CAO_GAME - chieucao_thanhcuon - 2 * DEM_GAME) * self.cuon_y / self.cuon_max

            self.khung_thanh_cuon = pygame.Rect(RONG_GAME - 15, vitri_y_thanhcuon, 10, chieucao_thanhcuon)

            mau = XAM_DEN if self.dang_keo else XAM

            # ve thanh cuon
            pygame.draw.rect(self.screen, mau, self.khung_thanh_cuon, border_bottom_left_radius=5)


    def dong_goi_chu(self, chuoi, do_rong_toi_da):
        """Chia nhỏ văn bản thành nhiều dòng"""
        ds_cac_tu = chuoi.split() # ds luu cac tu cua chuoi
        ds_dong = [] # ds luu cac dong 
        dong_hien_tai = "" # chuoi tam de ghep tu 
        for tu in ds_cac_tu:
            x = dong_hien_tai + tu + " "
            # len dòng hiện tại + với từ đang xét vượt quá chiều rộng 
            if self.font_chu_noi_dung.size(x)[0] <=  do_rong_toi_da:
                dong_hien_tai = x # chap nhan dong hien tai hop le 
            else:
                # vuot qua chieu rong screen 
                ds_dong.append(dong_hien_tai.strip())
                # tu nay phai xuong dong -> bat dau dong moi voi tu hien tai 
                dong_hien_tai = tu + " "
            # neu con tu trong dong -> them vao ds dong
        if dong_hien_tai:
            ds_dong.append(dong_hien_tai.strip())
        return ds_dong

    def ve_nut_quay_lai(self):
        """Vẽ nút quay lại (hình tròn có mũi tên)"""
        
        # Chọn màu cho nút (màu xanh nhạt nếu di chuột vào, ngược lại màu xanh đậm)
        mau_nut = XANH_SANG if self.hover_nutquaylai else XANH

        # Vẽ hình tròn làm nền cho nút
        pygame.draw.circle(self.screen, mau_nut, self.nut_quay_lai.center, 20)

        # Tạo mũi tên chỉ sang trái
        diem_mui_ten = [
            (self.nut_quay_lai.centerx + 8, self.nut_quay_lai.centery - 12),  # Đầu trên của mũi tên
            (self.nut_quay_lai.centerx - 12, self.nut_quay_lai.centery),       # Đỉnh mũi tên
            (self.nut_quay_lai.centerx + 8, self.nut_quay_lai.centery + 12)    # Đầu dưới của mũi tên
        ]

        # Vẽ mũi tên màu trắng
        pygame.draw.polygon(self.screen, TRANG, diem_mui_ten)

    def xu_ly_su_kien(self):
        """Xử lý các sự kiện như nhấn chuột, di chuột và cuộn chuột"""
        # Duyệt qua tất cả các sự kiện trong Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Đóng Pygame
                sys.exit()     # Dừng chương trình

            # Sự kiện di chuyển chuột
            elif event.type == pygame.MOUSEMOTION:
                # Kiểm tra xem chuột có đang ở trên nút quay lại không
                self.hover_nutquaylai = self.nut_quay_lai.collidepoint(event.pos)
                
                # Nếu đang kéo thanh cuộn
                if self.dang_keo and self.cuon_max > 0:
                    mouse_y = event.pos[1]  # Lấy vị trí Y của chuột
                    # Tính toán khu vực cuộn và vị trí cuộn tương ứng
                    scroll_area_height = CAO_GAME - 2 * DEM_GAME - self.khung_thanh_cuon.height
                    self.cuon_y = ((mouse_y - DEM_GAME) / scroll_area_height) * self.cuon_max
                    self.cuon_y = max(0, min(self.cuon_y, self.cuon_max))  # Giới hạn cuộn

            # Sự kiện khi nhấn chuột
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Nếu nhấn chuột vào nút quay lại
                if self.nut_quay_lai.collidepoint(event.pos):
                    from src.gui.home_screen import HomeScreen
                    HomeScreen().run()  # Quay lại màn hình chính
                # Nếu nhấn chuột vào thanh cuộn
                elif self.khung_thanh_cuon and self.khung_thanh_cuon.collidepoint(event.pos):
                    self.dang_keo = True  # Bắt đầu kéo thanh cuộn
                # Cuộn chuột
                elif event.button == 4:  # Cuộn lên
                    self.cuon_y = max(0, self.cuon_y - 10)
                elif event.button == 5:  # Cuộn xuống
                    self.cuon_y = min(self.cuon_max, self.cuon_y + 10)

            # Sự kiện khi thả chuột
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dang_keo = False  # Dừng kéo thanh cuộn

    def run(self):
        while True:
            self.xu_ly_su_kien()
            self.ve_noidung()
            self.ve_nut_quay_lai()
            pygame.display.flip()
            pygame.time.Clock().tick(60)



def KhoiDongManHinhHD():
    hd = Tutorial_Screen()
    hd.run()

if __name__ == "__main__":
    KhoiDongManHinhHD()

