from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import setup_logger, load_config

def fetch_poem_characters(driver, count):
    # 读取配置文件
    config = load_config()
    log_dir = config["log_directory"]

    # 设置日志记录
    logger = setup_logger(log_dir, "fetch_char.log")

    characters = []

    try:
        # 爬取想要的信息
        allelem = driver.find_elements(By.XPATH, '//*[@id="q{}"]/div/div[1]/div[3]/b'.format(count))

        for elem in allelem:
            word = elem.text.strip()  # 去除前后空白字符
            if word:  # 过滤掉空字符
                characters.append(word)

    except Exception as e:
        logger.error(f"出现异常：{e}")

    return characters

# 示例调用
if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service

    # 读取配置文件
    config = load_config()
    edge_driver_path = config["edge_driver_path"]
    oriurl = config["oriurl"]

    # 指定 Edge WebDriver 的路径
    service = Service(executable_path=edge_driver_path)

    # 启动浏览器
    driver = webdriver.Edge(service=service)

    # 浏览器自动驱动，登录网站
    driver.get(oriurl)

    characters = fetch_poem_characters(driver)
    print(characters)

    # 关闭浏览器
    driver.quit()