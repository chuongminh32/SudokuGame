# Thuật Toán Leo Đồi (Hill Climbing)

## Tổng Quan
Thuật toán Leo Đồi được sử dụng để giải Sudoku bằng cách cải thiện trạng thái hiện tại theo từng bước, ưu tiên các thay đổi làm giảm số lượng xung đột.

## Mã Giả
### Hàm: `GET_SAFE_VALUES(board, n, row, col)`
- Tính căn bậc hai của `n` để xác định kích thước khối.
- Xác định hàng và cột bắt đầu của khối.
- Thu thập tất cả các số đã được sử dụng trong hàng, cột và khối.
- Trả về danh sách các số từ `1..n` không nằm trong tập đã sử dụng.

### Hàm: `COUNT_CONFLICTS(board, n)`
- Khởi tạo `conflicts` bằng 0.
- Với mỗi ô `(i, j)` trên bảng:
    - Nếu `board[i][j] == 0`, tăng `conflicts` (các ô trống được coi là xung đột).
- Đếm các giá trị trùng lặp trong hàng, cột và khối.
- Trả về tổng số xung đột.

### Hàm: `HILL_CLIMBING_CORE(board, size)`
- Khởi tạo:
    - `current_conflicts` ← `COUNT_CONFLICTS(board)`
    - `best_board` ← một bản sao của `board`
    - `steps` ← 0
- Lặp lại cho đến khi `current_conflicts == 0`:
    - Đặt `improved` thành `False`.
    - Với mỗi ô trống:
        - Lấy các giá trị hợp lệ bằng `GET_SAFE_VALUES()`.
        - Với mỗi giá trị hợp lệ:
            - Gán giá trị cho ô hiện tại.
            - Tính `new_conflicts`.
            - Nếu `new_conflicts <= current_conflicts`:
                - Cập nhật `best_board` và `current_conflicts`.
                - Đặt `improved` thành `True` và thoát vòng lặp.
            - Ngược lại, khôi phục giá trị ban đầu.
    - Nếu không có cải thiện, thoát vòng lặp.
- Trả về `best_board`, `steps`, và thời gian chạy.

### Hàm: `SOLVE_SUDOKU_HILL_CLIMBING(board)`
- Tạo một bản sao của bảng.
- Gọi `HILL_CLIMBING_CORE` để tìm giải pháp.
- Trả về giải pháp, số bước, và trạng thái hợp lệ.

## Giải Thích Từng Bước
1. **Xác Định Các Giá Trị Hợp Lệ (`GET_SAFE_VALUES`)**:
     - Kiểm tra các giá trị đã tồn tại trong hàng, cột và khối 3x3.
     - Trả về danh sách các số hợp lệ còn lại từ `1` đến `9`.

2. **Đánh Giá Chất Lượng Giải Pháp (`COUNT_CONFLICTS`)**:
     - Xung đột được định nghĩa là các số trùng lặp trong hàng, cột hoặc khối.
     - Các ô trống cũng được tính là xung đột để khuyến khích điền chúng.

3. **Thuật Toán Leo Đồi**:
     - Thay đổi một ô trống bằng một giá trị hợp lệ để giảm hoặc giữ nguyên số lượng xung đột.
     - Nếu không có cải thiện nào khả thi (cực trị địa phương), thuật toán dừng lại.
     - Kết quả là giải pháp tốt nhất được tìm thấy.

4. **Tích Hợp Với Giao Diện Người Dùng (`SOLVE_SUDOKU_HILL_CLIMBING`)**:
     - Hỗ trợ các callback để cập nhật giao diện từng bước.
     - Trả về giải pháp cuối cùng, số bước, và trạng thái hợp lệ.

5. **Ghi Nhật Trình (`LOG_HILL_CLIMBING`)**:
     - Tự động lưu toàn bộ quá trình giải vào `log_HC.txt`.
     - Hữu ích cho phân tích, thống kê, và trực quan hóa.

---

# Thuật Toán Làm Lạnh Mô Phỏng (Simulated Annealing) Để Giải Sudoku

## Tổng Quan
Làm Lạnh Mô Phỏng là một kỹ thuật tối ưu hóa lấy cảm hứng từ quá trình nung nóng và làm nguội vật liệu để tìm cấu hình tối ưu. Đối với Sudoku, nó giảm xung đột trên bảng cho đến khi tìm được giải pháp hợp lệ.

## Mã Giả
1. Đầu vào: Bảng Sudoku và kích thước `N` (thường là 9).
2. Xác định các ô cố định (các ô đã được điền trước).
3. Chia bảng thành các khối `n x n`.
4. Với mỗi khối:
     - Gán ngẫu nhiên các giá trị còn thiếu mà không trùng lặp trong khối.
