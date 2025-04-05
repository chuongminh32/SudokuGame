import random 

import pygame, sys, os, math 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.algorithm.backtracking import solve_sudoku 
RONG, CAO, DEM, KT_LUOI = 700, 750, 60, 9
KT_O = (RONG - 2 * DEM) // KT_LUOI 
CAO_NUT, KC_NUT = 40, 20 
TRANG, DEN, XAM, XAM_SANG = (255,255,255), (0,0,0), (200,200,200), (220,220,220) 
XANH_DUONG, DO, XANH_LA = (0,0,255), (255,0,0), (0,128,0)
MAU_NUT, MAU_CHU_NUT = (50, 150, 250), TRANG
# Màu nút và chữ trên nút
MAU_NUT_BACK, MAU_ICON_BACK = (100, 100, 255), (80, 80, 80)  # Màu nút quay lại và biểu tượng
MAU_NUT_CAIDAT, MAU_KHI_DUOC_CHON = (60, 60, 60), (180, 230, 255)  # Màu biểu tượng cài đặt và tùy chọn được chọn
KT_NUT_BACK, DEM_NUT_BACK_x, DEM_NUT_BACK_y = 40, 20, 20  # Kích thước và vị trí của biểu tượng quay lại
KT_NUT_CAIDAT, DEM_NUT_CAIDAT = 37, 10  # Kích thước và khoảng cách của biểu tượng cài đặt

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((RONG, CAO))
    pygame.display.set_caption("Trò chơi Sudoku")
    return screen 

