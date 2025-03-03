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
|   requirements.txt  # Danh sách thư viện cần thiết
|
+---data  # Chứa dữ liệu liên quan (nếu có)
|
+---src  # Thư mục chứa mã nguồn chính
|   |   gui.py  # Giao diện đồ họa sử dụng Pygame
|   |   hill_climbing.py  # Triển khai thuật toán Hill Climbing
|   |   main.py  # Điểm bắt đầu để chạy chương trình
|   |   solver.py  # Hàm điều phối giải thuật Sudoku
|   |   sudoku.py  # Lớp Sudoku để tạo và kiểm tra bảng
|   |
|   \---__pycache__  # Tệp bytecode được tạo bởi Python
|           gui.cpython-312.pyc
|           hill_climbing.cpython-312.pyc
|           solver.cpython-312.pyc
|           sudoku.cpython-312.pyc
|
\---tests  # Thư mục chứa các bài kiểm thử
        test_solver.py  # Kiểm thử thuật toán giải Sudoku
```


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
| STT |        Họ và Tên       | Công việc                                              |
|-----|-----------|------------|--------------------------------------------------------|
|  1  | Nguyễn Thị Thanh Thùy  | Phát triển thuật toán Hill Climbing & Xử lý dữ liệu    |
|  2  |  Phạm Hàn Minh Chương  | Xây dựng giao diện đồ họa với Pygame                   |
|  3  | Nguyễn Thanh Bình Minh | Xây dựng hệ thống Sudoku và kết nối GUI với thuật toán |
