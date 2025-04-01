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

class khoiDongManHinhHuongDan():
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
        self.di_chuot_quay_lai = False 

        # Vị trí cố định cho tiêu đề và nội dung 
        self.tieude_y = 40 
        self.vitri_batdau_noidung_y = 80 

        # Cuộn nội dung 
        self.cuon_y = 0
        self.cuon_max = 0
        self.khung_thanh_cuon = None 
        self.dang_keo = False 

    def ve_nut_quay_lai(self):
        """Vẽ nút quay lại (hình tròn có mũi tên)"""
        
        # Chọn màu cho nút (màu xanh nhạt nếu di chuột vào, ngược lại màu xanh đậm)
        mau_nut = XANH_SANG if self.di_chuot_quay_lai else XANH

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
                self.di_chuot_quay_lai = self.nut_quay_lai.collidepoint(event.pos)
                
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
            # self.ve_noidung()
            self.ve_nut_quay_lai()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

def KhoiDongManHinhHD():
    hd = khoiDongManHinhHuongDan()
    hd.run()

if __name__ == "__main__":
    KhoiDongManHinhHD()

