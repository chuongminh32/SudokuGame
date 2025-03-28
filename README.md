# Sudoku AI - Hill Climbing

## 📌 Giới thiệu
Đây là một ứng dụng giải quyết bài toán Sudoku sử dụng thuật toán **Hill Climbing**. Chương trình cung cấp giao diện trực quan với **Pygame**, cho phép người dùng nhập bài toán, chọn mức độ khó và yêu cầu thuật toán giải tự động.

## 🚀 Tính năng chính
- Tạo đề Sudoku ngẫu nhiên với 3 mức độ: **Dễ, Trung bình, Khó**.
- Hỗ trợ nhập số vào bảng Sudoku.
- Sử dụng **Hill Climbing** để tìm lời giải cho Sudoku.
- Hiển thị lời giải trực tiếp lên giao diện đồ họa.
- Cho phép xóa bảng và chọn lại bài toán mới.

## 🛠 Công nghệ sử dụng
- Python 3.12
- Pygame
- NumPy

## 📂 Cấu trúc thư mục
```
README.md
|----requirements.txt  # Danh sách thư viện cần thiết
|----config.json  # Cấu hình tham số (tùy chọn)
|----.gitignore  # Bỏ qua tệp không cần thiết khi commit
|
+---assets  # Chứa hình ảnh, icon, v.v.
|
+---data  # Chứa dữ liệu liên quan (nếu có)
|
+---src  # Thư mục chứa mã nguồn chính
|   |   main.py  # Điểm bắt đầu để chạy chương trình
|   |   
|   +---algorithm  # Chứa các thuật toán giải sudoku
|   |   |   __init__.py  # Đánh dấu thư mục là module
|   |   |   backtracking.py  
|   |   |   hill_climbing.py  
|   |   |   generate_sudoku.py  # Sinh đề bài Sudoku
|   |   |-- solve.py  # Quản lý thuật toán (gọi backtracking hoặc hill_climbing)
|   |   |
|   +---gui  # Chứa các thành phần giao diện
|   |   |   __init__.py  # Đánh dấu thư mục là module
|   |   |   home_screen.py  # Màn hình chính của game
|   |   |   game_screen.py  # Màn hình chơi game Sudoku
|   |   |   tutorial_screen.py  # Màn hình hướng dẫn game 
|   |   |-- ai_screen.py  # Màn hình ai chơi game 
|   |   |
|   +---utils  # Chứa các hàm tiện ích dùng chung
|   |   |    gui_common.py  # Các hàm hỗ trợ chung cho giao diện: chức năng, vẽ,..
|   |   |
|   +---tests  # Thư mục chứa các bài kiểm thử
|       |    test_solver.py  # Kiểm thử thuật toán giải Sudoku
|       |--- test_sudoku.py  # Kiểm thử lớp Sudoku
|
|
+---docs  # Tài liệu dự án
        usage_guide.md  # Hướng dẫn sử dụng
        algorithm.md  # Giải thích thuật toán



## 🔧 Cách cài đặt và chạy chương trình
### 1️⃣ Cài đặt môi trường
Trước tiên, cài đặt Python 3.12 và các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2️⃣ Chạy chương trình
```bash
python src/gui.py
```

## 👥 Thành viên và phân công công việc
| **Phạm Hàn Minh Chương (Giao diện)** | Xây dựng UI với Pygame | - Phát triển màn hình chính, menu, game, kết quả trong `gui/`.  <br> - Viết code để vẽ Sudoku lên màn hình. <br> - Xử lý sự kiện người chơi (chuột, bàn phím). |
| **Nguyễn Thanh Bình Minh(Thuật toán & Logic)** | Cài đặt thuật toán Hill-Climbing | - Viết `hill_climbing.py` để giải Sudoku. <br> - Cải tiến thuật toán để tối ưu hiệu suất. <br> - Xây dựng `solver.py` để điều phối thuật toán. |
| **Nguyễn Thị Thanh Thùy (Kiểm thử, tài liệu, tối ưu)** | Viết test case & tối ưu code | - Tạo `tests/` để kiểm thử Sudoku & thuật toán. <br> - Viết log & ghi lỗi (logger.py). <br> - Cải thiện tốc độ thuật toán & UI. <br> - Viết tài liệu hướng dẫn (`docs/`). |