5. Tính số lượng xung đột ban đầu (các giá trị trùng lặp trong hàng và cột).
6. Đặt nhiệt độ ban đầu (`sigma = 100`).
7. Trong khi chưa tìm được giải pháp và chưa vượt quá giới hạn bước/thời gian:
     - Chọn ngẫu nhiên một khối và hoán đổi hai ô không cố định.
     - Tính số lượng xung đột mới.
     - Nếu xung đột giảm, chấp nhận hoán đổi.
     - Nếu xung đột tăng, chấp nhận hoán đổi với xác suất `e^(-delta/sigma)`.
     - Gọi callback (nếu có) để cập nhật giao diện hoặc ghi nhật trình.
     - Giảm nhiệt độ bằng một hàm làm lạnh.
8. Trả về kết quả cuối cùng.

## Các Hàm Chính
| Hàm                          | Mô Tả                                                                          |
|------------------------------|---------------------------------------------------------------------------------|
| `create_blocks()`            | Tạo danh sách các khối `n x n` trong bảng Sudoku.                              |
| `mark_fixed_cells()`         | Trả về ma trận nhị phân đánh dấu các ô đã được điền trước không thể thay đổi.  |
| `fill_randomly_in_blocks()`  | Điền ngẫu nhiên các số còn thiếu trong mỗi khối để khởi tạo trạng thái hợp lệ. |
| `calculate_conflicts()`      | Đếm tổng số xung đột (các giá trị trùng lặp trong hàng và cột).                |
| `conflicting_cells()`        | Trả về danh sách các ô gây ra xung đột trên bảng.                             |
| `swap_in_block()`            | Chọn ngẫu nhiên một khối và hoán đổi hai ô không cố định.                      |
| `simulated_annealing_core()` | Vòng lặp chính của thuật toán, thực hiện hoán đổi, đánh giá xung đột, và làm lạnh nhiệt độ. |
| `solve_sudoku_simulated_annealing()` | Hàm giao diện để giải Sudoku, hỗ trợ các callback cho giao diện người dùng. |
| `log_simulated_annealing()`  | Ghi nhật trình quá trình giải từng bước vào `log_SA.txt` để kiểm tra và phân tích. |

---

# Thuật Toán Quay Lui Với MRV Để Giải Sudoku

## Tổng Quan
Thuật toán Quay Lui truyền thống lặp qua các ô trống và thử các giá trị hợp lệ. Khi kết hợp với chiến lược MRV (Giá Trị Còn Lại Ít Nhất), nó ưu tiên các ô có ít tùy chọn hợp lệ nhất, giảm không gian tìm kiếm và tăng tốc quá trình giải.

## Mã Giả
1. Khởi tạo các tập để theo dõi các giá trị trong hàng, cột, và khối.
2. Phân tích bảng Sudoku ban đầu:
     - Với mỗi ô đã được điền, thêm giá trị của nó vào các tập hàng, cột, và khối tương ứng.
3. Bắt đầu đệ quy:
     - Tìm ô trống có ít giá trị hợp lệ nhất (MRV).
     - Nếu không còn ô trống, bài toán đã được giải.
     - Nếu một ô không có tùy chọn hợp lệ, quay lui.
4. Với mỗi giá trị hợp lệ trong ô được chọn:
     - Gán giá trị cho bảng.
     - Cập nhật các tập hàng, cột, và khối.
     - Đệ quy cho bước tiếp theo.
     - Nếu thành công, trả về `True`.
     - Nếu thất bại, quay lui bằng cách xóa giá trị và cập nhật các tập.
5. Nếu không có giá trị hợp lệ nào hoạt động, trả về `False`.

## Các Hàm Chính
| Hàm                          | Mô Tả                                                                          |
|------------------------------|---------------------------------------------------------------------------------|
| `backtracking_core()`        | Hàm chính triển khai Quay Lui với MRV, theo dõi thời gian và số bước.         |
| `solve()`                    | Hàm đệ quy chính, chọn ô bằng MRV, thử giá trị, và quay lui.                  |
| `solve_sudoku_backtracking()`| Hàm giao diện cho tích hợp giao diện người dùng, hỗ trợ các callback để cập nhật. |
| `log_backtracking()`         | Ghi nhật trình quá trình giải vào `log_B.txt`, bao gồm từng bước, thành công, và thất bại. |

## MRV Là Gì?
MRV (Giá Trị Còn Lại Ít Nhất) là một chiến lược để chọn ô trống có ít tùy chọn hợp lệ nhất trước.
- Mục tiêu: Loại bỏ nhanh các nhánh không khả thi (ngõ cụt) và tìm giải pháp nhanh hơn.
- Nếu một ô không có tùy chọn hợp lệ, quay lui ngay lập tức.
- Heuristic này cải thiện đáng kể hiệu quả của thuật toán Quay Lui.
