import logging
import json

# 设置日志记录
def setup_logger(log_dir):
    logger = logging.getLogger('poetry_retrieval')
    logger.setLevel(logging.INFO)
    
    # 检查是否已经存在相同的处理器
    if not logger.handlers:
        file_handler = logging.FileHandler(f"{log_dir}/retrieval.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# 加载配置文件
def load_config(config_path="config/config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config