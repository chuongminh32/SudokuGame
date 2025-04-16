
import sys, os , pygame, time 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.algorithm.generate_sudoku import *
from src.utils.utils_ai_screen import *

# trả về bảng giải 
def giai_sudoku_backtracking(bang):
    def hop_le(bang, row, col, num):
        for i in range(9):
            if bang[row][i] == num or bang[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if bang[i][j] == num:
                    return False

        return True

    def solve(bang):
        for row in range(9):
            for col in range(9):
                if bang[row][col] == 0:
                    for num in range(1, 10):
                        if hop_le(bang, row, col, num):
                            bang[row][col] = num
                            if solve(bang):
                                return True
                            bang[row][col] = 0 # quay lui nếu k tìm được lời giải hợp lệ 
                    return False
        return True

    bang_copy = [row[:] for row in bang]  # Sao chép để không sửa bảng gốc
    solve(bang_copy)
    return bang_copy

def giai_sudoku_backtracking_visual(bang, cap_nhat_gui=None, delay=0.05):
    import time

    # Hàm kiểm tra tính hợp lệ của giá trị
    def hop_le(bang, row, col, num):
        for i in range(9):
            if bang[row][i] == num or bang[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if bang[i][j] == num:
                    return False
        return True

    # Hàm giải quyết bảng sudoku bằng thuật toán backtracking
    so_buoc = 0  # Biến đếm số bước thử
    o_sai = []  # Xóa danh sách ô sai cũ
    o_dung = [] # Xóa danh sách ô đúng cũ

    def solve(bang):
        nonlocal so_buoc
        for row in range(9):
            for col in range(9):
                if bang[row][col] == 0:  # Nếu ô trống
                    for num in range(1, 10):
                        if hop_le(bang, row, col, num):  # Kiểm tra xem số có hợp lệ không
                            bang[row][col] = num
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, num, "thu", so_buoc)  # Cập nhật GUI nếu có
                                time.sleep(delay)

                            so_buoc += 1  # Tăng số bước thử

                            if solve(bang):
                                if cap_nhat_gui:
                                    cap_nhat_gui(row, col, num, "dung", so_buoc)
                                return True

                            # Nếu không thành công, quay lại (backtrack)
                            bang[row][col] = 0
                            if cap_nhat_gui:
                                cap_nhat_gui(row, col, 0, "sai", so_buoc)
                                time.sleep(delay)
                    return False
        return True

    bang_copy = [row[:] for row in bang]
    solve(bang_copy)

    return bang_copy  # Trả về bảng đã giải và số bước thử




# def giai_sudoku_backtracking_visual(screen, bang, cap_nhat_gui=None, delay=0.05):

#     def hop_le(bang, row, col, num):
#         # Kiểm tra trùng lặp trong cùng hàng
#         for i in range(9):
#             if bang[row][i] == num:
#                 return False  # Nếu có giá trị trùng thì không hợp lệ

#         # Kiểm tra trùng lặp trong cùng cột
#         for i in range(9):
#             if bang[i][col] == num:
#                 return False  # Nếu có giá trị trùng thì không hợp lệ

#         # Kiểm tra trùng lặp trong cùng vùng 3x3
#         start_row, start_col = 3 * (row // 3), 3 * (col // 3)
#         for i in range(start_row, start_row + 3):
#             for j in range(start_col, start_col + 3):
#                 if bang[i][j] == num:
#                     return False  # Nếu có giá trị trùng thì không hợp lệ

#         return True
#     so_buoc = 0
#     def solve(bang):
#         nonlocal so_buoc
#         for row in range(9):
#             for col in range(9):
#                 if bang[row][col] == 0:
#                     for num in range(1, 10):
#                         if hop_le(bang, row, col, num):
#                             bang[row][col] = num
#                             if cap_nhat_gui:
#                                 cap_nhat_gui(row, col, num, "thu",so_buoc)
#                                 time.sleep(delay)
#                                 so_buoc += 1  # Tăng số bước thử

#                             if solve(bang):
#                                 if cap_nhat_gui:
#                                     cap_nhat_gui(row, col, num, "dung",so_buoc)
#                                 return True

#                             bang[row][col] = 0
#                             if cap_nhat_gui:
#                                 cap_nhat_gui(row, col, 0, "sai",so_buoc)
#                                 time.sleep(delay)
#                     return False
#         return True

#     # Bắt đầu giải và theo dõi thời gian
#     bang_copy = [row[:] for row in bang]
#     solve(bang_copy)

#     # Vẽ biểu đồ hiển thị tổng số bước và thời gian trên giao diện Pygame
#     def ve_bieu_do():
#         # Vẽ thanh biểu đồ cho số bước thử
#         pygame.draw.rect(screen, (173, 216, 230), pygame.Rect(RONG + 20, 200, 200, 20))  # Thanh nền
#         pygame.draw.rect(screen, (70, 130, 180), pygame.Rect(RONG + 20, 200, so_buoc * 20, 20))  # Thanh bước thử

#         # Vẽ thanh biểu đồ cho thời gian
#         pygame.draw.rect(screen, (173, 216, 230), pygame.Rect(RONG + 20, 250, 200, 20))  # Thanh nền
#         pygame.draw.rect(screen, (60, 179, 113), pygame.Rect(RONG + 20, 250, thoi_gian * 20, 20))  # Thanh thời gian

#         # Hiển thị thông số
#         font = pygame.font.SysFont("Verdana", 20)
#         text_steps = font.render(f"Số bước thử: {cnt}", True, DEN)
#         screen.blit(text_steps, (RONG + 20, 180))

#         text_time = font.render(f"Thời gian (s): {thoi_gian:.2f}", True, DEN)
#         screen.blit(text_time, (RONG + 20, 230))

#         pygame.display.update()

#     # Gọi hàm vẽ biểu đồ
#     ve_bieu_do()

#     return bang_copy