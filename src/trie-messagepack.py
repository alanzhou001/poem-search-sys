import json
import msgpack
from collections import defaultdict
from PageRank import build_co_occurrence_graph

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_poem = False
        self.pagerank_score = 0

    def to_dict(self):
        return {
            'children': {char: child.to_dict() for char, child in self.children.items()},
            'is_end_of_poem': self.is_end_of_poem,
            'pagerank_score': self.pagerank_score
        }

    @staticmethod
    def from_dict(data):
        node = TrieNode()
        node.children = defaultdict(TrieNode, {char: TrieNode.from_dict(child) for char, child in data['children'].items()})
        node.is_end_of_poem = data['is_end_of_poem']
        node.pagerank_score = data['pagerank_score']
        return node

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, poem, pagerank_scores):
        node = self.root
        for char in poem:
            node = node.children[char]
            node.pagerank_score = pagerank_scores.get(char, 0)
        node.is_end_of_poem = True

    def to_dict(self):
        return self.root.to_dict()

# 读取 JSON 文件
file_path = r"D:\introAI\小组作业\db\processed\poem_database_with_pagerank.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 获取 "poem_database"
poem_database = data["poem_database"]

# 构建共现图并计算 PageRank 分数
pagerank_scores = build_co_occurrence_graph(poem_database)

# 构建 Trie 树
trie = Trie()
for poem in poem_database:
    trie.insert(poem, pagerank_scores)

# 将 Trie 树保存到文件（使用 MessagePack）
trie_dict = trie.to_dict()
output_file_path = r"D:\introAI\小组作业\db\processed\trie_tree_with_pagerank.msgpack"
with open(output_file_path, "wb") as f:
    msgpack.pack(trie_dict, f)

print("已生成 Trie 树文件")