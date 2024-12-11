from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
from utils import load_config


config = load_config()
edge_driver_path = config["edge_driver_path"]
oriurl = config["oriurl"]
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service)

# 浏览器自动驱动，登录网站
driver.get(oriurl)

count = 1
# 构建对应汉字的xpath模板
xpath_template = '//*[@id="q{}"]/div/div[1]/div[3]/b[{}]'

# 等待按钮加载并确保按钮可见
start_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/article/div[1]/button'))
)
# 实测有效：增加time.sleep(5)可以大大提高按钮点击成功率
time.sleep(5)

# 使用JavaScript点击按钮
driver.execute_script("arguments[0].click();", start_button)

while True:  # 通过循环来处理每一道题
    # 等待页面加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="hint_status_init"]'))
    )

    all_words = []
    xpath = '//*[@id="q{}"]/div/div[1]/div[3]/b'.format(count)
    words = driver.find_elements(By.XPATH,xpath)
    for word in words:
        all_words.append(word.text)
    print(all_words)

#  这里只是简单的取前7个汉字作为答案，大家可以根据实际情况调整答案的获取方式
    answer = all_words[:7]
    
    # 按照答案列表顺序依次点击对应的汉字
    for char in answer:
        index = answer.index(char) + 1  # 因为xpath中的序号从1开始，所以要加1
        xpath = xpath_template.format(count, index)
        elem = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elem.click()
        time.sleep(0.5)

    # 判断是否成功跳转到下一题（这里我简单通过判断当前题目元素是否还存在来粗略判断，如果不存在了，可认为跳转到下一题了）
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, xpath_template.format(count, 1)))
        )
        # 如果元素还存在，说明没跳转，答案可能错误，点击跳过按钮
        skip_button_xpath = '//*[@id="q{}"]/div/div[1]/button'.format(count)
        skip_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, skip_button_xpath))
        )
        skip_button.click()
        time.sleep(1)
    except:
        # 如果不存在了，说明正常跳转到下一题了，无需点击跳过按钮，直接进行下一题的处理
        pass

    count += 1
    if count > 50:  # 这里假设最多做50道题，大家可以根据实际情况调整这个结束条件
        break

driver.quit()