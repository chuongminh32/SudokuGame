import logging
import json
import os

def setup_logger():
    # Tìm đường dẫn tuyệt đối đến thư mục gốc của dự án
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    config_path = os.path.join(project_root, 'config.json')

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file config.json tại {config_path}. Sử dụng cấu hình mặc định.")
        config = {"log_level": "INFO"}  # Cấu hình mặc định nếu không tìm thấy file

    logger = logging.getLogger('SudokuSolver')
    logger.setLevel(getattr(logging, config.get('log_level', 'INFO')))

    # Thêm handler để ghi log vào file
    handler = logging.FileHandler(os.path.join(project_root, 'sudoku_solver.log'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logger()