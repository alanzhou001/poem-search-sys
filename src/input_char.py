from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def input_characters(driver, chars, answer, count):
    xpath_template = '//*[@id="q{}"]/div/div[1]/div[3]/b[{}]'
    
    # 按照答案列表顺序依次点击对应的汉字
    for char in answer:
        index = chars.index(char) + 1  # 因为xpath中的序号从1开始，所以要加1
        xpath = xpath_template.format(count, index)
        elem = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elem.click()
        time.sleep(0.5)