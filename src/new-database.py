import json
from collections import defaultdict
from tqdm import tqdm
from PageRank import build_co_occurrence_graph

# 读取 JSON 文件
file_path = r"D:\introAI\小组作业\db\processed\poem_database_with_pagerank.json"
with tqdm(total=1, desc="读取 JSON 文件") as pbar:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    pbar.update(1)

# 获取 "poem_database"
with tqdm(total=1, desc="获取 'poem_database'") as pbar:
    poem_database = data["poem_database"]
    pbar.update(1)

# 构建共现图并计算 PageRank 分数
with tqdm(total=1, desc="构建共现图并计算 PageRank 分数") as pbar:
    pagerank_scores = build_co_occurrence_graph(poem_database)
    pbar.update(1)

# 构建每个字后面可能出现的字及其 PageRank 分数
char_followers = defaultdict(lambda: defaultdict(float))
with tqdm(poem_database, desc="处理诗句") as pbar:
    for poem in pbar:
        for i in range(len(poem) - 1):
            char = poem[i]
            next_char = poem[i + 1]
            char_followers[char][next_char] += pagerank_scores.get(next_char, 0)

# 将 defaultdict 转换为字典
char_followers = {char: dict(followers) for char, followers in char_followers.items()}

# 将结果写回 JSON 文件
output_data = {
    "poem_database": poem_database,
    "pagerank_scores": pagerank_scores,
    "char_followers": char_followers
}

with tqdm(total=1, desc="写回 JSON 文件") as pbar:
    output_file_path = r"D:\introAI\小组作业\db\processed\poem_database_with_followers.json"
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    pbar.update(1)

print("已生成可检索的数据集")