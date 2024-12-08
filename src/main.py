from fetch_char import fetch_poem_characters
from trie_retrieval import search_poems

def main():
    # 获取汉字列表
    input_chars = fetch_poem_characters()
    
    # 调用诗句检索函数
    search_poems(input_chars)

if __name__ == "__main__":
    main()