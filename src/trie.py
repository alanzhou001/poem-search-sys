# FILE: trie.py
import msgpack
from collections import defaultdict

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
    def __init__(self, root=None):
        self.root = root if root else TrieNode()

    def insert(self, poem, pagerank_scores):
        node = self.root
        for char in poem:
            node = node.children[char]
            node.pagerank_score = pagerank_scores.get(char, 0)
        node.is_end_of_poem = True

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
        file_path = f"D:\\poem-search-sys\\db\\processed\\trie_tree_{char}.msgpack"
        with open(file_path, "rb") as f:
            subtree_dict = msgpack.unpack(f)
        self.root.children[char] = TrieNode.from_dict(subtree_dict)