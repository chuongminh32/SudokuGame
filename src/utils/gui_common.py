import random 
import pygame, sys, os, math 
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.algorithm.backtracking import solve_sudoku 
RONG, CAO, DEM, KT_LUOI = 700, 750, 60, 9
KT_O = (RONG - 2 * DEM) // KT_LUOI 
CAO_NUT, KC_NUT = 40, 20 
TRANG, DEN, XAM, XAM_SANG = (255,255,255), (0,0,0), (200,200,200), (220,220,220) 
XANH_DUONG, DO, XANH_LA = (0,0,255), (255,0,0), (0,128,0)
MAU_NUT, MAU_CHU_NUT = (90, 123, 192), TRANG
MAU_NEN_NUT_HOVER = (67, 99, 167)
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
    text_goi_y = font.render("Gợi ý", True, MAU_CHU_NUT)  # Vẽ chữ "Gợi ý"
    screen.blit(text_goi_y, text_goi_y.get_rect(center=nut_goi_y.center))  # Căn giữa chữ trong nút

    # Nút Làm mới
    nut_lam_moi = pygame.Rect(DEM + w_nut + KC_NUT, y_nut, w_nut, CAO_NUT)
    pygame.draw.rect(screen, MAU_NUT, nut_lam_moi, border_radius=8)
    text_lam_moi = font.render("Làm mới", True, MAU_CHU_NUT)
    screen.blit(text_lam_moi, text_lam_moi.get_rect(center=nut_lam_moi.center))

    # Nút AI giải
    nut_ai = pygame.Rect(DEM + 2 * (w_nut + KC_NUT), y_nut, w_nut, CAO_NUT)
    pygame.draw.rect(screen, MAU_NUT, nut_ai, border_radius=8)
    text_ai = font.render("AI giải", True, MAU_CHU_NUT)
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



def ve_highlight_cho_o(screen, row, col, grid):

    sr = (row // 3) * 3  # Xác định hàng đầu của ô 3x3
    sc = (col // 3) * 3  # Xác định cột đầu của ô 3x3

    gia_tri_o_dang_duoc_chon = grid[row][col]

    # Rect(x, y, w, h)
    # x : trai -> phai : dùng cho col 
    # Tô màu highlight cho hàng và cột
    for i in range(KT_LUOI):  # Duyệt theo hàng (row)
        pygame.draw.rect(screen, (226, 235, 243), pygame.Rect(
            DEM + i * KT_O,  # Cột thay đổi, x tăng dần 
            DEM + row * KT_O,  # Hàng giữ nguyên, y không đổi 
            KT_O, KT_O
        ))

    for j in range(KT_LUOI):  # Duyệt theo cột (column)
        pygame.draw.rect(screen, (226, 235, 243), pygame.Rect(
            DEM + col * KT_O,  # Cột giữ nguyên
            DEM + j * KT_O,  # Hàng thay đổi
            KT_O, KT_O
        ))

    # Tô màu cho ô 3x3 chứa ô đang chọn
    for i in range(3):
        for j in range(3):  
            ar = sr + i  # ar = actual_row(dòng chính xác tính từ vị trí chỉ số), sr = start_row    
            ac = sc + j
         
            pygame.draw.rect(screen, (226, 235, 243), pygame.Rect(
                DEM + ac * KT_O,  
                DEM + ar * KT_O,  
                KT_O, KT_O
            ))  

    # Tô tất cả ô cùng giá trị 
    if gia_tri_o_dang_duoc_chon == 0:
         pygame.draw.rect(screen, (187, 222, 251), pygame.Rect(DEM + col* KT_O, DEM + row* KT_O, KT_O, KT_O))
    else:
        for r in range(KT_LUOI):
            for c in range(KT_LUOI):
                if (grid[r][c] == gia_tri_o_dang_duoc_chon):
                    pygame.draw.rect(screen, (187, 222, 251), pygame.Rect(DEM + c* KT_O, DEM + r * KT_O, KT_O, KT_O))


def buocDiHopLe(board, row, col, num):
    """Trả về T/F  nếu đặt số `num` vào vị trí `(row, col) khong hop le`"""
    if num == 0:
      return True
    # Kiểm tra hàng
    for i in range(9):
        if board[row][i] == num and i != col:
            return False

    # Kiểm tra cột
    for i in range(9):
        if board[i][col] == num and i != row:
           return False

    # Xác định góc trên trái của ô 3x3
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)

    # Kiểm tra ô 3x3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num and (i, j) != (row, col):
                return False

    return True  # Trả về danh sách các ô sai


def viTriHopLe(board, row, col, num):
    """Trả về danh sách các ô bị lỗi nếu đặt số `num` vào vị trí `(row, col)`"""
    if num == 0:
        return []  # Ô trống luôn hợp lệ
    
    ds_o_loi = []  # Danh sách ô bị lỗi

    # Kiểm tra hàng
    for i in range(9):
        if board[row][i] == num and i != col:
            ds_o_loi.append((row, i))

    # Kiểm tra cột
    for i in range(9):
        if board[i][col] == num and i != row:
            ds_o_loi.append((i, col))

    # Xác định góc trên trái của ô 3x3
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)

    # Kiểm tra ô 3x3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num and (i, j) != (row, col):
                ds_o_loi.append((i, j))

    return ds_o_loi  # Trả về danh sách các ô sai

