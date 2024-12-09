from fetch_char import fetch_poem_characters
from trie_retrieval import search_poems
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils import load_config
import time

def main():
    # 读取配置文件
    config = load_config()
    edge_driver_path = config["edge_driver_path"]
    oriurl = config["oriurl"]
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service)

    # 浏览器自动驱动，登录网站
    driver.get(oriurl)

    # 等待按钮加载并确保按钮可见
    start_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/article/div[1]/button'))
    )

    # 使用 JavaScript 点击按钮
    driver.execute_script("arguments[0].click();", start_button)

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="hint_status_init"]'))
    )

    while True:
        try:
            # 获取汉字列表
            input_chars = fetch_poem_characters(driver)
            
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
            
            # 等待用户进入下一题
            input("\033[1;33m按 Enter 键给出答案...\033[0m")

            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="hint_status_init"]'))
            )
        except Exception as e:
            print(f"\033[1;31m发生错误：{e}\033[0m")
            print("\033[1;33m跳过当前循环，进入下一题...\033[0m")
            continue

if __name__ == "__main__":
    main()