import os
import json
import re
from tqdm import tqdm
from collections import defaultdict
from PageRank import build_co_occurrence_graph
from utils import setup_logger, load_config

# 使用正则表达式提取 JSON 文件中的诗句
def extract_paragraphs_from_json(file_content):
    paragraphs = []
    matches = re.findall(r'"paragraphs":\s*\[(.*?)\]', file_content, re.DOTALL)
    for match in matches:
        lines = re.findall(r'"(.*?)"', match)
        for line in lines:
            cleaned_line = re.sub(r'\(.*?\)', '', line)
            cleaned_line = "".join(cleaned_line.split())
            paragraphs.append(cleaned_line)
    return paragraphs

# 加载诗句库
def load_poems_from_files(poem_directory):
    poem_database = []
    for dirpath, _, filenames in os.walk(poem_directory):
        json_files = [f for f in filenames if f.endswith(".json")]
        for filename in tqdm(json_files, desc="加载诗句文件"):
            with open(os.path.join(dirpath, filename), "r", encoding="utf-8") as f:
                try:
                    file_content = f.read()
                    paragraphs = extract_paragraphs_from_json(file_content)
                    poem_database.extend(paragraphs)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")
                except ValueError as e:
                    print(f"Error processing poem in file {filename}: {e}")
    return poem_database


# 构建并保存数据库
def build_and_save_database(poem_directory, output_file):
    poem_database = load_poems_from_files(poem_directory)
    pagerank_scores = build_co_occurrence_graph(tqdm(poem_database, desc="构建 PageRank"))

    # 保存数据库
    database = {
        "poem_database": poem_database,
        "pagerank_scores": pagerank_scores
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=4)
    print(f"数据库已保存到 {output_file}")


if __name__ == "__main__":
    config = load_config()
    log_dir = config["log_directory"]
    logger = setup_logger(log_dir)
    logger.info("开始构建数据库...")

    poem_directory = config["raw_poem_directory"]
    output_file = config["processed_poem_file"]
    build_and_save_database(poem_directory, output_file)
    logger.info("数据库构建完成")