def ve_so(screen, board, board_original, font):
        for i in range(KT_LUOI):
            for j in range(KT_LUOI):
                if board[i][j]:
                    color = (25, 53, 88) if board_original[i][j] else DEN
                    text = font.render(str(board[i][j]), True, color)
                    rect = text.get_rect(center=(DEM + j * KT_O + KT_O // 2, 
                                               DEM + i * KT_O + KT_O // 2))
                    screen.blit(text, rect)
def ve_nut(screen):
    # Tính toán vị trí của các nút
    y_nut = DEM + KT_LUOI * KT_O + KC_NUT  # Vị trí y cho các nút
    w_nut = (RONG - 2 * DEM - 2 * KC_NUT) // 3  # Chiều rộng của mỗi nút, chia đều 3 nút

    font_size = 24  # Cỡ chữ cho các nút
    font = pygame.font.SysFont("verdana", font_size)

    # Nút Gợi ý
    nut_goi_y = pygame.Rect(DEM, y_nut, w_nut, CAO_NUT)  # Vị trí và kích thước của nút
    pygame.draw.rect(screen, MAU_NUT, nut_goi_y, border_radius=8)  # Vẽ nút với màu nền và bo tròn
    text_goi_y = font.render("Gợi ý", True, TRANG)  # Vẽ chữ "Gợi ý"
    screen.blit(text_goi_y, text_goi_y.get_rect(center=nut_goi_y.center))  # Căn giữa chữ trong nút

    # Nút Làm mới
    nut_lam_moi = pygame.Rect(DEM + w_nut + KC_NUT, y_nut, w_nut, CAO_NUT)
    pygame.draw.rect(screen, DO, nut_lam_moi, border_radius=8)
    text_lam_moi = font.render("Làm mới", True, TRANG)
    screen.blit(text_lam_moi, text_lam_moi.get_rect(center=nut_lam_moi.center))

    # Nút AI giải
    nut_ai = pygame.Rect(DEM + 2 * (w_nut + KC_NUT), y_nut, w_nut, CAO_NUT)
    pygame.draw.rect(screen, XANH_LA, nut_ai, border_radius=8)
    text_ai = font.render("AI giải", True, TRANG)
    screen.blit(text_ai, text_ai.get_rect(center=nut_ai.center))

    # Nút Back (mũi tên trái)
    x_b, y_b = DEM_NUT_BACK_x, DEM_NUT_BACK_y
    nut_back = pygame.Rect(x_b, y_b, KT_NUT_BACK, KT_NUT_BACK)

    # Vẽ mũi tên trái '<' không có nền
    arrow_points = [
        (x_b + KT_NUT_BACK * 0.65, y_b + KT_NUT_BACK * 0.3),  # Điểm trên của mũi tên
        (x_b + KT_NUT_BACK * 0.35, y_b + KT_NUT_BACK * 0.5),  # Điểm giữa của mũi tên
        (x_b + KT_NUT_BACK * 0.65, y_b + KT_NUT_BACK * 0.7)   # Điểm dưới của mũi tên
    ]
    pygame.draw.polygon(screen, DEN, arrow_points)  # Vẽ mũi tên màu trắng

    return nut_goi_y, nut_lam_moi, nut_ai, nut_back

def ve_so(screen, bang, bang_goc, font):
    for i in range(KT_LUOI):
        for j in range(KT_LUOI):
            if bang[i][j]:
                mau = (25,53,88) if bang_goc[i][j] else DEN # Màu xanh cho số gốc, màu đen cho số người chơi nhập
                text = font.render(str(bang[i][j]), True, mau) # Tạo đối tượng văn bản số
                rect = text.get_rect(center=(DEM + j * KT_O + KT_O // 2, DEM + i * KT_O + KT_O // 2))
                screen.blit(text, rect) # Tạo hình chữ nhật bao quanh số

def ve_luoi(screen):  # Vẽ lưới Sudoku
    for i in range(KT_LUOI + 1):  # Duyệt qua tất cả các đường
        duongVien = 3 if i % 3 == 0 else 1  # Đường viền dày hơn cho mỗi khối 3x3
        pygame.draw.line(screen, DEN, (DEM + i * KT_O, DEM), (DEM + i * KT_O, DEM + 9 * KT_O), duongVien)  # Vẽ đường dọc
        pygame.draw.line(screen, DEN, (DEM, DEM + i * KT_O), (DEM + 9 * KT_O, DEM + i * KT_O), duongVien)  # Vẽ đường ngang



def sinh_bang_giai_sudoku():
    """Tạo một bảng Sudoku hoàn chỉnh."""
    base = 3  # Kích thước của khu vực 3x3 (tức là Sudoku 9x9)
    side = base * base  # Tổng số hàng và cột là 9

    # Hàm này tính toán vị trí của mỗi số trong bảng Sudoku
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # Hàm xáo trộn các danh sách, giúp tạo ra sự ngẫu nhiên
    def shuffle(s):
        return random.sample(s, len(s))  # Trả về danh sách xáo trộn ngẫu nhiên

    r_base = range(base)  # Dãy số từ 0 đến base-1 (từ 0 đến 2)
    
    # Tạo danh sách các hàng và cột ngẫu nhiên dựa trên các số từ r_base
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]

    # Xáo trộn các số từ 1 đến 9 để sử dụng trong bảng
    nums = shuffle(range(1, side + 1))

    # Tạo bảng Sudoku hoàn chỉnh bằng cách áp dụng hàm pattern cho từng hàng, cột
    sudoku = []
    for r in rows:
        sudoku_row = []
        for c in cols:
            sudoku_row.append(nums[pattern(r, c)])  # Sắp xếp các số vào bảng
        sudoku.append(sudoku_row)

    return sudoku


def singNgauNhienBangSudoKu():
    """Tạo một bảng Sudoku hoàn chỉnh."""
    base = 3  # Kích thước của khu vực 3x3 (tức là Sudoku 9x9)
    side = base * base  # Tổng số hàng và cột là 9

    # Hàm này tính toán vị trí của mỗi số trong bảng Sudoku
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # Hàm xáo trộn các danh sách, giúp tạo ra sự ngẫu nhiên
    def shuffle(s):
        return random.sample(s, len(s))  # Trả về danh sách xáo trộn ngẫu nhiên

    r_base = range(base)  # Dãy số từ 0 đến base-1 (từ 0 đến 2)
    
    # Tạo danh sách các hàng và cột ngẫu nhiên dựa trên các số từ r_base
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]

    # Xáo trộn các số từ 1 đến 9 để sử dụng trong bảng
    nums = shuffle(range(1, side + 1))

    # Tạo bảng Sudoku hoàn chỉnh bằng cách áp dụng hàm pattern cho từng hàng, cột
    sudoku = []
    for r in rows:
        sudoku_row = []
        for c in cols:
            sudoku_row.append(nums[pattern(r, c)])  # Sắp xếp các số vào bảng
        sudoku.append(sudoku_row)

    return sudoku


# phan chia cấp ____________
def xoaSoNgauNhien(board, num_to_remove):
    """Xóa một số lượng ô khỏi bảng Sudoku."""
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    board_copy = [row[:] for row in board]  # Tạo bản sao tránh sửa bảng gốc
    
    for _ in range(num_to_remove):
        row, col = positions.pop()
        board_copy[row][col] = 0
    
    return board_copy

def layBangSuDoKuTheoCapDo(level="easy"):
    """Tạo bảng Sudoku theo cấp độ."""
    bangDaGiai = singNgauNhienBangSudoKu()

    CapDo = {
        "easy": 20,
        "medium": 30,
        "hard": 40,
    }
    
    if level not in CapDo:
        raise ValueError("Cấp độ không hợp lệ. Chọn 'easy', 'medium', 'hard'.")

    return xoaSoNgauNhien(bangDaGiai, CapDo[level])

def ve_nut_phan_chia_cap_do(screen, ten_cap_do):
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
        {"text": "Dễ", "value": "easy", "rect": pygame.Rect(box_x + 23, box_y + 40, 150, 40)},
        {"text": "Trung bình", "value": "medium", "rect": pygame.Rect(box_x + 23, box_y + 90, 150, 40)},
        {"text": "Khó", "value": "hard", "rect": pygame.Rect(box_x + 23, box_y + 140, 150, 40)},
    ]
    
    font = pygame.font.SysFont("verdana", 20)

    # Vẽ bảng trắng
    pygame.draw.rect(screen, TRANG, pygame.Rect(box_x, box_y, box_rong, box_cao), border_radius=10)

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
        
    return bang_cap_do
# phân chia cấp ______________


def draw_mode_submenu(screen, small_font, selected_mode):  # Vẽ menu phụ chọn cấp độ
    submenu_rect = pygame.Rect(RONG - 550, KT_NUT_CAIDAT + DEM_NUT_CAIDAT * 2 + 60, 250, 180)  # Tạo hình chữ nhật cho menu phụ
    pygame.draw.rect(screen, TRANG, submenu_rect, border_radius=10)  # Vẽ nền trắng cho menu phụ
    pygame.draw.rect(screen, XAM, submenu_rect, 2, border_radius=10)  # Vẽ viền xám cho menu phụ
    screen.blit(small_font.render("Chọn cấp độ", True, DEN), 
                (submenu_rect.centerx - small_font.size("Chọn cấp độ")[0] // 2, submenu_rect.y + 10))  # Vẽ tiêu đề menu phụ

    difficulty_options = [{"text": "Dễ", "value": "easy", "y_offset": 60}, 
                          {"text": "Trung bình", "value": "medium", "y_offset": 100}, 
                          {"text": "Khó", "value": "hard", "y_offset": 140}]  # Định nghĩa các tùy chọn cấp độ
    option_rects = []  # Danh sách để lưu thông tin về các tùy chọn
    for option in difficulty_options:
        option_rect = pygame.Rect(submenu_rect.x + 10, submenu_rect.y + option["y_offset"] - 15, submenu_rect.RONG - 20, 30)  # Tạo hình chữ nhật cho mỗi tùy chọn
        pygame.draw.rect(screen, MAU_KHI_DUOC_CHON if option["value"] == selected_mode else XAM_SANG, option_rect, border_radius=5)  # Vẽ nền cho tùy chọn
        screen.blit(small_font.render(option["text"], True, DEN), 
                    (option_rect.centerx - small_font.size(option["text"])[0] // 2, option_rect.centery - small_font.size(option["text"])[1] // 2))  # Vẽ văn bản
        option_rects.append({"rect": option_rect, "value": option["value"]})  # Thêm thông tin về tùy chọn vào danh sách
    return option_rects  # Trả về danh sách thông tin về các tùy chọn


