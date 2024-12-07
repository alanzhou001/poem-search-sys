import msgpack
import logging
import os
from collections import defaultdict
from utils import setup_logger, load_config
from trie import Trie, TrieNode
from opencc import OpenCC

# 初始化 OpenCC 转换器
cc_to_traditional = OpenCC('s2t')  # 简体到繁体
cc_to_simplified = OpenCC('t2s')  # 繁体到简体

# 主程序：进行诗句检索
def main():
    config = load_config()
    log_dir = config["log_directory"]
    logger = setup_logger(log_dir)
    
    input_chars = ["春", "平", "野", "松", "雄", "草", "宅", "綠", "石"]
    target_length = config["retrieval_target_length"]

    # 将输入字符转换为繁体
    input_chars_traditional = [cc_to_traditional.convert(char) for char in input_chars]
    
    logger.info("开始加载 Trie 树...")
    trie = Trie()

    # 按需加载 Trie 树的子树
    for char in input_chars_traditional:
        trie.load_subtree(char)

    logger.info("Trie 树加载完成，开始检索...")

    # 对输入字符进行排序，按每个字符的最高 PageRank 分数排序
    input_chars_traditional.sort(key=lambda char: -trie.root.children[char].pagerank_score if char in trie.root.children else 0)

    results = trie.search(input_chars_traditional, target_length)
    if results:
        results.sort(key=lambda x: -x[1])  # 按 PageRank 分数排序
        for result, score in results:
            # 将结果转换为简体
            result_simplified = cc_to_simplified.convert(result)
            logger.info(f"找到诗句：{result_simplified}，评分：{score}")
    else:
        logger.info("未找到符合条件的诗句")

if __name__ == "__main__":
    main()