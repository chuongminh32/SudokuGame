import pygame, sys, os
import matplotlib.pyplot as plt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RONG, CAO, DEM, KT_LUOI = 700, 750, 60, 9
KT_O = (RONG - 2 * DEM) // KT_LUOI 
CAO_NUT, KC_NUT = 40, 20 
TRANG, DEN, XAM, XAM_SANG = (255,255,255), (0,0,0), (200,200,200), (220,220,220) 
XANH_DUONG, DO, XANH_LA = (0,0,255), (255,0,0), (0,128,0)
MAU_NUT, MAU_CHU_NUT, MAU_NEN = (90, 123, 192), TRANG, TRANG
MAU_NEN_NUT_HOVER = (67, 99, 167)
# Màu nút và chữ trên nút
MAU_NUT_BACK, MAU_ICON_BACK = (100, 100, 255), (80, 80, 80)  # Màu nút quay lại và biểu tượng
MAU_NUT_CAIDAT, MAU_KHI_DUOC_CHON = (60, 60, 60), (180, 230, 255)  # Màu biểu tượng cài đặt và tùy chọn được chọn
KT_NUT_BACK, DEM_NUT_BACK_x, DEM_NUT_BACK_y = 40, 20, 20  # Kích thước và vị trí của biểu tượng quay lại
KT_NUT_CAIDAT, DEM_NUT_CAIDAT = 37, 10  # Kích thước và khoảng cách của biểu tượng cài đặt

# Tạo đường dẫn tương đối từ thư mục này
def get_relative_path(*paths):
    return os.path.join(BASE_DIR, *paths)

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((RONG, CAO))
    pygame.display.set_caption("Trò chơi Sudoku")
    return screen 

def ve_nut_ai(screen):
    # Tính toán vị trí của các nút
    y_nut = DEM + KT_LUOI * KT_O + KC_NUT  # Vị trí y cho các nút
    w_nut = (RONG - 2 * DEM - 2 * KC_NUT) // 3  # Chiều rộng của mỗi nút, chia đều 3 nút

    font_size = 24  # Cỡ chữ cho các nút
    font = pygame.font.SysFont("verdana", font_size)

    # nút so sánh 
    icon_ss_path = get_relative_path("..", "assets", "icons8-compare-50.png")
    icon_ss = pygame.image.load(icon_ss_path).convert_alpha()
    x = RONG - 160
    y = CAO - 90
    rect_nut_ss = icon_ss.get_rect(topleft=(x, y))
    screen.blit(icon_ss, rect_nut_ss)

    # nút làm mới
    icon_ss_path = get_relative_path("..", "assets", "icons8-refresh-48.png")
    icon_lam_moi = pygame.image.load(icon_ss_path).convert_alpha()
    x = 120
    y = CAO - 90
    rect_nut_lam_moi = icon_lam_moi.get_rect(topleft=(x, y))
    screen.blit(icon_lam_moi, rect_nut_lam_moi)

    # nut back 
    icon_ss_path = get_relative_path("..", "assets", "icons8-go-back-48.png")
    icon_back = pygame.image.load(icon_ss_path).convert_alpha()
    # Vị trí icon
    x = 12
    y = 15
    # Lấy rect từ icon và đặt vị trí
    rect_nut_back = icon_back.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_back, rect_nut_back)

    # nut chart 
    icon_chart_path = get_relative_path("..", "assets", "chart.png")
    icon_chart = pygame.image.load(icon_chart_path).convert_alpha()
    icon_chart = pygame.transform.scale(icon_chart, (40, 40))
    # Vị trí icon
    x = RONG - 230
    y = 15
    # Lấy rect từ icon và đặt vị trí
    rect_btn_chart = icon_chart.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_chart, rect_btn_chart)

    # nut tao de bai 
    icon_create_topic = get_relative_path("..", "assets", "icons8-plus-50.png")
    icon_topic = pygame.image.load(icon_create_topic).convert_alpha()
    # Vị trí icon
    x = RONG - 300
    y = 12
    # Lấy rect từ icon và đặt vị trí
    rect_nut_tao_de_bai = icon_topic.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_topic, rect_nut_tao_de_bai)

    # nut info 
    icon_info = get_relative_path("..", "assets", "info.png")
    icon_if = pygame.image.load(icon_info).convert_alpha()
    # Vị trí icon
    x = RONG - 370
    y = 12
    # Lấy rect từ icon và đặt vị trí
    rect_nut_thong_tin = icon_if.get_rect(topleft=(x, y))
    # Vẽ icon lên màn hình
    screen.blit(icon_if, rect_nut_thong_tin)

    # Nút AI giải
    nut_ai = pygame.Rect(DEM + w_nut + KC_NUT, y_nut, w_nut, CAO_NUT)
    pygame.draw.rect(screen, MAU_NUT, nut_ai, border_radius=8)
    text_lam_moi = font.render("Giải", True, MAU_CHU_NUT)
    screen.blit(text_lam_moi, text_lam_moi.get_rect(center=nut_ai.center))

    return rect_nut_ss, rect_nut_lam_moi, nut_ai, rect_nut_back, rect_btn_chart, rect_nut_tao_de_bai, rect_nut_thong_tin


