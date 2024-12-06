import json

# 读取 JSON 文件
file_path = r"D:\introAI\小组作业\db\processed\poem_database_with_pagerank.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 获取 "poem_database" 并进行分割
poem_database = data["poem_database"]
split_poem_database = []
for poem in poem_database:
    # 按照 '，' 和 '。' 分割
    lines = poem.replace('，', '。').split('。')
    split_poem_database.extend(lines)

# 去除空字符串
split_poem_database = [line for line in split_poem_database if line]

# 更新数据
data["poem_database"] = split_poem_database

# 写回 JSON 文件
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("已对 poem_database 进行分割和去除空字符串")