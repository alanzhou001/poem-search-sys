import heapq
import json
from itertools import combinations
from utils import setup_logger, load_config
from PageRank import build_co_occurrence_graph


# 位置权重：根据字的位置赋予不同的权重
def position_weight(index, total_length):
    if index == 0 or index == total_length - 1:
        return 1.2  # 开头和结尾位置权重较高
    else:
        return 1.0  # 中间位置权重较低


# 计算排列的评分（包括PageRank分数和位置权重）
def calculate_weighted_score(permutation, pagerank_scores):
    total_score = 0
    total_length = len(permutation)
    for i, char in enumerate(permutation):
        score = pagerank_scores.get(char, 0)
        weight = position_weight(i, total_length)
        total_score += score * weight
    return total_score


# 生成排列时根据 char_followers 数据，按照可能性顺序确定字的排列
def generate_permutations(input_chars, target_length, char_followers, pagerank_scores):
    permutations = []
    for char in input_chars:
        if char in char_followers:
            followers = sorted(char_followers[char].items(), key=lambda x: -x[1])
            for follower, _ in followers:
                if follower in input_chars:
                    permutation = [char, follower]
                    while len(permutation) < target_length:
                        last_char = permutation[-1]
                        if last_char in char_followers:
                            next_followers = sorted(char_followers[last_char].items(), key=lambda x: -x[1])
                            for next_follower, _ in next_followers:
                                if next_follower in input_chars and next_follower not in permutation:
                                    permutation.append(next_follower)
                                    break
                        else:
                            break
                    if len(permutation) == target_length:
                        permutations.append(permutation)
    return permutations


# A* 搜索：通过启发式函数优化排列组合
def a_star_search(input_chars, target_length, pagerank_scores, char_followers, poem_database, logger):
    possible_permutations = generate_permutations(input_chars, target_length, char_followers, pagerank_scores)
    heap = []
    for perm in possible_permutations:
        score = calculate_weighted_score(perm, pagerank_scores)
        heapq.heappush(heap, (-score, perm))  # 采用负分值，以便最大值优先
    
    logger.debug(f"Possible permutations: {possible_permutations}")
    
    while heap:
        best_score, best_perm = heapq.heappop(heap)
        best_poem = "".join(best_perm)
        logger.debug(f"Checking permutation: {best_poem} with score: {-best_score}")
        if best_poem in poem_database:
            return best_poem, -best_score
    
    return None, None


# 主程序：进行诗句检索
def main():
    config = load_config()
    log_dir = config["log_directory"]
    logger = setup_logger(log_dir)
    
    input_chars = ["秦", "月", "川", "松", "雄", "帝", "宅", "泉", "石"]
    target_length = config["retrieval_target_length"]

    logger.info("开始加载数据库...")
    with open(r"D:\introAI\小组作业\db\processed\poem_database_with_followers.json", "r", encoding="utf-8") as f:
        database = json.load(f)

    poem_database = database["poem_database"]
    pagerank_scores = database["pagerank_scores"]
    char_followers = database["char_followers"]
    logger.info("数据库加载完成，开始检索...")

    # 调用 A* 搜索函数进行检索
    best_poem, best_score = a_star_search(input_chars, target_length, pagerank_scores, char_followers, poem_database, logger)

    if best_poem:
        logger.info(f"找到诗句：{best_poem}，评分：{best_score}")
    else:
        logger.info("未找到符合条件的诗句")


if __name__ == "__main__":
    main()