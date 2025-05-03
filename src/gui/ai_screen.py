import pygame, sys, os, time, random, textwrap
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.utils_ai_screen import *
from src.algorithm.generate_sudoku import *
from src.algorithm.backtracking import *
from src.algorithm.simulate_anealing import *
from src.algorithm.hill_climbing import *
# Đường dẫn gốc đến thư mục gốc của dự án (Sudoku)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_relative_path(*paths):
    """Trả về đường dẫn tuyệt đối từ thư mục gốc dự án."""
    return os.path.join(BASE_DIR, *paths)
class Ai_Screen:
    def __init__(self):

        self.screen = init_pygame()
        pygame.display.set_caption("Sudoku - Chơi Game")
        self.font = pygame.font.SysFont("verdana", 25)
        self.font_text = pygame.font.SysFont("verdana", 20)
        self.tg_delay = 0.5
        self.size = 9
        self.gia_tri_cap_do = "E"
        self.gia_tri_alg = "B"
        self.bang,self.solution = tao_sudoku_theo_cap_do(self.size, self.gia_tri_cap_do)
        self.bang_goc = [row[:] for row in self.bang]
        self.bang_giai = None
        self.bang_sudoku = None # grid -> bắt sk click ngoài

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


        # sự kiện click nút trong bảng
        self.o_chon = None

        self.dangChayGame = True

        # nút
        self.nut_ss, self.reset_btn, self.ai_btn, self.back_btn, self.nut_dd_cap_do, self.nut_dd_alg, self.nut_bieu_do, self.nut_tao_de_sudoku, self.nut_thong_tin, self.nut_log = [None] * 10

        # view log (bật giao diện xem tiến trình giải)
        self.hien_log = False
        self.danh_sach_log = []
        self.log_limit = int((CAO - 3 * DEM) // 22)




        # -----------thông báo giải xong -------------
        self.hien_thong_bao_ai = False
        self.thoi_gian_giai = 0
        self.thoat_btn = None
        self.so_buoc = 0

        # log giải thuật
        self.log_sau_cung = ""  # Lưu log cuối để vẽ lại sau khi thuật toán kết thúc
        self.time = 0


        # cờ để bắt tín hiệu tạo đề
        self.dang_tao_de = False

        # cờ đã giải
        self.daGiaiThanhCong = False
        self.click_giai = False

        # error
        self.hien_bang_thong_bao_loi = False
        self.danh_sach_ve_loi = []
        self.gia_tri_trung = None
        self.vi_tri_sai = None
        self.thoat_btn_loi = None

        # nut resize kt bang
        self.nut_dd_size = None
        self.hien_bang_chon_size = False
        self.bang_chon_size = []
        self.ten_size = "9x9"
        self.KT_O = (RONG - 2 * DEM) // 9

        # nút điều chỉnh tốc độ hiện log
        self.nut_dd_delay = None
        self.hien_bang_delay = False
        self.bang_chon_delay = []
        self.ten_delay = "0.5s"

        # thanh cuộn
        self.log_scroll = 0  # chỉ số cuộn log


    def update_sudoku_board(self):
        """Cập nhật bảng Sudoku khi kích thước thay đổi."""
        # Khởi tạo lại bảng Sudoku dựa trên kích thước mới
        self.bang = []
        self.bang,_ = tao_sudoku_theo_cap_do(self.size, self.gia_tri_cap_do)
        self.bang_goc = [row[:] for row in self.bang]  # Lưu bảng gốc để so sánh sau này
        self.bang_giai = None  # Reset bảng giải
        self.bang_sudoku = None  # Reset bảng sudoku nếu có
        self.KT_O = (RONG - 2 * DEM) // self.size

    def xuLiSuKien(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.dangChayGame = False
            elif e.type == pygame.KEYDOWN:
                self.xuLiSuKienNhanPhim(e)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.xuLiSuKienClickChuot(e.pos)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                max_scroll = max(0, len(self.danh_sach_log) - self.max_lines_log)
                if e.button == 4:  # Lăn lên
                    self.log_scroll = max(0, self.log_scroll - 1)
                elif e.button == 5:  # Lăn xuống
                    self.log_scroll = min(max_scroll, self.log_scroll + 1)



    def kiemTraHopLe(self, board, row, col, num):
        """
        Trả về tuple (is_valid, ds_o_loi):
            - is_valid: True nếu hợp lệ, False nếu không
            - ds_o_loi: Danh sách các ô bị lỗi khi đặt số `num` vào vị trí (row, col)
        """
        base = math.isqrt(self.size)
        if num == 0:
            return True, []

        ds_o_loi = []

        # Kiểm tra hàng
        for i in range(self.size):
            if board[row][i] == num and i != col:
                ds_o_loi.append((row, i))

        # Kiểm tra cột
        for i in range(self.size):
            if board[i][col] == num and i != row:
                ds_o_loi.append((i, col))

        # Xác định góc trên trái của box
        box_row, box_col = base * (row // base), base * (col // base)

        # Kiểm tra ô box
        for i in range(box_row, box_row + base):
            for j in range(box_col, box_col + base):
                if board[i][j] == num and (i, j) != (row, col):
                    ds_o_loi.append((i, j))

        return len(ds_o_loi) == 0, ds_o_loi

    def xuLiSuKienNhanPhim(self, go_phim):
        if self.o_chon is None:
            return

        i, j = self.o_chon

        # Xử lý nhập số từ 1 đến 9
        if pygame.K_1 <= go_phim.key <= pygame.K_9:
            # Kiểm tra và cho phép nhập số vào ô
            if self.bang[i][j] is None:
                self.bang[i][j] = go_phim.key - pygame.K_0
            else:
                self.bang[i][j] = self.bang[i][j] * 10 + (go_phim.key - pygame.K_0)

        # Xử lý nhập số từ bàn phím số (KP1 đến KP9)
        elif pygame.K_KP1 <= go_phim.key <= pygame.K_KP9:
            if self.bang[i][j] is None:
                self.bang[i][j] = go_phim.key - pygame.K_KP0
            else:
                self.bang[i][j] = self.bang[i][j] * 10 + (go_phim.key - pygame.K_KP0)

        # Xử lý xóa giá trị trong ô
        elif go_phim.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
            self.bang[i][j] = 0

        # Kiểm tra tính hợp lệ của giá trị nhập vào
        is_hop_le, ds_o_loi = self.kiemTraHopLe(self.bang, i, j, self.bang[i][j])
        if not is_hop_le:
            # Nếu không hợp lệ, lưu các ô lỗi và thông báo lỗi
            self.danh_sach_ve_loi = ds_o_loi + [(i, j)]
            self.gia_tri_trung = self.bang[i][j]  # Lưu lại giá trị sai
            self.vi_tri_sai = (i, j)  # Lưu vị trí để xử lý sau
            self.hien_bang_thong_bao_loi = True  # Hiển thị bảng thông báo lỗi

        return

    def reset_game(self):
        """Reset toàn bộ trạng thái giao diện và dữ liệu Sudoku."""

        # Dừng tất cả chế độ đặc biệt
        self.hien_bang_cap_do = False
        self.hien_bang_chon_alg = False
        self.hien_bang_chon_bieu_do = False
        self.hien_thong_bao_ai = False

        # Reset bảng
        self.update_sudoku_board()

        # Reset các trạng thái giải AI
        self.so_buoc = 0
        self.ds_log = []
        self.log_sau_cung = ""
        self.dong_log_gan_nhat = ""
        self.thoi_gian_giai = 0
        self.daGiaiThanhCong = False
        self.click_giai = False

         # nut resize kt bang
        self.nut_dd_size = None
        self.hien_bang_chon_size = False
        self.bang_chon_size = []

        # Không có ô nào đang chọn
        self.o_chon = None

        # Xóa log cũ nếu có
        try:
            log_file_path = get_relative_path("data", "log_giai_sudoku.txt")
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            with open(log_file_path, "w", encoding="utf-8") as f:
                f.write("")
        except Exception as e:
            print("Không thể xóa log:", e)

        # Sau cùng vẽ lại màn hình 
        self.veCauTrucBang()
        pygame.display.update()

    # hàm giải sudoku theo thuật toán
    def giai_sudoku_theo_ten_alg(self):
        if self.gia_tri_alg == "B":
           self.bang_giai, self.so_buoc, self.daGiaiThanhCong = giai_sudoku_backtracking(self.bang,self.size, self.tg_delay, self.cap_nhat_gui_b)
           self.thoi_gian_giai = ghi_log_backtracking(self.bang, self.size)
        elif self.gia_tri_alg == "HC":
           self.bang_giai, self.so_buoc, self.daGiaiThanhCong = giai_sudoku_hill_climbing(self.bang,self.size, self.tg_delay, self.cap_nhat_gui_hc)
           self.thoi_gian_giai = ghi_log_hill_climbing(self.bang, self.size)
           print(self.bang)
           print(self.bang_giai)
           print(self.bang_goc)
           print(self.daGiaiThanhCong)
           print(self.size)
           print(self.so_buoc)
        elif self.gia_tri_alg == "SA":
            self.bang_giai, self.so_buoc , self.daGiaiThanhCong, self.thoi_gian_giai = giai_sudoku_simulated_annealing(self.bang,self.size,self.cap_nhat_gui_sa, self.tg_delay)
    
    def ve_log_giao_dien(self):
        log_x = DEM + self.size * self.KT_O + 70
        log_y = DEM
        log_width = RONG * 0.85
        log_height = CAO - 3 * DEM
        line_height = 22
        font = pygame.font.SysFont("consolas", 18)

        # Vẽ nền log
        pygame.draw.rect(self.screen, (30, 30, 30), (log_x, log_y, log_width, log_height))

        # Tính số dòng có thể hiển thị
        max_lines = int(log_height // line_height)
        self.max_lines_log = max_lines  # lưu lại để xử lý scroll

        # Cắt dòng hiển thị theo scroll
        start = max(0, len(self.danh_sach_log) - max_lines - self.log_scroll)
        end = start + max_lines
        logs_to_draw = self.danh_sach_log[start:end]

        # Vẽ log
        y = log_y + 5
        x = log_x + 10
        for dong in logs_to_draw:
            text = font.render(dong.strip(), True, (255, 255, 255))
            self.screen.blit(text, (x, y))
            y += line_height
    
    def cap_nhat_gui_hc(self, r, c, n, status, buoc,t, conflicts):
        mau_map = {
            "conflict": ((255, 193, 193), "Lỗi - Vi phạm quy tắc"),
            "improved": ((195, 247, 202), "Cải thiện"),
            "no_improvement" :(((255, 255, 204), "Không cải thiện"))
        }
        mau, trang_thai_text = mau_map.get(status, ((255, 255, 255), ""))

        # Tạo và lưu log -> ds_log -> gui
        dong_log = f"[{buoc}:{t:.4f}(s)] | conflicts: {conflicts} | ({r},{c}) <- {n} --> {trang_thai_text}\n"
        self.danh_sach_log.append(dong_log)

        # Vẽ ô và số
        pygame.draw.rect(self.screen, mau, pygame.Rect(
            DEM + c * self.KT_O + 1,
            DEM + r * self.KT_O + 1,
            self.KT_O - 2, self.KT_O - 2
        ))

        if n != 0:
            font = pygame.font.SysFont(None, int(self.KT_O * 0.6))
            text = font.render(str(n), True, (0, 0, 0))
            rect = text.get_rect(center=(
                DEM + c * self.KT_O + self.KT_O // 2,
                DEM + r * self.KT_O + self.KT_O // 2
            ))
            self.screen.blit(text, rect)

        self.ve_log_giao_dien()
        pygame.display.update()
        pygame.time.delay(10)   

    def cap_nhat_gui_b(self, row, col, value,  trang_thai, so_buoc):
        mau_map = {
            "sai": ((255, 193, 193), "Sai - Quay lui"),
            "dung": ((195, 247, 202), "Đúng"),
            "thu" :(((255, 255, 204), "Thử giá trị- Hợp lệ"))
        }
        mau, trang_thai_text = mau_map.get(trang_thai, ((255, 255, 255), ""))

        # Tạo và lưu log -> ds_log -> gui
        dong_log = f"[Bước {so_buoc}] ({row},{col}) <- {value} --> {trang_thai_text}"
        self.danh_sach_log.append(dong_log)

        # Vẽ ô và số
        pygame.draw.rect(self.screen, mau, pygame.Rect(
            DEM + col * self.KT_O + 1,
            DEM + row * self.KT_O + 1,
            self.KT_O - 2, self.KT_O - 2
        ))

        if value != 0:
            font = pygame.font.SysFont(None, int(self.KT_O * 0.6))
            text = font.render(str(value), True, (0, 0, 0))
            rect = text.get_rect(center=(
                DEM + col * self.KT_O + self.KT_O // 2,
                DEM + row * self.KT_O + self.KT_O // 2
            ))
            self.screen.blit(text, rect)

        self.ve_log_giao_dien()
        pygame.display.update()
        pygame.time.delay(10)

    def cap_nhat_gui_sa(self, r1, c1, r2, c2, v1, v2, score, conflicts,  thoi_gian_tong, sigma, trang_thai, buoc):
        mau_map = {
            "sai": ((255, 193, 193), "Sai - Quay lui"),
            "dung": ((195, 247, 202), "Đúng"),
            "thu" :(((255, 255, 204), "Thử giá trị- Hợp lệ"))
        }
        mau, trang_thai_text = mau_map.get(trang_thai, ((255, 255, 255), ""))

        # Tạo và lưu log
        dong_log = f" {buoc}:({r1},{c1})={v1} <=> ({r2},{c2})={v2} | e:{score:2} | cf:{conflicts} t:{thoi_gian_tong:.3f}s | s:{sigma:.3f}\n"
        self.danh_sach_log.append(dong_log)

        # Vẽ ô và số
        pygame.draw.rect(self.screen, mau, pygame.Rect(
            DEM + c1 * self.KT_O + 1,
            DEM + r1 * self.KT_O + 1,
            self.KT_O - 2, self.KT_O - 2
        ))
        pygame.draw.rect(self.screen, mau, pygame.Rect(
            DEM + c2 * self.KT_O + 1,
            DEM + r2 * self.KT_O + 1,
            self.KT_O - 2, self.KT_O - 2
        ))

        if v1 != 0:
            font = pygame.font.SysFont(None, int(self.KT_O * 0.6))
            text = font.render(str(v1), True, (0, 0, 0))
            rect = text.get_rect(center=(
                DEM + c1 * self.KT_O + self.KT_O // 2,
                DEM + r1 * self.KT_O + self.KT_O // 2
            ))
            self.screen.blit(text, rect)
        if v2 != 0:
            font = pygame.font.SysFont(None, int(self.KT_O * 0.6))
            text = font.render(str(v2), True, (0, 0, 0))
            rect = text.get_rect(center=(
                DEM + c2 * self.KT_O + self.KT_O // 2,
                DEM + r2 * self.KT_O + self.KT_O // 2
            ))
            self.screen.blit(text, rect)

        self.ve_log_giao_dien()
        pygame.display.update()
        pygame.time.delay(10)


    def xuLiSuKienClickChuot(self, vitri_click):
        x = vitri_click[0]
        y = vitri_click[1]

        # click nút back -> home
        if (self.back_btn is not None and self.back_btn.collidepoint(vitri_click)):
            self.dangChayGame = False

        # click nut info
        elif self.nut_thong_tin and self.nut_thong_tin.collidepoint(vitri_click):
            self.hien_thong_bao_ai = not self.hien_thong_bao_ai
            self.thoat_btn = None

        # click nut tao de sudoku
        elif self.nut_tao_de_sudoku.collidepoint(vitri_click):
            self.dang_tao_de = True
            # Xóa số trong grid hiện tại (reset grid) use list comprehension
            self.bang = [[0 for _ in range(self.size)] for _ in range(self.size)]  

        elif self.nut_dd_delay and self.nut_dd_delay.collidepoint(vitri_click):
            self.hien_bang_delay = not self.hien_bang_delay

        # click nút cấp độ
        elif self.nut_dd_cap_do.collidepoint(vitri_click):
            self.hien_bang_cap_do = not self.hien_bang_cap_do # toggle hien bang cap do

        # click nút alg
        elif self.nut_dd_alg.collidepoint(vitri_click):
            self.hien_bang_chon_alg = not self.hien_bang_chon_alg

        # cick nút size
        elif self.nut_dd_size and self.nut_dd_size.collidepoint(vitri_click):
            self.hien_bang_chon_size = not self.hien_bang_chon_size

        # click ô
        elif DEM <= x <= DEM + self.size * self.KT_O and DEM <= y <= DEM + self.size * self.KT_O  and not self.hien_bang_cap_do and not self.hien_bang_chon_alg and not self.hien_thong_bao_ai  and not self.hien_bang_thong_bao_loi and not self.hien_bang_chon_size:
            print(self.KT_O, self.size)
            cot = (x - DEM) // self.KT_O
            dong = (y - DEM) // self.KT_O
            self.o_chon = (dong, cot) # chọn ô

        # cick nút biểu đồ
        elif self.nut_bieu_do and self.nut_bieu_do.collidepoint(vitri_click):
            ve_bieu_do_tong_thoi_gian_so_buoc(self.ds_log)

       # click nút giải
        elif self.ai_btn.collidepoint(vitri_click):
            # Xóa log cũ nếu có
            self.danh_sach_log = []
            self.click_giai = True
            self.bang_goc = [row[:] for row in self.bang]
            self.dang_tao_de = False

            # Chạy với cập nhật GUI để trực quan hóa
            self.giai_sudoku_theo_ten_alg()  # CÓ cập nhật GUI

            # hiện thông báo giải xong
            self.hien_thong_bao_ai = True
            
            # Cập nhật bảng giải cho bảng chính
            self.bang = [row[:] for row in self.bang_giai]

            # pygame.display.update()


        # click nút thoát -> ẩn bảng thông báo
        elif self.thoat_btn != None:
            if self.thoat_btn.collidepoint(vitri_click):
                self.hien_thong_bao_ai = False
                self.thoat_btn = None

        # click nút thoát -> ẩn bảng thông báo lỗi
        elif self.hien_bang_thong_bao_loi and self.thoat_btn_loi and self.thoat_btn_loi.collidepoint(vitri_click):
        # Người dùng bấm nút "Thoát"

            # Xóa giá trị sai (i,j = vitrisai)
            i, j = self.vi_tri_sai
            self.bang[i][j] = 0

            # Ẩn bảng cảnh báo
            self.hien_bang_thong_bao_loi = False

            # Xóa danh sách lỗi
            self.danh_sach_ve_loi = []
            self.vi_tri_sai = None
            self.thoat_btn_loi = None

        # click nút reset
        elif self.reset_btn is not None and self.reset_btn.collidepoint(vitri_click):
            self.reset_game()

        # Nếu click ra ngoài bảng cấp độ thì ẩn bảng cấp độ
        elif self.hien_bang_cap_do and not self.rect_bang_cap_do.collidepoint(vitri_click):
            self.hien_bang_cap_do = False

        # Nếu click ra ngoài bảng chọn alg thì ẩn đi
        elif self.hien_bang_chon_alg and not self.rect_bang_alg.collidepoint(vitri_click):
            self.hien_bang_chon_alg = False

        # Xử lí sự kiện click từng cấp độ trong bảng( có thể sửa đề trực tiếp trong đề mẫu )
        elif self.hien_bang_cap_do == True:
            if self.dang_tao_de:
                self.reset_game()
            for cap_do in self.bang_cap_do:
                if cap_do["rect"].collidepoint(vitri_click):
                    self.gia_tri_cap_do = cap_do["value"] # cập nhất giá trị cấp độ đã chọn 
                    self.ten_cap_do = cap_do["text"] # hiển thị lên giao diện 
                    self.update_sudoku_board()
                    self.hien_bang_cap_do = False
                    break

        # Xử lí sự kiện click chọn alg
        elif self.hien_bang_chon_alg == True:
            for alg in self.bang_alg:
                if alg["rect"].collidepoint(vitri_click):
                    self.gia_tri_alg = alg["value"] # cập nhất giá trị cấp độ đã chọn
                    self.ten_alg = alg["text"] # hiển thị lên giao diện
                    # cập nhật lại từng ô trong bảng giải
                    self.hien_bang_chon_alg = False
                    break

        # Xử lí sự kiện click chọn size
        elif self.hien_bang_chon_size == True:
            for s in self.bang_chon_size:
                if s["rect"].collidepoint(vitri_click):
                    self.size = s["value"] # cập nhất giá trị cấp độ đã chọn
                    self.ten_size = s["text"] # hiển thị lên giao diện
                    # cập nhật lại từng ô trong bảng giải
                    self.hien_bang_chon_size = False
                    self.update_sudoku_board()  # Cập nhật lại bảng Sudoku
                    break

         # Xử lí sự kiện click chọn time delay
        elif self.hien_bang_delay == True:
            for t in self.bang_chon_delay:
                if t["rect"].collidepoint(vitri_click):
                    self.tg_delay = t["value"] # cập nhất giá trị cấp độ đã chọn
                    self.ten_delay = t["text"] # hiển thị lên giao diện
                    # cập nhật lại từng ô trong bảng giải
                    self.hien_bang_delay = False
                    break


        # click nut view log
        elif self.nut_log and self.nut_log.collidepoint(vitri_click):
            self.hien_log = not self.hien_log
            if self.hien_log:
                self.screen = pygame.display.set_mode((RONG * 1.9 , CAO))
            else:
                self.screen = pygame.display.set_mode((RONG, CAO))

        # click ra ngoai luoi -> xoa o dang chon
        elif self.bang_sudoku and not self.bang_sudoku.collidepoint(vitri_click):
            self.o_chon = None


    def veCauTrucBang(self):
        if self.click_giai:
            to_o_giai(self.screen, self.bang_goc, self.bang_giai, self.size)
        ve_so_ai(self.screen, self.bang, self.size)
        self.bang_sudoku = ve_luoi(self.screen, self.size)
        self.reset_btn, self.ai_btn, self.back_btn, self.nut_bieu_do, self.nut_tao_de_sudoku, self.nut_thong_tin, self.nut_log = ve_nut_ai(self.screen, self.size)
        self.nut_dd_cap_do = ve_nut_dd_bang_cap_do(self.screen, self.ten_cap_do)
        self.nut_dd_alg = ve_nut_dd_bang_alg(self.screen, self.ten_alg)
        self.nut_dd_size = ve_nut_dd_bang_size(self.screen, self.ten_size)
        self.ve_log_giao_dien()
        (self.screen, self.KT_O, self.size)
        self.nut_dd_delay = ve_nut_dd_bang_speedDelay(self.screen, self.KT_O, self.size, self.ten_delay)

    def run(self):
        while self.dangChayGame:
            self.screen.fill(TRANG)

            # Vẽ nền, lưới và số
            self.veCauTrucBang()

            # Highlight nếu có ô chọn -> vẽ trước để tránh che table khác
            if self.o_chon:
                dong, cot = self.o_chon
                ve_highlight_cho_o(self.screen, dong, cot, self.bang, self.size)
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
                self.thoat_btn = ve_thong_bao_giai_xong(self.screen, RONG, CAO, self.thoi_gian_giai, self.ten_alg, self.so_buoc, self.daGiaiThanhCong)

            # Nếu lỗi -> hiện thông báo lỗi
            if self.hien_bang_thong_bao_loi:
                # Tô đỏ các ô lỗi
                to_o_loi(self.screen, self.danh_sach_ve_loi, self.size)

                # Vẽ lại số và lưới
                ve_so_ai(self.screen, self.bang, self.size)
                ve_luoi(self.screen, self.size)
                self.thoat_btn_loi = ve_thong_bao_loi(self.screen, self.gia_tri_trung)


            # ve bảng chọn size
            if self.hien_bang_chon_size:
                self.bang_chon_size = ve_bang_chon_size(self.screen)

            # vẽ bảng chọn mức delay
            if self.hien_bang_delay:
                self.bang_chon_delay = ve_bang_chon_speedDelay(self.screen, self.KT_O, self.size)
            pygame.display.update()


def KhoiDongManHinhAI():
    sdk = Ai_Screen()
    sdk.run()

if __name__ == "__main__":
    KhoiDongManHinhAI()