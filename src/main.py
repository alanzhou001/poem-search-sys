from fetch_char import fetch_poem_characters
from trie_retrieval import search_poems
from input_char import input_characters
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
    time.sleep(5)  # 增加等待时间，提高按钮点击成功率
    driver.execute_script("arguments[0].click();", start_button)

    count = 1
    while True:
        chars = []
        answer = []
        try:
            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="hint_status_init"]'))
            )

            # 获取汉字列表
            chars = fetch_poem_characters(driver, count)
            if not chars:
                raise ValueError("未能抓取到汉字列表")
            # 调用诗句检索函数
            results = search_poems(chars)
            
            # 显示结果
            print("\n" + "="*40)
            print("\033[1;32m" + "检索结果：" + "\033[0m")
            if results:
                result, score = results[0]
                print(f"\033[1;34m找到诗句：{result}，评分：{score}\033[0m")
                # 获取答案列表（取第一个结果并转化为列表）
                answer = list(result)
            else:
                print("\033[1;31m未找到符合条件的诗句\033[0m")
            print("="*40 + "\n")
            
            # 输入汉字
            input_characters(driver, chars, answer, count)

            # 判断是否成功跳转到下一题
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="q{}"]/div/div[1]/div[3]/b[1]'.format(count)))
                )
                # 如果元素还存在，说明没跳转，答案可能错误，点击跳过按钮
                skip_button_xpath = '//*[@id="q{}"]/div/div[1]/button'.format(count)
                skip_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, skip_button_xpath))
                )
                skip_button.click()
                time.sleep(0)
            except:
                # 如果不存在说明正常跳转，无需点击跳过按钮，直接进入下一循环
                pass

            count += 1
            '''if count > 50:  # 测试50题
                break'''

        except Exception as e:
            print(f"\033[1;31m发生错误：{e}\033[0m")
            print("\033[1;33m跳过当前循环，进入下一题...\033[0m")
            skip_button_xpath = '//*[@id="q{}"]/div/div[1]/button'.format(count)
            skip_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, skip_button_xpath))
            )
            skip_button.click()
            continue

    #driver.quit()

if __name__ == "__main__":
    main()