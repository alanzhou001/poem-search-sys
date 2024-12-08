from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils import setup_logger, load_config

def fetch_poem_characters():
    # 读取配置文件
    config = load_config()
    edge_driver_path = config["edge_driver_path"]
    oriurl = config["oriurl"]
    log_dir = config["log_directory"]

    # 设置日志记录
    logger = setup_logger(log_dir, "fetch_char.log")

    # 指定 Edge WebDriver 的路径
    service = Service(executable_path=edge_driver_path)

    # 启动浏览器
    driver = webdriver.Edge(service=service)

    # 浏览器自动驱动，登录网站
    driver.get(oriurl)

    characters = []

    try:
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

        # 爬取想要的信息
        allelem = driver.find_elements(By.XPATH, '/html/body/ul/li[1]/div/div[1]/div[3]/b')

        for elem in allelem:
            word = elem.text
            characters.append(word)
            elem.click()
            time.sleep(1)

    except Exception as e:
        logger.error(f"出现异常：{e}")

    finally:
        time.sleep(5)  # 等待5秒，查看爬取结果
        driver.quit()  # 退出浏览器

    return characters

# 示例调用
if __name__ == "__main__":
    characters = fetch_poem_characters()
    print(characters)