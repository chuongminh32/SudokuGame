# Sudoku AI - Hill Climbing

##  Giới thiệu
Đây là một ứng dụng giải quyết bài toán Sudoku sử dụng thuật toán **Hill Climbing**. Chương trình cung cấp giao diện trực quan với **Pygame**, cho phép người dùng có thể chơi game sudoku 9x9 ở chế độ chơi game; đọc hướng dẫn; Nhập bài toán, chọn mức độ khó và yêu cầu thuật toán giải tự động trong chế độ ai để phân tích 

##  Tính năng chính
* Chế độ chơi game
- Người chơi có thể chơi game, sử dụng gợi ý hoặc giải ngay nếu muốn
- Chương trình sẽ mặc định lấy thuật toán Backtrackiing để giải (đảm bảo giải được tất cả mực độ 9x9) 
- Có thể chọn đề Sudoku 9x9 ngẫu nhiên với 3 mức độ: **Dễ, Trung bình, Khó**.
- Hỗ trợ nhập số vào bảng Sudoku.
- Cho phép xóa bảng và chọn lại bài toán mới.
* chế độ AI 
- Chọn thuật toán, cấp độ, kích thước bảng sudoku, đề sudoku theo cấp độ ngẫu nhiên
- Xem log giải thuật - có thể điều chỉnh thời gian delay -> xem rõ tiến trình giải, biểu đồ phân tích giải thuật
- Xem thông tin giải thuật sudoku: thời gian + số bước thử giá trị vào bảng
- xem tiến trình giải, chọn thuật toán - cấp độ, thời gian, kích thước bảng sudoku
- Có thể tự tạo đề sudoku cho thuật toán giải 

## 🛠 Công nghệ sử dụng
- Python 3.12
- Pygame
- NumPy

##  Cấu trúc thư mục
```
README.md
|----requirements.txt  # Danh sách thư viện cần thiết
|----.gitignore  # Bỏ qua tệp không cần thiết khi commit
|---assets  # Chứa hình ảnh, icon, v.v.
|---data  # Chứa dữ liệu log giải thuật, đề + giải sudoku
|----main.py  # Điểm bắt đầu để chạy chương trình
+---src  # Thư mục chứa mã nguồn chính
|   |   
|   +---algorithm  # Chứa các thuật toán giải sudoku
|   |   |   __init__.py  # Đánh dấu thư mục là module
|   |   |   backtracking.py  
|   |   |   hill_climbing.py  
|   |   |   generate_sudoku.py  # Sinh đề bài Sudoku
|   |   |   simulated_anealing.py  
|   |   |
|   +---gui  # Chứa các thành phần giao diện
|   |   |   __init__.py  # Đánh dấu thư mục là module
|   |   |   home_screen.py  # Màn hình chính của game
|   |   |   game_screen.py  # Màn hình chơi game Sudoku
|   |   |   tutorial_screen.py  # Màn hình hướng dẫn game 
|   |   |-- ai_screen.py  # Màn hình ai chơi game 
|   |   |
|   +---utils  # Chứa các hàm tiện ích dùng chung 
|   |   |    utils_ai_screen.py  # Các hàm hỗ trợ cho ai screen  
|   |   |    utils_game_screen.py  # Các hàm hỗ trợ cho game screen
|   |   |
|   +---tests  # Thư mục chứa các bài kiểm thử
|       |    
|       |--- test_B.py  # Kiểm thử thuật toán Backtracking giải Sudoku
|       |--- test_HC.py  # Kiểm thử thuật toán Hill_Climbing giải Sudoku
|       |--- test_SA.py  # Kiểm thử thuật toán Simulated_Anealing giải Sudoku
|
|
+---docs  # Tài liệu dự án
        usage_guide.md  # Hướng dẫn sử dụng
        algorithm.md  # Giải thích thuật toán



##  Cách cài đặt và chạy chương trình
### 1️ Cài đặt môi trường
Trước tiên, cài đặt Python 3.12 và các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2️ Chạy chương trình
```bash
python src/gui.py
```

## 👥 Thành viên và phân công công việc
| **Phạm Hàn Minh Chương (Giao diện)** | Xây dựng UI với Pygame | - Phát triển màn hình chính, menu, game, kết quả trong `gui/`.  <br> - Viết code để vẽ Sudoku lên màn hình. <br> - Xử lý sự kiện người chơi (chuột, bàn phím).- Viết tài liệu hướng dẫn (`docs/`).  |
| **Nguyễn Thanh Bình Minh(Thuật toán & Logic)** | Cài đặt thuật toán Hill-Climbing | - Viết `hill_climbing.py` để giải Sudoku. <br> - Cải tiến thuật toán để tối ưu hiệu suất. <br> - Xây dựng `solver.py` để điều phối thuật toán. |
| **Nguyễn Thị Thanh Thùy (Kiểm thử, tài liệu, tối ưu)** | Viết test case & tối ưu code | - Viết thêm 1 số thuật toán bổ trợ và so sánh : "SA", "Backtracking",.. Tạo `tests/` để kiểm thử Sudoku & thuật toán. <br> - Viết log & ghi lỗi (logger.py). <br> - Cải thiện tốc độ thuật toán & UI. <br> |
