from fetch_char import fetch_poem_characters
from trie_retrieval import search_poems

def main():
    # 获取汉字列表
    input_chars = fetch_poem_characters()
    
    # 调用诗句检索函数
    results = search_poems(input_chars)
    
    # 显示结果
    print("\n" + "="*40)
    print("\033[1;32m" + "检索结果：" + "\033[0m")
    if results:
        for result, score in results:
            print(f"\033[1;34m找到诗句：{result}，评分：{score}\033[0m")
    else:
        print("\033[1;31m未找到符合条件的诗句\033[0m")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()