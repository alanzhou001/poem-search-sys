import msgpack
import logging
import os
from collections import defaultdict
from utils import setup_logger, load_config
from opencc import OpenCC

# 初始化 OpenCC 转换器
cc_to_traditional = OpenCC('s2t')  # 简体到繁体
cc_to_simplified = OpenCC('t2s')  # 繁体到简体

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_poem = False
        self.pagerank_score = 0

    @staticmethod
    def from_dict(data):
        node = TrieNode()
        node.children = defaultdict(TrieNode, {char: TrieNode.from_dict(child) for char, child in data['children'].items()})
        node.is_end_of_poem = data['is_end_of_poem']
        node.pagerank_score = data['pagerank_score']
        return node

class Trie:
    def __init__(self, root=None):
        self.root = root if root else TrieNode()

    def search(self, input_chars, target_length):
        results = []
        self._dfs(self.root, "", input_chars, target_length, results)
        return results

    def _dfs(self, node, path, input_chars, target_length, results):
        if len(path) == target_length:
            if node.is_end_of_poem:
                results.append((path, node.pagerank_score))
            return
        for char in sorted(input_chars, key=lambda c: -node.children[c].pagerank_score if c in node.children else 0):
            if char in node.children:
                self._dfs(node.children[char], path + char, input_chars, target_length, results)

    def load_subtree(self, char):
        file_path = f"D:\\introAI\\小组作业\\db\\processed\\trie_tree_{char}.msgpack"
        with open(file_path, "rb") as f:
            subtree_dict = msgpack.unpack(f)
        self.root.children[char] = TrieNode.from_dict(subtree_dict)

# 主程序：进行诗句检索
def main():
    config = load_config()
    log_dir = config["log_directory"]
    logger = setup_logger(log_dir)
    
    input_chars = ["平", "春", "野", "松", "雄", "草", "宅", "綠", "石"]
    target_length = config["retrieval_target_length"]

    # 将输入字符转换为繁体
    input_chars_traditional = [cc_to_traditional.convert(char) for char in input_chars]
    
    logger.info("开始加载 Trie 树...")
    trie = Trie()

    # 按需加载 Trie 树的子树
    for char in input_chars_traditional:
        trie.load_subtree(char)

    logger.info("Trie 树加载完成，开始检索...")

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