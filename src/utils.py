import logging
import json
import os

# 设置日志记录
def setup_logger(log_dir, log_file_name):
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(log_file_name)
    logger.setLevel(logging.INFO)
    
    # 检查是否已经存在相同的处理器
    if not logger.handlers:
        file_handler = logging.FileHandler(os.path.join(log_dir, log_file_name))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

# 加载配置文件
def load_config(config_path="config/config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config