import pygame, os, sys
# Thư mục gốc
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Kích thước và màu
RONG_GAME, CAO_GAME = 700, 750
DEM_GAME = 30
TRANG = (255, 255, 255)
DEN = (0, 0, 0)
XANH = (90, 123, 192)

def load_image_relative(*path):
    return pygame.image.load(os.path.join(BASE_DIR, *path)).convert_alpha()

class Tutorial_Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((RONG_GAME, CAO_GAME))
        pygame.display.set_caption("Hướng Dẫn SUDOKU")

        # Fonts
        self.font_tieu_de = pygame.font.SysFont('Verdana', 40)
        self.font_tieu_de_noi_dung = pygame.font.SysFont('Verdana', 28)
        self.font_chu_noi_dung = pygame.font.SysFont('Verdana', 20)

        self.nut_quay_lai = None
        self.dang_chay = True

    def tao_noi_dung(self):
        return [
            {"kieu": "tieude", "noidung": "Cách Chơi Sudoku"},
            {"kieu": "noidung", "noidung": "Điền số 1-9 vào lưới 9x9 sao cho mỗi hàng, cột, ô 3x3 không lặp số."},
            {"kieu": "tieude", "noidung": "Hướng Dẫn Chơi"},
            {"kieu": "noidung", "noidung": "- Chọn 'Chơi Game' để tự giải."},
            {"kieu": "noidung", "noidung": "- Nhấn ô trống, nhập số 1-9."},
            {"kieu": "noidung", "noidung": "- Xóa số bằng phím Delete."},
            {"kieu": "noidung", "noidung": "- Dùng 'Gợi Ý' nếu cần."},
            {"kieu": "noidung", "noidung": "- Chọn 'Máy Giải' để xem máy giải."},
            {"kieu": "tieude", "noidung": "Mẹo Giải Sudoku"},
            {"kieu": "noidung", "noidung": "- Bắt đầu từ ô có nhiều số sẵn."},
            {"kieu": "noidung", "noidung": "- Loại trừ để tìm số đúng."},
            {"kieu": "noidung", "noidung": "- Tìm số theo từng số (1, 2, 3...)."},
            {"kieu": "noidung", "noidung": "- Chỉ điền khi chắc chắn."}
        ]

    def dong_goi_chu(self, chuoi, max_width):
        """Chia văn bản thành nhiều dòng ngắn"""
        tu = chuoi.split()
        dong, ds_dong = "", []
        for t in tu:
            tam = dong + t + " "
            if self.font_chu_noi_dung.size(tam)[0] <= max_width:
                dong = tam
            else:
                ds_dong.append(dong.strip())
                dong = t + " "
        if dong:
            ds_dong.append(dong.strip())
        return ds_dong

    def ve_noidung(self):
        self.screen.fill(TRANG)

        # Tiêu đề chính
        tieu_de = self.font_tieu_de.render("Hướng Dẫn", True, XANH)
        self.screen.blit(tieu_de, tieu_de.get_rect(center=(RONG_GAME // 2, 40)))

        vitri_y = 80
        noi_dung = self.tao_noi_dung()

        for item in noi_dung:
            if item["kieu"] == "tieude":
                vitri_y += 20
                text = self.font_tieu_de_noi_dung.render(item["noidung"], True, DEN)
                self.screen.blit(text, (DEM_GAME, vitri_y))
                vitri_y += 40
            else:
                for dong in self.dong_goi_chu(item["noidung"], RONG_GAME - 2 * DEM_GAME):
                    text = self.font_chu_noi_dung.render(dong, True, DEN)
                    self.screen.blit(text, (DEM_GAME, vitri_y))
                    vitri_y += 25
                vitri_y += 10

    def ve_nut_quay_lai(self):
        icon = load_image_relative("..","..", "assets", "icons8-go-back-48.png")
        rect = icon.get_rect(topleft=(12, 15))
        self.screen.blit(icon, rect)
        self.nut_quay_lai = rect

    def xu_ly_su_kien(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.nut_quay_lai and self.nut_quay_lai.collidepoint(event.pos):
                    self.dang_chay = False

    def run(self):
        while self.dang_chay:
            self.xu_ly_su_kien()
            self.ve_noidung()
            self.ve_nut_quay_lai()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

def KhoiDongManHinhHD():
    Tutorial_Screen().run()

if __name__ == "__main__":
    KhoiDongManHinhHD()
