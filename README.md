# Sudoku Game

## Giới thiệu
Đây là một ứng dụng giải quyết bài toán Sudoku sử dụng thuật toán **Hill Climbing**. Chương trình cung cấp giao diện trực quan với **Pygame**, cho phép người dùng chơi game Sudoku 9x9 ở chế độ chơi game; đọc hướng dẫn; nhập bài toán, chọn mức độ khó và yêu cầu thuật toán giải tự động trong chế độ AI để phân tích.

## Tính năng chính
### Chế độ chơi game
- Người chơi có thể chơi game, sử dụng gợi ý hoặc giải ngay nếu muốn.
- Chương trình mặc định sử dụng thuật toán Backtracking để giải (đảm bảo giải được tất cả các mức độ 9x9).
- Có thể chọn đề Sudoku 9x9 ngẫu nhiên với 3 mức độ: **Dễ, Trung bình, Khó**.
- Hỗ trợ nhập số vào bảng Sudoku.
- Cho phép xóa bảng và chọn lại bài toán mới.

### Chế độ AI
- Chọn thuật toán, cấp độ, kích thước bảng Sudoku, và đề Sudoku theo cấp độ ngẫu nhiên.
- Xem log giải thuật - có thể điều chỉnh thời gian delay để theo dõi rõ tiến trình giải và biểu đồ phân tích giải thuật.
- Xem thông tin giải thuật Sudoku: thời gian + số bước thử giá trị vào bảng.
- Theo dõi tiến trình giải, chọn thuật toán, cấp độ, thời gian, và kích thước bảng Sudoku.
- Có thể tự tạo đề Sudoku để thuật toán giải.

## 🛠 Công nghệ sử dụng
- Python 3.12
- Pygame
- NumPy
- Seaborn
- Matplotlib

## Cấu trúc thư mục dự án
```
\SudokuGame
|
+---- data  # Chứa dữ liệu log giải thuật, đề + giải Sudoku
|      |--- log_B.txt  # log chạy Backtracking giải Sudoku
|      |--- log_HC.txt  # log chạy Hill Climbing giải Sudoku
|      |--- log_SA.txt  # log chạy Simulated Anealing giải Sudoku
|      |--- sudoku_4x4_dataset.json  # file json chứa đề và lời giải 4x4 
|      |--- sudoku_9x9_dataset.json  # file json chứa đề và lời giải 9x9 
|      |--- sudoku_16x16_dataset.json  # file json chứa đề và lời giải 16x16 
|      |--- sudoku_25x25_dataset.json  # file json chứa đề và lời giải 25x25 
|
+---docs  # Tài liệu dự án
|      |--- usage_guide.md  # Hướng dẫn sử dụng
|      |--- algorithm.md  # Giải thích thuật toán
|     
+---src  # Thư mục chứa mã nguồn chính
|   |   
|   +---algorithm  # Chứa các thuật toán giải Sudoku
|   |   |   __init__.py  # Đánh dấu thư mục là module
|   |   |   backtracking.py  
|   |   |   hill_climbing.py  
|   |   |   generate_sudoku.py  # Sinh đề bài Sudoku
|   |   |   simulated_annealing.py  
|   |   |
|   |   |
|   +---assets  # Chứa ảnh/icon 
|   |   |
|   |   |
|   +---gui  # Chứa các thành phần giao diện
|   |   |   
|   |   |+-- generate_gui  # Thư mục chứa các file sinh giao diện 
|   |   |----- gen_ai_screen.py  # Sinh giao diện (vẽ nút, lưới,...) -> trang AI
|   |   |----- gen_game_screen.py  # Sinh giao diện (vẽ nút, lưới,...) -> trang chơi game
|   |   |
|   |   |+-- manage_gui  # Thư mục chứa các file quản lý giao diện 
|   |   |----- ai_screen.py  # Quản lý giao diện AI
|   |   |----- game_screen.py  # Quản lý giao diện chơi game
|   |   |----- home_screen.py  # Quản lý giao diện trang chủ
|   |   |----- tutorial_screen.py  # Quản lý giao diện hướng dẫn
|   |   
|   +---tests  # Thư mục chứa các bài kiểm thử
|       |    
|       |--- test_backtracking.py  # Kiểm thử thuật toán Backtracking giải Sudoku
|       |--- test_hill_climbing.py  # Kiểm thử thuật toán Hill Climbing giải Sudoku
|       |--- test_simulated_annealing.py  # Kiểm thử thuật toán Simulated Annealing giải Sudoku
|       
|----.gitignore  # Bỏ qua tệp không cần thiết khi commit
|---- main.py  # Điểm bắt đầu để chạy chương trình
|---- README.md # File hướng dẫn + giới thiệu dự án
|---- requirements.txt  # Danh sách thư viện cần thiết

```

## Cách cài đặt và chạy chương trình
### 1. Cài đặt môi trường
Trước tiên, cài đặt Python 3.12 và các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2. Chạy chương trình
```bash
python src/gui.py
```

## 👥 Thành viên và phân công công việc
| **Phạm Hàn Minh Chương (Giao diện, quản lý)** | Xây dựng UI với Pygame | - Phát triển màn hình chính, menu, game, kết quả trong `gui/`. <br> - Viết code để vẽ Sudoku lên màn hình. <br> - Xử lý sự kiện người chơi (chuột, bàn phím). <br> - Viết tài liệu hướng dẫn (`docs/`). |
| **Nguyễn Thanh Bình Minh (Thuật toán & Logic, Kiểm thử )** | Cài đặt thuật toán Hill Climbing | - Viết `hill_climbing.py` để giải Sudoku. <br> - Cải tiến thuật toán để tối ưu hiệu suất. <br> - Xây dựng `solver.py` để điều phối thuật toán. |
| **Nguyễn Thị Thanh Thùy (Thuật toán, Kiểm thử, tài liệu, tối ưu)** | Viết test case & tối ưu code | - Viết thêm một số thuật toán bổ trợ và so sánh: "Simulated Annealing", "Backtracking",... <br> - Tạo `tests/` để kiểm thử Sudoku & thuật toán. <br> - Viết log & ghi lỗi (`logger.py`). <br> - Cải thiện tốc độ thuật toán & UI. |
