import pygame, os, math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import re
import seaborn as sns
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RONG, CAO, DEM, KT_LUOI = 700, 750, 60, 9
CAO_NUT, KC_NUT = 40, 20
TRANG, DEN, XAM = (255,255,255), (0,0,0), (200,200,200)


# Tạo đường dẫn tương đối từ thư mục này
def get_relative_path(*paths):
    return os.path.join(BASE_DIR, *paths)

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((RONG, CAO))
    pygame.display.set_caption("Trò chơi Sudoku")
    return screen

def ve_nut_ai(screen, size):
    KT_O = (RONG - 2 * DEM) // size
    # Tính toán vị trí của các nút
    y_nut = DEM + size * KT_O + KC_NUT  # Vị trí y cho các nút
    w_nut = (RONG - 2 * DEM - 2 * KC_NUT) // 3  # Chiều rộng của mỗi nút, chia đều 3 nút

    font_size = 24  # Cỡ chữ cho các nút
    font = pygame.font.SysFont("verdana", font_size)

    # nút làm mới
    icon_ss_path = get_relative_path("..","..", "assets", "icons8-refresh-48.png")
    icon_lam_moi = pygame.image.load(icon_ss_path).convert_alpha()
    x = 120
    y = CAO - 90
    rect_nut_lam_moi = icon_lam_moi.get_rect(topleft=(x, y))
    screen.blit(icon_lam_moi, rect_nut_lam_moi)

    # nut back
    icon_ss_path = get_relative_path("..","..", "assets", "icons8-go-back-48.png")
    icon_back = pygame.image.load(icon_ss_path).convert_alpha()
    # Vị trí icon
    x = 12
    y = 15
    # Lấy rect từ icon và đặt vị trí
    rect_nut_back = icon_back.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_back, rect_nut_back)

    # nut chart
    icon_chart_path = get_relative_path("..","..", "assets", "chart.png")
    icon_chart = pygame.image.load(icon_chart_path).convert_alpha()
    icon_chart = pygame.transform.scale(icon_chart, (40, 40))
    # Vị trí icon
    x = RONG - 160
    y = CAO - 90
    # Lấy rect từ icon và đặt vị trí
    rect_btn_chart = icon_chart.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_chart, rect_btn_chart)

    # nut tao de bai
    icon_create_topic = get_relative_path("..","..", "assets", "icons8-plus-50.png")
    icon_topic = pygame.image.load(icon_create_topic).convert_alpha()
    # Vị trí icon
    x = RONG - 340
    y = 12
    # Lấy rect từ icon và đặt vị trí
    rect_nut_tao_de_bai = icon_topic.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_topic, rect_nut_tao_de_bai)

    # nut info
    icon_info = get_relative_path("..","..", "assets", "info.png")
    icon_if = pygame.image.load(icon_info).convert_alpha()
    # Vị trí icon
    x = RONG - 400
    y = 12
    # Lấy rect từ icon và đặt vị trí
    rect_nut_thong_tin = icon_if.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_if, rect_nut_thong_tin)

    # nút log (xem chi tiết các bước giải)
    icon_log = get_relative_path("..","..", "assets", "log.png")
    img_log = pygame.image.load(icon_log).convert_alpha()
    # Vị trí icon
    x = RONG - 50
    y = (CAO - 2*DEM) // 2
    # Lấy rect từ icon và đặt vị trí
    rect_nut_log = img_log.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(img_log, rect_nut_log)

    # nút reset bảng 
    path_icon_reset_path = get_relative_path("..","..", "assets", "reset_board.png")
    icon_reset = pygame.image.load(path_icon_reset_path).convert_alpha()
    # Vị trí icon
    x = RONG - 50
    y = (CAO - 2*DEM) // 2 - 50
    # Lấy rect từ icon và đặt vị trí
    rect_btn_reset_board = icon_reset.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_reset, rect_btn_reset_board)

    # Nút AI giải
    nut_ai = pygame.Rect(DEM + w_nut + KC_NUT, y_nut, w_nut, CAO_NUT)
    pygame.draw.rect(screen, (98,123,192), nut_ai, border_radius=8)
    text_lam_moi = font.render("Giải", True, TRANG)
    screen.blit(text_lam_moi, text_lam_moi.get_rect(center=nut_ai.center))

    return rect_nut_lam_moi, nut_ai, rect_nut_back, rect_btn_chart, rect_nut_tao_de_bai, rect_nut_thong_tin, rect_nut_log, rect_btn_reset_board