# Vẽ icon gợi ý, so goi y, so loi  
def ve_icon_goi_y(screen, font, soGoiY, soLoi):

    # Hiển thị gợi ý 
    goi_y_text = font.render(f"Gợi ý: {soGoiY}", True, DEN)
    screen.blit(goi_y_text, (RONG - 430, 20))

    # Hiển thị lỗi 
    loi_sai = font.render(f"Số lỗi: {soLoi}/5", True, DEN)
    screen.blit(loi_sai, (RONG - 600, 20))

    icon_color = (255, 215, 0)  # Màu vàng sáng cho biểu tượng gợi ý

    # Vẽ phần bóng đèn tròn (hình tròn)
    pygame.draw.circle(screen, icon_color, (RONG - 445, 30), 10)  

    # Vẽ phần đế của bóng đèn (hình chữ nhật)
    pygame.draw.rect(screen, icon_color, (RONG - 450, 40, 10, 5))

    # Vẽ tia sáng (3 tia)
    pygame.draw.line(screen, icon_color, (RONG - 445, 15), (RONG - 445, 5), 2)
    pygame.draw.line(screen, icon_color, (RONG - 455, 20), (RONG - 465, 15), 2)
    pygame.draw.line(screen, icon_color, (RONG - 435, 20), (RONG - 425, 15), 2)

# Hiển thị tg đang chơi 
def hienThiTGChoi(screen, tg_da_troi, font):
    phut = int(tg_da_troi) // 60
    giay = int(tg_da_troi) % 60
    thoi_gian_text = font.render(f"{phut:02}:{giay:02}", True, DEN) 
    screen.blit(thoi_gian_text, (RONG - 250, 20)) 

# Vẽ icon pause/play  
def ve_icon_pause(screen, is_paused):
    """Vẽ nút Pause/Play trên màn hình"""
    MAU_NUT = (200, 200, 200)  # Màu nền của nút
    icon_color = (50, 50, 50)  # Màu biểu tượng Pause/Play
    button_rect = pygame.Rect(RONG - 310, 10, 55, 40)  # Vị trí và kích thước của nút
    
    pygame.draw.rect(screen, MAU_NUT, button_rect, border_radius=10)  # Vẽ hình chữ nhật
    
    if is_paused:
        # Nếu đang ở trạng thái tạm dừng -> vẽ biểu tượng "Play" (hình tam giác) top(x,y) - bottom(x,y) - right(x,y)
        pygame.draw.polygon(screen, icon_color, [(RONG - 290   , 20), (RONG - 290, 40), (RONG - 270, 30)])
    else:
        # Nếu đang ở trạng thái chơi -> vẽ biểu tượng "Pause" (hai đường thẳng đứng)
        pygame.draw.rect(screen, icon_color, (RONG - 295, 20, 8, 20))
        pygame.draw.rect(screen, icon_color, (RONG - 280, 20, 8, 20))
    
    return button_rect  # Trả về rect để kiểm tra sự kiện click