def to_o_giai(screen, bang_goc, bang_giai, font):
    for i in range(KT_LUOI):
        for j in range(KT_LUOI):
            if bang_giai[i][j] != 0 and bang_goc[i][j] == 0:  # Kiểm tra ô có giá trị trong bảng giải nhưng không có trong bảng ban đầu
                # Vẽ hình chữ nhật với màu để tô ô
                pygame.draw.rect(
                    screen,
                    (204, 255, 229),  # Màu xanh nhạt (hoặc màu bạn muốn)
                    (DEM + j * KT_O + 1, DEM + i * KT_O + 1, KT_O - 2, KT_O - 2)  # Tô trong ô
                )


def ve_so_ai(screen, bang, font):
    for i in range(KT_LUOI):
        for j in range(KT_LUOI):
            if bang[i][j]:
                # Xác định màu chữ
                mau = (25, 53, 88)
                # Vẽ số
                text = font.render(str(bang[i][j]), True, mau)
                rect = text.get_rect(center=(DEM + j * KT_O + KT_O // 2, DEM + i * KT_O + KT_O // 2))
                screen.blit(text, rect)


def ve_luoi(screen):
    # Vẽ lưới Sudoku
    for i in range(KT_LUOI + 1):
        duongVien = 3 if i % 3 == 0 else 1
        # Vẽ đường dọc
        pygame.draw.line(screen, DEN, (DEM + i * KT_O, DEM), (DEM + i * KT_O, DEM + 9 * KT_O), duongVien)
        # Vẽ đường ngang
        pygame.draw.line(screen, DEN, (DEM, DEM + i * KT_O), (DEM + 9 * KT_O, DEM + i * KT_O), duongVien)

    # Trả về hình chữ nhật bao quanh toàn bộ lưới để kiểm tra click ở ngoài
    return pygame.Rect(DEM, DEM, KT_O * 9, KT_O * 9)

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


def ve_highlight_cho_o(screen, row, col, grid):

    sr = (row // 3) * 3  # Xác định hàng đầu của ô 3x3
    sc = (col // 3) * 3  # Xác định cột đầu của ô 3x3

    gia_tri_o_dang_duoc_chon = grid[row][col]

    # Rect(x, y, w, h)
    # x : trai -> phai : dùng cho col 
    # Tô màu highlight cho hàng và cột
    for i in range(KT_LUOI):  # Duyệt theo hàng (row)
        pygame.draw.rect(screen, (150, 190, 228), pygame.Rect(
            DEM + i * KT_O,  # Cột thay đổi, x tăng dần 
            DEM + row * KT_O,  # Hàng giữ nguyên, y không đổi 
            KT_O, KT_O
        ))

    for j in range(KT_LUOI):  # Duyệt theo cột (column)
        pygame.draw.rect(screen, (150, 190, 228), pygame.Rect(
            DEM + col * KT_O,  # Cột giữ nguyên
            DEM + j * KT_O,  # Hàng thay đổi
            KT_O, KT_O
        ))

    # Tô màu cho ô 3x3 chứa ô đang chọn
    for i in range(3):
        for j in range(3):  
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
        for r in range(KT_LUOI):
            for c in range(KT_LUOI):
                if (grid[r][c] == gia_tri_o_dang_duoc_chon):
                    pygame.draw.rect(screen, (187, 222, 251), pygame.Rect(DEM + c* KT_O, DEM + r * KT_O, KT_O, KT_O))

def ve_thong_bao_giai_xong(screen, RONG, CAO, tg_giai, ten_alg, so_buoc):
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
    font = pygame.font.SysFont("verdana", 28)
    font_sub = pygame.font.SysFont("verdana", 20)
    text = font.render("Đã giải thành công!", True, (52, 72, 97))
    text_sub = font_sub.render(f"Thuật toán sử dụng: {ten_alg}", True, (148, 163, 183))
    screen.blit(text, (box_x + 105, box_y + 20))
    screen.blit(text_sub, (box_x + 100, box_y + 70))

    # Tính giây và mili giây
    time_text = f"Thời gian giải: {tg_giai:.6f} (giây)"
    step = f"Tổng số bước thử: {so_buoc}(bước)"


    # Vẽ thời gian
    font_time = pygame.font.SysFont("verdana", 18)
    time_render = font_time.render(time_text, True, (52, 72, 97))
    screen.blit(time_render, (box_x + 100, box_y + 100))

    # Vẽ số bước 
    font_step = pygame.font.SysFont("verdana", 18)
    step_render = font_step.render(step, True, (52, 72, 97))
    screen.blit(step_render, (box_x + 100, box_y + 130))

    # Vẽ nút "Thoát" ở giữa
    btn_width, btn_height = 150, 50
    btn_x = box_x + (box_rong - btn_width) // 2  # Căn giữa
    btn_y = box_y + 170
    thoat_btn = pygame.draw.rect(screen, (90, 123, 192),
                                 pygame.Rect(btn_x, btn_y, btn_width, btn_height), border_radius=10)

    text = font.render("Thoát", True, (255, 255, 255))
    screen.blit(text, (btn_x + 30, btn_y + 5))

    return thoat_btn




# _____________________vẽ biểu đồ ____________________________________
# Vẽ menu chọn loại biểu đồ (thời gian, số bước, log)
def ve_bang_chon_bieu_do(screen, x, y):
    font = pygame.font.SysFont("verdana", 18)  # Khởi tạo font chữ
    w, h = 180, 35  # Kích thước của mỗi ô menu
    options = [  # Danh sách các tùy chọn biểu đồ
        {"text": "Biểu đồ thời gian", "value": "TIME"},
        {"text": "Biểu đồ số bước", "value": "STEP"},
        {"text": "Log theo bước", "value": "LOG"},
    ]
    ds_rect = []  # Danh sách lưu vùng chọn (rect) tương ứng từng tùy chọn
    for i, opt in enumerate(options):
        rect = pygame.Rect(x, y + i * h, w, h)  # Tạo hình chữ nhật cho mỗi tùy chọn
        pygame.draw.rect(screen, (230, 230, 230), rect)  # Tô màu nền ô
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Vẽ viền ô
        text = font.render(opt["text"], True, (0, 0, 0))  # Vẽ nội dung chữ
        screen.blit(text, (x + 10, y + i * h + 5))  # Hiển thị chữ lên màn hình
        ds_rect.append({"rect": rect, "text": opt["text"], "value": opt["value"]})  # Lưu thông tin tùy chọn
    return ds_rect  # Trả về danh sách các ô tùy chọn đã vẽ
def ve_bieu_do_thoi_gian(ds_log):
    if not ds_log:  # Nếu không có dữ liệu log thì thoát
        return
    buoc = [b[0] for b in ds_log]  # Danh sách các bước
    thoi_gian = [b[1] - ds_log[0][1] for b in ds_log]  # Thời gian trôi qua từ bước đầu
    plt.plot(buoc, thoi_gian, marker='o')  # Vẽ biểu đồ đường
    plt.title("Thời gian theo bước")  # Tiêu đề
    plt.xlabel("Bước")  # Nhãn trục X
    plt.ylabel("Thời gian (s)")  # Nhãn trục Y
    plt.grid()  # Hiển thị lưới
    plt.show()  # Hiển thị biểu đồ