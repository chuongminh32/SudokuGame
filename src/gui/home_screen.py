import pygame # thư viện tạo giao diện game 
import sys # thư viện để thoát game 
import os # thư viện để xử lý đường dẫn file 

# thêm đường dẫn để import các file khác trong dự án 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# kích thước cửa sổ game 
RONG_HOME = 650 
CAO_HOME = 700 

# kích thước và kc cho nút 
RONG_NUT = 250 
CAO_NUT = 60 
DEM_NUT = 30 # Phần đệm thêm 

# Màu 
MAU_TRANG = (255, 255, 255)
MAU_DEN = (0, 0, 0)
MAU_NEN_NUT = (90, 123, 192)
MAU_NEN_NUT_HOVER = (67, 99, 167)
MAU_TIEU_DE = (52, 72, 97)

# Lớp chính để tạo màn hình chính
class HomeScreen:
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()

        # Tạo cửa sổ game với kích thước đã định nghĩa
        self.screen = pygame.display.set_mode((RONG_HOME, CAO_HOME))

        # Đặt tiêu đề cho cửa sổ
        pygame.display.set_caption("Trò Chơi Sudoku")
        
        # Tạo các font chữ với kích thước khác nhau
        self.font_tieu_de = pygame.font.SysFont('verdana', 72)  # Font lớn cho tiêu đề
        self.font_tieu_de_phu = pygame.font.SysFont('verdana', 30)  # Font cho phụ đề
        self.font_nut = pygame.font.SysFont('verdana', 33)  # Font cho nút
        self.font_chan_trang = pygame.font.SysFont('verdana', 22)  # Font nhỏ cho chân trang
        
        # Tạo danh sách các nút bấm
        self.ds_nut = self.tao_ds_nut()
        
        # Đặt màu nền là màu trắng
        self.mau_nen = MAU_TRANG

    # hàm vẽ tiêu đề và tiêu đề phụ 
    def ve_tieu_de(self):
        # Vẽ chữ sudoku màu xanh 
        tieu_de = self.font_tieu_de.render("SUDOKU", True, MAU_TIEU_DE)
        khung_tieude = tieu_de.get_rect(center = (RONG_HOME // 2, 100))
        self.screen.blit(tieu_de, khung_tieude)

        # Vẽ chữ trò chơi 
        tieudephu = self.font_tieu_de_phu.render("TRÒ CHƠI", True, MAU_DEN)
        khung_tieudephu = tieudephu.get_rect(center = (RONG_HOME // 2, 160)) 
        self.screen.blit(tieudephu, khung_tieudephu)

        # Vẽ lưới trang trí 
        self.ve_luoi()
    
    # Hàm vẽ lưới nhỏ trang trí 
    def ve_luoi(self):
        kt_luoi = 130 
        kt_o = 40 
        x_luoi = RONG_HOME - kt_luoi - 20 
        y_luoi = 100

        for i in range(4):
            # tô đậm viền ngoài
            do_day = 3 if i in [0, 3] else 1

            """  (function) def line(
                surface: Surface,
                color: ColorValue,
                start_pos: Coordinate,
                end_pos: Coordinate,
                width: int = 1
            """
            # vẽ đường dọc 
            pygame.draw.line(self.screen, MAU_DEN, 
                            (x_luoi + i * kt_o, y_luoi),
                            (x_luoi + i * kt_o, y_luoi + kt_luoi), 
                            do_day)
            # vẽ đường ngang  
            pygame.draw.line(self.screen, MAU_DEN,
                             (x_luoi, y_luoi + i * kt_o),
                             (x_luoi + kt_luoi, y_luoi + i * kt_o),
                             do_day)
            # danh sách số hiển thị trong grid 
            ds_so = [[5, 3, 0], [6, 0, 0], [0, 9, 8]]
            # vẽ các số vào ô 
            for dong in range(3):
                for cot in range(3):
                    if(ds_so[dong][cot]!=0):

                        so = self.font_tieu_de_phu.render(str(ds_so[dong][cot]), True, MAU_TIEU_DE)

                        khung_so = so.get_rect(center = (x_luoi + cot * kt_o + kt_o // 2, y_luoi + dong * kt_o + kt_o // 2))

                        self.screen.blit(so, khung_so)
            
    # Hàm tạo ds nút 
    def tao_ds_nut(self):
        vi_tri_nut_y = 250 
        ds_nut = [
            # Nút chơi game 
            {'vitri': pygame.Rect((RONG_HOME - RONG_NUT) // 2, vi_tri_nut_y, RONG_NUT, CAO_NUT),
                'noi_dung': 'Chơi game',
                'mau': MAU_NEN_NUT,
                'mau_di_chuot': MAU_NEN_NUT_HOVER,
                'hanh_dong': self.bat_dau_choi_btn_click
            },
            # Nút hướng dẫn 
            {'vitri': pygame.Rect((RONG_HOME - RONG_NUT) // 2, vi_tri_nut_y + CAO_NUT + DEM_NUT, RONG_NUT, CAO_NUT),
                'noi_dung': 'Hướng dẫn',
                'mau': MAU_NEN_NUT,
                'mau_di_chuot': MAU_NEN_NUT_HOVER,
                'hanh_dong': self.huong_dan_btn_click
            },
            # Nút AI
            {'vitri': pygame.Rect((RONG_HOME - RONG_NUT) // 2, vi_tri_nut_y + CAO_NUT*2 + DEM_NUT*2, RONG_NUT, CAO_NUT),
                'noi_dung': 'AI',
                'mau': MAU_NEN_NUT,
                'mau_di_chuot': MAU_NEN_NUT_HOVER,
                'hanh_dong': self.ai_btn_click
            },
            # Nút thoát 
            {'vitri': pygame.Rect((RONG_HOME - RONG_NUT) // 2, vi_tri_nut_y + CAO_NUT*3 + DEM_NUT*3, RONG_NUT, CAO_NUT),
                'noi_dung': 'Thoát',
                'mau': MAU_NEN_NUT,
                'mau_di_chuot': MAU_NEN_NUT_HOVER,
                'hanh_dong': self.thoat_btn_click
            },
        ]
        return ds_nut
            
    # Vẽ các nút bấm lên màn hình 
    def ve_nut(self):
        vitri_nut = pygame.mouse.get_pos()
        for nut in self.ds_nut:
            # Đổi màu khi di chuột qua nút 
            mau_nut = None
            if nut['vitri'].collidepoint(vitri_nut):
                mau_nut = nut['mau_di_chuot']
            else :
                mau_nut = nut['mau']
            # Vẽ hcn cho nút và bo tròn 
            pygame.draw.rect(self.screen, mau_nut, nut['vitri'], border_radius=10)
            # vẽ chữ lên nút 
            chu = self.font_nut.render(nut['noi_dung'], True, MAU_TRANG)
            khung_chu = chu.get_rect(center=nut['vitri'].center) # tạo hcn, đặt center của chu vào vị trí giữ hcn 
            self.screen.blit(chu, khung_chu) # vẽ lên mh 

    # Hàm vẽ chân trang 
    def ve_chan_trang(self):
        chantrang = self.font_chan_trang.render("© 2025 Trò Chơi Sudoku - Group6_HCMUTE", True, MAU_DEN)
        khung_chantrang = chantrang.get_rect(center=(RONG_HOME//2, CAO_HOME-30))
        self.screen.blit(chantrang, khung_chantrang)
    
    # Hàm bắt sự kiện click nút chơi game 
    def bat_dau_choi_btn_click(self):
        from src.gui import game_screen
        game_screen.KhoiDongManHinhChoiGame()
    
    # Hàm bắt sự kiện click nút hướng dẫn  
    def huong_dan_btn_click(self):
        from src.gui import tutorial_screen
        tutorial_screen.KhoiDongManHinhHD()

    # Hàm bắt sự kiện click thoát game 
    def thoat_btn_click(self):
        pygame.quit()
        sys.exit()

    # Hàm click nút ai 
    def ai_btn_click(self):
        from src.gui import ai_screen
        ai_screen.KhoiDongManHinhAI()

    # Hàm xử lí sự kiện click chuột 
    def xu_li_su_kien(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.thoat_btn_click()
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                vitri = pygame.mouse.get_pos()
                for nut in self.ds_nut:
                    # Nếu click vào nút -> gọi hàm xử lí cho nút đó 
                    if nut['vitri'].collidepoint(vitri):
                        nut['hanh_dong']() 
    
    def run(self):
        """Nếu không có clock.tick(60), vòng lặp while sẽ chạy liên tục nhanh nhất có thể, dẫn đến việc sử dụng 100% CPU."""
        clock = pygame.time.Clock()  # Đặt đồng hồ để giới hạn FPS
        while True:
            self.xu_li_su_kien()  # Xử lý sự kiện
            self.screen.fill(self.mau_nen)  # Làm mới màn hình
            self.ve_tieu_de()
            self.ve_nut()
            self.ve_chan_trang  ()
            pygame.display.update()  # Cập nhật màn hình
            clock.tick(60)  # Giới hạn FPS


# Chạy chương trình
if __name__ == "__main__":
    game = HomeScreen()  # Tạo đối tượng game
    game.run()          # Chạy game