def to_o_giai(screen, bang_goc, bang_giai, size):
    KT_O = (RONG - 2*DEM) // size
    for i in range(size):
        for j in range(size):
            if bang_giai != None:
                if bang_giai[i][j] != 0 and bang_goc[i][j] == 0:  # Kiểm tra ô có giá trị trong bảng giải nhưng không có trong bảng ban đầu
                    # Vẽ hình chữ nhật với màu để tô ô
                    pygame.draw.rect(
                        screen,
                        (204, 255, 229),  # Màu xanh nhạt (hoặc màu bạn muốn)
                        (DEM + j * KT_O + 1, DEM + i * KT_O + 1, KT_O - 2, KT_O - 2)  # Tô trong ô
                    )
def to_lai_o_cho_bang_reset(screen, bang_goc, size):
    KT_O = (RONG - 2*DEM) // size
    for i in range(size):
        for j in range(size):
            if bang_goc[i][j] == 0:  # Kiểm tra ô có giá trị trong bảng giải nhưng không có trong bảng ban đầu
                # Vẽ hình chữ nhật với màu để tô ô
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),  # Màu xanh nhạt (hoặc màu bạn muốn)
                    (DEM + j * KT_O + 1, DEM + i * KT_O + 1, KT_O - 2, KT_O - 2)  # Tô trong ô
                )

def to_o_loi(screen, ds_loi, size):
    KT_O = (RONG - 2*DEM) // size
    for dong, cot in ds_loi:
        pygame.draw.rect(screen, (250, 180, 180), pygame.Rect(DEM + cot * KT_O, DEM + dong * KT_O, KT_O, KT_O))

