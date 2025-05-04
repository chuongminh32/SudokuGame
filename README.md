# Sudoku AI - Hill Climbing

##  Giới thiệu
Đây là một ứng dụng giải quyết bài toán Sudoku sử dụng thuật toán **Hill Climbing**. Chương trình cung cấp giao diện trực quan với **Pygame**, cho phép người dùng nhập bài toán, chọn mức độ khó và yêu cầu thuật toán giải tự động, chế độ riêng ai để phân tích 

* ALG 
1. Mục tiêu
Sử dụng thuật toán tối ưu cục bộ Hill-Climbing để giải bài toán Sudoku 9x9 — một bài toán ràng buộc cổ điển, đòi hỏi mỗi hàng, cột và vùng 3x3 đều chứa các số từ 1 đến 9, không lặp.

2. Ý tưởng chính
Thay vì tìm lời giải bằng cách thử tất cả khả năng, Hill-Climbing bắt đầu từ một lời giải hợp lệ về mặt cấu trúc (đầy đủ các số trong từng block) và dần dần cải thiện nó bằng các phép hoán đổi thông minh, nhằm giảm số lượng lỗi trong hàng và cột.
Tối ưu hóa trên không gian bị ràng buộc:
Giữ nguyên các ô gốc.
Chỉ cho phép hoán đổi giá trị trong cùng block 3x3 để bảo toàn tính hợp lệ block.
Từ đó, tìm lời giải hợp lệ toàn cục bằng cách tối thiểu hóa số lỗi (xung đột).

3. Cách tiếp cận
Khởi tạo lời giải khả thi:
Mỗi block 3x3 được điền ngẫu nhiên nhưng đảm bảo không trùng số bên trong.
Hàm đánh giá (Heuristic):
Đếm số lần trùng số trong các hàng và cột (conflict count).
Tạo lân cận:
Chọn 2 ô có thể hoán đổi trong cùng block.
Đánh giá lại nghiệm mới.
Leo dốc (Hill-Climbing):
Di chuyển sang trạng thái lân cận tốt nhất.

Nếu không có trạng thái tốt hơn → mắc kẹt → kết thúc hoặc khởi động lại.

##  Tính năng chính
* chế độ chơi 
-  Tạo đề Sudoku ngẫu nhiên với 3 mức độ: **Dễ, Trung bình, Khó**.
- Hỗ trợ nhập số vào bảng Sudoku.
- Sử dụng **Hill Climbing, SA,..** để tìm lời giải cho Sudoku.
- Hiển thị lời giải trực tiếp lên giao diện đồ họa.
- Cho phép xóa bảng và chọn lại bài toán mới.
* chế độ AI (đang thực hiện)
- xem tiến trình giải, chọn thuật toán - cấp độ, thời gian, so sánh lời giải với các thuật toán,.. 

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
|   |   |    utils_game_screen.py  # Các hàm hỗ trợ cho game screen diện
|   |   |
|   +---tests  # Thư mục chứa các bài kiểm thử
|       |    test_solver.py  # Kiểm thử thuật toán giải Sudoku
|       |--- test_sudoku.py  # Kiểm thử lớp Sudoku
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
