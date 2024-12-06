import json

# 读取 JSON 文件
file_path = r"D:\introAI\小组作业\db\processed\poem_database_with_pagerank.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 获取 "poem_database" 并进行去重
poem_database = data["poem_database"]
unique_poem_database = list(set(poem_database))

# 更新数据
data["poem_database"] = unique_poem_database

# 写回 JSON 文件
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("已对 poem_database 进行去重")