def ve_so_ai(screen, bang, size):
    KT_O = (RONG - 2 * DEM) // size
    font_size = KT_O // 2  # Bạn có thể điều chỉnh tỷ lệ này để font không quá lớn hoặc quá nhỏ
    font = pygame.font.SysFont("verdana", font_size)
    for i in range(size):
        for j in range(size):
            if bang[i][j]:
                # Xác định màu chữ
                mau = (25, 53, 88)
                # Vẽ số
                text = font.render(str(bang[i][j]), True, mau)
                rect = text.get_rect(center=(DEM + j * KT_O + KT_O // 2, DEM + i * KT_O + KT_O // 2))
                screen.blit(text, rect)

def ve_luoi(screen, size):
    """
    Vẽ lưới Sudoku với kích thước bảng n x n.
    :param screen: Màn hình pygame
    :param n: Kích thước bảng Sudoku (n x n)
    :param KT_O: Kích thước ô
    :param DEM: Khoảng cách lề
    """
    KT_O = (RONG - 2 * DEM) // size
    # Vẽ lưới Sudoku
    for i in range(size + 1):
        duongVien = 3 if i % int(size ** 0.5) == 0 else 1  # Tùy vào kích thước khối con (3x3, 4x4, v.v.)
        # Vẽ đường dọc
        pygame.draw.line(screen, (0, 0, 0), (DEM + i * KT_O, DEM), (DEM + i * KT_O, DEM + size * KT_O), duongVien)
        # Vẽ đường ngang
        pygame.draw.line(screen, (0, 0, 0), (DEM, DEM + i * KT_O), (DEM + size * KT_O, DEM + i * KT_O), duongVien)

    # Trả về hình chữ nhật bao quanh toàn bộ lưới để kiểm tra click ở ngoài
    return pygame.Rect(DEM, DEM, KT_O * size, KT_O * size)

def ve_nut_dd_bang_cap_do(screen, ten_cap_do):
    """Vẽ combobox chọn cấp độ khó dễ (Dễ, Trung bình, Khó)."""

    # Vị trí và kích thước của combobox
    box_x, box_y = RONG - 170, 20
    box_rong, box_cao = 100, 30
    box_rect = pygame.Rect(box_x, box_y, box_rong, box_cao)

    # Vẽ nền và viền
    pygame.draw.rect(screen, TRANG, box_rect, border_radius=5)
    pygame.draw.rect(screen, XAM, box_rect, 2, border_radius=5)

    # Vẽ văn bản và mũi tên
    font = pygame.font.SysFont("verdana", 12)
    text_surf = font.render(ten_cap_do, True, DEN)

    # Căn giữa chữ trong box, -10 - tranh đụng vào icon arow down
    text_x = box_x + (box_rong - text_surf.get_width()) // 2 - 10
    text_y = box_y + (box_cao - text_surf.get_height()) // 2

    screen.blit(text_surf, (text_x, text_y))

    # Vẽ mũi tên xuống
    arrow_points = [
        (box_x + box_rong - 20, box_y + box_cao//2 - 3),
        (box_x + box_rong - 10, box_y + box_cao//2 - 3),
        (box_x + box_rong - 15, box_y + box_cao//2 + 5)
    ]
    pygame.draw.polygon(screen, DEN, arrow_points)

    return box_rect  # Trả về hình chữ nhật của combobox để phát hiện sự kiện click

def ve_bang_chia_cap_do(screen):
    """Hiển thị bảng chọn cấp độ: Dễ, Trung bình, Khó."""

    box_rong, box_cao = 200, 200
    box_x, box_y = RONG - 270, 50
    bang_cap_do = [
        {"text": "Dễ", "value": "E", "rect": pygame.Rect(box_x + 23, box_y + 40, 150, 40)},
        {"text": "Trung bình", "value": "M", "rect": pygame.Rect(box_x + 23, box_y + 90, 150, 40)},
        {"text": "Khó", "value": "H", "rect": pygame.Rect(box_x + 23, box_y + 140, 150, 40)},
    ]

    font = pygame.font.SysFont("verdana", 20)

    # Vẽ bảng trắng
    bang_bao_quanh = pygame.draw.rect(screen, TRANG, pygame.Rect(box_x, box_y, box_rong, box_cao), border_radius=10)

    # Vẽ tiêu đề
    title_font = pygame.font.SysFont("verdana", 22)
    title_text = title_font.render("Chọn cấp độ", True, DEN)
    screen.blit(title_text, (box_x + (box_rong - title_text.get_width()) // 2, box_y + 10))

    # Vẽ các nút cấp độ
    for cap_do in bang_cap_do:
        pygame.draw.rect(screen, TRANG, cap_do["rect"], border_radius=5)
        pygame.draw.rect(screen, XAM, cap_do["rect"], 2, border_radius=5)

        # Hiển thị văn bản căn giữa
        text_surf = font.render(cap_do["text"], True, DEN)
        screen.blit(text_surf, (
            cap_do["rect"].x + (cap_do["rect"].width - text_surf.get_width()) // 2,
            cap_do["rect"].y + (cap_do["rect"].height - text_surf.get_height()) // 2
        ))

    return bang_cap_do, bang_bao_quanh
#_________________ Nút lựa chọn alg _____________________
def ve_nut_dd_bang_alg(screen, ten_alg):
    """Vẽ nút dropdown."""

    # Vị trí và kích thước của combobox
    box_x, box_y = RONG - 620, 20
    box_rong, box_cao = 200, 30
    box_rect = pygame.Rect(box_x, box_y, box_rong, box_cao)

    # Vẽ nền và viền
    pygame.draw.rect(screen, TRANG, box_rect, border_radius=5)
    pygame.draw.rect(screen, XAM, box_rect, 2, border_radius=5)

    # Vẽ văn bản và mũi tên
    font = pygame.font.SysFont("verdana", 17)
    text_surf = font.render(ten_alg, True, DEN)

    # Căn giữa chữ trong box, -10 - tranh đụng vào icon arow down
    text_x = box_x + (box_rong - text_surf.get_width()) // 2 - 10
    text_y = box_y + (box_cao - text_surf.get_height()) // 2

    screen.blit(text_surf, (text_x, text_y))

    # Vẽ mũi tên xuống
    arrow_points = [
        (box_x + box_rong - 20, box_y + box_cao//2 - 3),
        (box_x + box_rong - 10, box_y + box_cao//2 - 3),
        (box_x + box_rong - 15, box_y + box_cao//2 + 5)
    ]
    pygame.draw.polygon(screen, DEN, arrow_points)

    return box_rect  # Trả về hình chữ nhật của combobox để phát hiện sự kiện click

def ve_bang_chon_alg(screen):
    """Vẽ combobox chọn alg(backtracking, hill-climbing, sa)."""

    box_rong, box_cao = 250, 200
    box_x, box_y = RONG - 630, 50
    bang_alg = [
        {"text": "Backtracking", "value": "B", "rect": pygame.Rect(box_x + 23, box_y + 40, 200, 40)},
        {"text": "Hill Climbing", "value": "HC", "rect": pygame.Rect(box_x + 23, box_y + 90, 200, 40)},
        {"text": "Simulated Anealing", "value": "SA", "rect": pygame.Rect(box_x + 23, box_y + 140, 200, 40)},
    ]

    font = pygame.font.SysFont("verdana", 18)

    # Vẽ bảng trắng
    rect_bang_alg = pygame.draw.rect(screen, TRANG, pygame.Rect(box_x, box_y, box_rong, box_cao), border_radius=10)

    # Vẽ tiêu đề
    title_font = pygame.font.SysFont("verdana", 20)
    title_text = title_font.render("Chọn thuật toán", True, DEN)
    screen.blit(title_text, (box_x + (box_rong - title_text.get_width()) // 2, box_y + 10))

    # Vẽ các nút cấp độ
    for alg in bang_alg:
        pygame.draw.rect(screen, TRANG, alg["rect"], border_radius=5)
        pygame.draw.rect(screen, XAM, alg["rect"], 2, border_radius=5)

        # Hiển thị văn bản căn giữa
        text_surf = font.render(alg["text"], True, DEN)
        screen.blit(text_surf, (
            alg["rect"].x + (alg["rect"].width - text_surf.get_width()) // 2,
            alg["rect"].y + (alg["rect"].height - text_surf.get_height()) // 2
        ))

    return bang_alg, rect_bang_alg

# Vẽ dropdown chọn kích thước bảng Sudoku
def ve_nut_dd_bang_size(screen, size_board="9x9"):
    """Vẽ nút dropdown cho kích thước bảng Sudoku."""

    # Vị trí và kích thước của combobox
    box_x, box_y = RONG - 260, 20
    box_rong, box_cao = 80, 30
    box_rect = pygame.Rect(box_x, box_y, box_rong, box_cao)

    # Vẽ nền và viền
    pygame.draw.rect(screen, TRANG, box_rect, border_radius=5)
    pygame.draw.rect(screen, XAM, box_rect, 2, border_radius=5)

    # Vẽ văn bản và mũi tên
    font = pygame.font.SysFont("verdana", 15)
    text_surf = font.render(size_board, True, DEN)

    # Căn giữa chữ trong box, -10 - tránh đụng vào icon mũi tên xuống
    text_x = box_x + (box_rong - text_surf.get_width()) // 2 - 10
    text_y = box_y + (box_cao - text_surf.get_height()) // 2

    screen.blit(text_surf, (text_x, text_y))

    # Vẽ mũi tên xuống
    arrow_points = [
        (box_x + box_rong - 20, box_y + box_cao//2 - 3),
        (box_x + box_rong - 10, box_y + box_cao//2 - 3),
        (box_x + box_rong - 15, box_y + box_cao//2 + 5)
    ]
    pygame.draw.polygon(screen, DEN, arrow_points)

    return box_rect  # Trả về hình chữ nhật của combobox để phát hiện sự kiện click

# Vẽ bảng chọn kích thước cho Sudoku
def ve_bang_chon_size(screen):
    """Vẽ combobox chọn kích thước bảng Sudoku (9x9, 16x16, 25x25)."""

    box_x, box_y = RONG - 280, 55
    box_rong, box_cao = 120, 100
    bang_size = [
        {"text": "4x4", "value": 4, "rect": pygame.Rect(box_x + 23, box_y + 10, 80, 40)},
        {"text": "9x9", "value": 9, "rect": pygame.Rect(box_x + 23 , box_y + 60, 80, 40)},
        {"text": "16x16", "value": 16, "rect": pygame.Rect(box_x + 23, box_y + 110, 80, 40)},
        {"text": "25x25", "value": 25, "rect": pygame.Rect(box_x + 23, box_y + 160, 80, 40)},
    ]

    font = pygame.font.SysFont("verdana", 18)

    # Vẽ bảng trắng
    pygame.draw.rect(screen, TRANG, pygame.Rect(box_x, box_y, box_rong, 210), border_radius=10)

    # Vẽ các nút kích thước
    for size in bang_size:
        pygame.draw.rect(screen, TRANG, size["rect"], border_radius=5)
        pygame.draw.rect(screen, XAM, size["rect"], 2, border_radius=5)

        # Hiển thị văn bản căn giữa
        text_surf = font.render(size["text"], True, DEN)
        screen.blit(text_surf, (
            size["rect"].x + (size["rect"].width - text_surf.get_width()) // 2,
            size["rect"].y + (size["rect"].height - text_surf.get_height()) // 2
        ))

    return bang_size  # Trả về danh sách các nút kích thước


# Vẽ dropdown chọn kích thước bảng Sudoku
def ve_nut_dd_bang_speedDelay(screen, KT_O, size, delay = "0.5s"):
    """Vẽ nút dropdown cho delay hiện log."""

    # Vị trí và kích thước của combobox
    box_x, box_y = DEM + KT_O*size + 70, 20
    box_rong, box_cao = 80, 30
    box_rect = pygame.Rect(box_x, box_y, box_rong, box_cao)

    # Vẽ nền và viền
    pygame.draw.rect(screen, TRANG, box_rect, border_radius=5)
    pygame.draw.rect(screen, XAM, box_rect, 2, border_radius=5)

    # Vẽ văn bản và mũi tên
    font = pygame.font.SysFont("verdana", 15)
    text_surf = font.render(delay, True, DEN)

    # Căn giữa chữ trong box, -10 - tránh đụng vào icon mũi tên xuống
    text_x = box_x + (box_rong - text_surf.get_width()) // 2 - 10
    text_y = box_y + (box_cao - text_surf.get_height()) // 2

    screen.blit(text_surf, (text_x, text_y))

    # Vẽ mũi tên xuống
    arrow_points = [
        (box_x + box_rong - 20, box_y + box_cao//2 - 3),
        (box_x + box_rong - 10, box_y + box_cao//2 - 3),
        (box_x + box_rong - 15, box_y + box_cao//2 + 5)
    ]
    pygame.draw.polygon(screen, DEN, arrow_points)

    return box_rect  # Trả về hình chữ nhật của combobox để phát hiện sự kiện click

# Vẽ bảng chọn kích thước cho Sudoku
def ve_bang_chon_speedDelay(screen, KT_O, size):
    """Vẽ combobox chọn delay bảng log  (0.1, 0.5, 1)."""
    box_x, box_y = DEM + size * KT_O + 70, 55
    # box_x, box_y = RONG - 280, 55
    box_rong, box_cao = 90, 30
    bang_size = [
        {"text": "0.01s", "value": 0.01, "rect": pygame.Rect(box_x, box_y + 10, 80, 40)},
        {"text": "0.1s", "value": 0.1, "rect": pygame.Rect(box_x, box_y + 60, 80, 40)},
        {"text": "0.5s", "value": 0.5, "rect": pygame.Rect(box_x, box_y + 110, 80, 40)},
         {"text": "1s", "value": 1, "rect": pygame.Rect(box_x, box_y + 160, 80, 40)},
    ]

    font = pygame.font.SysFont("verdana", 18)

    # Vẽ bảng trắng
    pygame.draw.rect(screen, TRANG, pygame.Rect(box_x, box_y, box_rong, 210), border_radius=10)

    # Vẽ các nút kích thước
    for size in bang_size:
        pygame.draw.rect(screen, TRANG, size["rect"], border_radius=5)
        pygame.draw.rect(screen, XAM, size["rect"], 2, border_radius=5)

        # Hiển thị văn bản căn giữa
        text_surf = font.render(size["text"], True, DEN)
        screen.blit(text_surf, (
            size["rect"].x + (size["rect"].width - text_surf.get_width()) // 2,
            size["rect"].y + (size["rect"].height - text_surf.get_height()) // 2
        ))

    return bang_size  # Trả về danh sách các nút kích thước


def ve_highlight_cho_o(screen, row, col, grid, size):
    base = math.isqrt(size)
    KT_O = (RONG - 2 * DEM) // size

    sr = (row // base) * base  # Xác định hàng đầu của box
    sc = (col // base) * base  # Xác định cột đầu của box

    gia_tri_o_dang_duoc_chon = grid[row][col]

    # Rect(x, y, w, h)
    # x : trai -> phai : dùng cho col
    # Tô màu highlight cho hàng và cột
    for i in range(size):  # Duyệt theo hàng (row)
        pygame.draw.rect(screen, (150, 190, 228), pygame.Rect(
            DEM + i * KT_O,  # Cột thay đổi, x tăng dần
            DEM + row * KT_O,  # Hàng giữ nguyên, y không đổi
            KT_O, KT_O
        ))

    for j in range(size):  # Duyệt theo cột (column)
        pygame.draw.rect(screen, (150, 190, 228), pygame.Rect(
            DEM + col * KT_O,  # Cột giữ nguyên
            DEM + j * KT_O,  # Hàng thay đổi
            KT_O, KT_O
        ))


    # Tô màu cho ô 3x3 chứa ô đang chọn
    for i in range(base):
        for j in range(base):
            ar = sr + i  # ar = actual_row(dòng chính xác tính từ vị trí chỉ số), sr = start_row
            ac = sc + j

            pygame.draw.rect(screen, (150, 190, 228), pygame.Rect(
                DEM + ac * KT_O,
                DEM + ar * KT_O,
                KT_O, KT_O
            ))

    # Tô tất cả ô cùng giá trị
    if gia_tri_o_dang_duoc_chon == 0:
         pygame.draw.rect(screen, (187, 222, 251), pygame.Rect(DEM + col* KT_O, DEM + row* KT_O, KT_O, KT_O))
    else:
        for r in range(size):
            for c in range(size):
                if (grid[r][c] == gia_tri_o_dang_duoc_chon):
                    pygame.draw.rect(screen, (187, 222, 251), pygame.Rect(DEM + c* KT_O, DEM + r * KT_O, KT_O, KT_O))

def ve_thong_bao_giai_xong(screen, RONG, CAO, tg_giai, ten_alg, so_buoc, da_giai_thanh_cong):
    """Hiển thị bảng thông báo giải xong."""

    # Tạo lớp nền mờ
    overlay = pygame.Surface((RONG, CAO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # Màu đen với độ trong suốt
    screen.blit(overlay, (0, 0))

    # Kích thước bảng thông báo
    box_rong, box_cao = 510, 245
    box_x = (RONG - box_rong) // 2
    box_y = (CAO - box_cao) // 2

    # Vẽ bảng trắng
    pygame.draw.rect(screen, (255, 255, 255),
                                       pygame.Rect(box_x, box_y, box_rong, box_cao), border_radius=10)

    # Vẽ chữ thông báo
    font1 = pygame.font.SysFont("verdana", 28)
    font2 = pygame.font.SysFont("Segoe UI Emoji", 28)  # Font hỗ trợ emoji trên Windows
    font_sub = pygame.font.SysFont("verdana", 20)
    if da_giai_thanh_cong == True:
            text = font1.render("Đã giải thành công ", True, (52, 72, 97))
            icon = font2.render("✅", True, (52, 72, 97))
    else: 
        text = font1.render("Không giải được", True, (52, 72, 97))
        icon = font2.render("❌", True, (52, 72, 97))
    text_sub = font_sub.render(f"Thuật toán sử dụng: {ten_alg}", True, (148, 163, 183))
    vitri_text_x = box_x + (box_rong - text.get_width()) // 2
    screen.blit(text, (vitri_text_x, box_y + 20))
    screen.blit(icon, (vitri_text_x+text.get_width(), box_y + 20))
    screen.blit(text_sub, (box_x + (box_rong - text_sub.get_width()) // 2, box_y + 70))

    # Tính giây và mili giây
    time_text = f"Thời gian giải: {tg_giai:.6f} (giây)"
    step = f"Tổng số bước thử: {so_buoc}(bước)"


    # Vẽ thời gian
    font_time = pygame.font.SysFont("verdana", 18)
    time_render = font_time.render(time_text, True, (52, 72, 97))
    screen.blit(time_render, (box_x + (box_rong - time_render.get_width()) // 2, box_y + 100))

    # Vẽ số bước
    font_step = pygame.font.SysFont("verdana", 18)
    step_render = font_step.render(step, True, (52, 72, 97))
    screen.blit(step_render, (box_x + (box_rong - step_render.get_width()) // 2, box_y + 130))

    # Vẽ nút "Thoát" ở giữa
    btn_width, btn_height = 150, 50
    btn_x = box_x + (box_rong - btn_width) // 2  # Căn giữa
    btn_y = box_y + 170
    thoat_btn = pygame.draw.rect(screen, (90, 123, 192),
                                 pygame.Rect(btn_x, btn_y, btn_width, btn_height), border_radius=10)

    text = font1.render("Thoát", True, (255, 255, 255))
    screen.blit(text, (btn_x + 30, btn_y + 5))

    return thoat_btn

def ve_thong_bao_loi(screen, giatritrung):
    """Vẽ bảng cảnh báo ô nhập sai Sudoku."""

    # Lớp nền mờ nhẹ hơn
    overlay = pygame.Surface((RONG, CAO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 50))  # Độ trong suốt nhẹ (80 thay vì 150)
    screen.blit(overlay, (0, 0))

    # Kích thước bảng thông báo nhỏ hơn
    box_rong, box_cao = 400, 180
    box_x = (RONG - box_rong) // 2
    box_y = (CAO - box_cao) // 2

    # Vẽ bảng trắng bán trong suốt
    box_surface = pygame.Surface((box_rong, box_cao), pygame.SRCALPHA)
    box_surface.fill((255, 255, 255, 230))  # Bảng trắng hơi trong suốt
    screen.blit(box_surface, (box_x, box_y))

    # Vẽ chữ thông báo
    font = pygame.font.SysFont("verdana", 24)
    font_sub = pygame.font.SysFont("verdana", 18)

    text = font.render("Ô nhập bị sai logic Sudoku!", True, (52, 72, 97))
    text_sub = font_sub.render(f"Giá trị bạn vừa nhập: {giatritrung} bị trùng!", True, (148, 163, 183))
    screen.blit(text, (box_x + 30, box_y + 20))
    screen.blit(text_sub, (box_x + 30, box_y + 70))

    # Vẽ nút "Thoát"
    btn_width, btn_height = 120, 40
    btn_x = box_x + (box_rong - btn_width) // 2
    btn_y = box_y + 120
    thoat_btn = pygame.draw.rect(screen, (90, 123, 192),
                                 pygame.Rect(btn_x, btn_y, btn_width, btn_height), border_radius=8)

    text_btn = font_sub.render("Thoát", True, (255, 255, 255))
    screen.blit(text_btn, (btn_x + 30, btn_y + 8))

    return thoat_btn

# _____________________vẽ biểu đồ ____________________________________

def ve_bieu_do_phan_tich_b(file_path):
    steps = []
    times = []
    rows = []
    cols = []
    values = []

    # Regex để bắt thông tin trong dòng log
    pattern = r"(\d+):([\d.]+) \((\d+),(\d+)\) <- (\d+)"

    # Đọc file và parse
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                step = int(match.group(1))
                time = float(match.group(2))
                row = int(match.group(3))
                col = int(match.group(4))
                value = int(match.group(5))

                steps.append(step)
                times.append(time)
                rows.append(row)
                cols.append(col)
                values.append(value)

    # Tạo figure với 2 hàng 2 cột
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    fig.suptitle("GIẢI SUDOKU VỚI BACKTRACKING", fontsize=16,fontweight='bold')

    # 1. Biểu đồ thời gian theo bước
    axs[0, 0].plot(steps, times, marker='o')
    axs[0, 0].set_xlabel("Bước")
    axs[0, 0].set_ylabel("Thời gian (giây)")
    axs[0, 0].set_title("Thời gian theo bước")
    axs[0, 0].grid(True)

    # 2. Scatter vị trí các ô thử giá trị
    sc = axs[0, 1].scatter(cols, rows, c=steps, cmap='viridis', s=100)
    axs[0, 1].invert_yaxis()
    axs[0, 1].set_xlabel("Cột")
    axs[0, 1].set_ylabel("Hàng")
    axs[0, 1].set_title("Vị trí các ô thử giá trị")
    fig.colorbar(sc, ax=axs[0, 1], label='Bước')

    # 3. Heatmap giá trị đã thử trên lưới Sudoku
    grid = np.zeros((9, 9), dtype=int)
    for r, c, v in zip(rows, cols, values):
        grid[r][c] = v
    sns.heatmap(grid, annot=True, fmt='d', cmap='YlGnBu', cbar=False, ax=axs[1, 0])
    axs[1, 0].set_title("Lưới Sudoku sau khi thử các giá trị")

    # 4. Biểu đồ cột giá trị được thử theo bước
    axs[1, 1].bar(steps, values)
    axs[1, 1].set_xlabel("Bước")
    axs[1, 1].set_ylabel("Giá trị được thử")
    axs[1, 1].set_title("Giá trị được thử theo từng bước")
    axs[1, 1].set_yticks(range(1, max(values)+1))
    axs[1, 1].grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # dành chỗ cho tiêu đề chung
    plt.show()

def ve_bieu_do_phan_tich_sa(log_path):

    # Lấy dữ liệu từ log
    def phan_tich_log(log_path):
        buoc = []
        loi = []
        conflicts = []
        thoi_gian = []
        sigma = []

        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('Bước'):
                    parts = line.split('|')
                    buoc.append(int(parts[0].split(':')[0].split()[1]))
                    loi.append(int(parts[1].split(':')[1].strip().split()[0]))
                    conflicts.append(int(parts[2].split(':')[1].strip()))
                    thoi_gian.append(float(parts[3].split(':')[1].strip().split('s')[0]))
                    sigma.append(float(parts[4].split(':')[1].strip()))

        return {
            'buoc': buoc,
            'loi': loi,
            'conflicts': conflicts,
            'thoi_gian': thoi_gian,
            'sigma': sigma
        }

    log_data = phan_tich_log(log_path)
    if not log_data['buoc']:
        print("Không có dữ liệu log để vẽ.")
        return

    thoi_gian_tich_luy = np.cumsum(np.diff(log_data['thoi_gian'], prepend=0))
    avg_time_per_step = np.mean(np.diff(thoi_gian_tich_luy))
    std_time_per_step = np.std(np.diff(thoi_gian_tich_luy))

    plt.figure(figsize=(8 , 6))
    plt.suptitle('GIẢI SUDOKU VỚI SIMULATED ANEALING',
                fontsize=10, y=0.99, fontweight='bold')

    # Subplot 1: Tiến triển giải thuật
    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(log_data['buoc'], log_data['loi'], 'r-', label='Số lỗi', linewidth=2)
    ax1.plot(log_data['buoc'], log_data['conflicts'], 'b--', label='Số conflicts', linewidth=2)
    ax1.set_title('TIẾN TRIỂN GIẢI THUẬT', pad=5)
    ax1.set_xlabel('Số bước', fontsize=10)
    ax1.set_ylabel('Giá trị', fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper right')
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Subplot 2: Quá trình làm nguội
    ax2 = plt.subplot(2, 2, 2)
    ax2.plot(log_data['buoc'], log_data['sigma'], 'g-', linewidth=2)
    ax2.set_title('QUÁ TRÌNH LÀM NGUỘI (SIGMA)', pad=5)
    ax2.set_xlabel('Số bước', fontsize=10)
    ax2.set_ylabel('Giá trị sigma', fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Subplot 3: Thời gian tích lũy
    ax3 = plt.subplot(2, 2, 3)
    ax3.plot(log_data['buoc'], thoi_gian_tich_luy, 'm-o', markersize=4, linewidth=2)
    ax3.set_title('THỜI GIAN TÍCH LŨY', pad=5)
    ax3.set_xlabel('Số bước', fontsize=10)
    ax3.set_ylabel('Thời gian (giây)', fontsize=10)
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.text(0.02, 0.85,
            f'Thời gian/bước: {avg_time_per_step:.4f}s ± {std_time_per_step:.4f}s',
            transform=ax3.transAxes,
            bbox={'facecolor': 'white', 'alpha': 0.7, 'pad': 5})

    # Subplot 4: Quá trình giảm lỗi (log scale)
    ax4 = plt.subplot(2, 2, 4)
    ax4.semilogy(log_data['thoi_gian'], log_data['loi'], 'c-', linewidth=2)
    ax4.set_title('GIẢM LỖI THEO THỜI GIAN (LOG SCALE)', pad=5)
    ax4.set_xlabel('Thời gian (giây)', fontsize=10)
    ax4.set_ylabel('Số lỗi', fontsize=10)
    ax4.grid(True, which="both", linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92, hspace=0.3, wspace=0.25)
    plt.show()

def ve_bieu_do_phan_tich_hc(file_path):
    steps = []
    times = []
    rows = []
    cols = []
    values = []
    conflicts = []

    # Regex để bắt thông tin từ log dạng Hill Climbing
    pattern = r"(\d+):([\d.]+)s \| Conflicts: (\d+) \| \((\d+),(\d+)\) <- (\d+)"

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                step = int(match.group(1))
                time = float(match.group(2))
                conflict = int(match.group(3))
                row = int(match.group(4))
                col = int(match.group(5))
                value = int(match.group(6))

                steps.append(step)
                times.append(time)
                conflicts.append(conflict)
                rows.append(row)
                cols.append(col)
                values.append(value)

    # Vẽ 4 biểu đồ
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    fig.suptitle("PHÂN TÍCH GIẢI SUDOKU BẰNG HILL CLIMBING", fontsize=16, fontweight='bold')

    # 1. Thời gian theo bước
    axs[0, 0].plot(steps, times, marker='o', color='purple')
    axs[0, 0].set_title("Thời gian tích lũy theo bước")
    axs[0, 0].set_xlabel("Bước")
    axs[0, 0].set_ylabel("Thời gian (s)")
    axs[0, 0].grid(True)

    # 2. Vị trí các ô được gán
    sc = axs[0, 1].scatter(cols, rows, c=steps, cmap='viridis', s=100)
    axs[0, 1].invert_yaxis()
    axs[0, 1].set_title("Vị trí các ô được gán giá trị")
    axs[0, 1].set_xlabel("Cột")
    axs[0, 1].set_ylabel("Hàng")
    fig.colorbar(sc, ax=axs[0, 1], label="Bước")

    # 3. Heatmap giá trị đã gán
    grid = np.zeros((9, 9), dtype=int)
    for r, c, v in zip(rows, cols, values):
        grid[r][c] = v
    sns.heatmap(grid, annot=True, fmt='d', cmap='YlGnBu', cbar=False, ax=axs[1, 0])
    axs[1, 0].set_title("Lưới Sudoku sau các bước gán")

    # 4. Số xung đột theo bước
    axs[1, 1].plot(steps, conflicts, marker='o', color='red')
    axs[1, 1].set_title("Số xung đột theo bước")
    axs[1, 1].set_xlabel("Bước")
    axs[1, 1].set_ylabel("Số xung đột")
    axs[1, 1].grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
