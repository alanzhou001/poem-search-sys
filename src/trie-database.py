import json
import msgpack
import os
from collections import defaultdict
from tqdm import tqdm
from trie import Trie, TrieNode
from PageRank import build_co_occurrence_graph
from utils import setup_logger, load_config

# 读取配置文件
config = load_config()
log_dir = config["log_directory"]

# 设置日志记录器
logger = setup_logger(log_dir, "trie_build.log")

# 读取 JSON 文件
file_path = config["poem_database_path"]
logger.info("开始读取 JSON 文件...")
with tqdm(total=1, desc="读取 JSON 文件") as pbar:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    pbar.update(1)
logger.info("JSON 文件读取完成")

# 获取 "poem_database"
logger.info("开始获取 'poem_database'...")
with tqdm(total=1, desc="获取 'poem_database'") as pbar:
    poem_database = data["poem_database"]
    pbar.update(1)
logger.info("'poem_database' 获取完成")

# 构建共现图并计算 PageRank 分数
logger.info("开始构建共现图并计算 PageRank 分数...")
with tqdm(total=1, desc="构建共现图并计算 PageRank 分数") as pbar:
    pagerank_scores = build_co_occurrence_graph(poem_database)
    pbar.update(1)
logger.info("共现图构建完成，PageRank 分数计算完成")

# 构建 Trie 树并按首个字分割
logger.info("开始构建 Trie 树...")
trie = Trie()
for poem in tqdm(poem_database, desc="插入诗句到 Trie 树"):
    trie.insert(poem, pagerank_scores)
logger.info("Trie 树构建完成")

# 将 Trie 树按首个字分割并保存到多个文件
logger.info("开始将 Trie 树按首个字分割并保存到多个文件...")
root_dict = trie.to_dict()
with tqdm(total=len(root_dict['children']), desc="保存 Trie 子树到文件") as pbar:
    for char, subtree in root_dict['children'].items():
        # 使用字符的 Unicode 编码作为文件名的一部分
        char_code = ord(char)
        output_file_path = f"D:\\introAI\\小组作业\\db\\processed\\trie_tree_{char_code}.msgpack"
        with open(output_file_path, "wb") as f:
            msgpack.pack(subtree, f)
        logger.info(f"Trie 子树保存到文件: {output_file_path}")
        pbar.update(1)

logger.info("已生成 Trie 树文件")