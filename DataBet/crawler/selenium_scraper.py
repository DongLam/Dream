

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:\chromedriver.exe")
url = "https://stake.games/sports/home/upcoming/league-of-legends"
driver.get(url)

# print(driver.page_source)
while True:
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".variant-subtle-link.line-height-150pct.text-size-default.spacing-none.weight-semibold.align-left.fullWidth.svelte-1aq1zn0"))).click()
    try:
        time.sleep(5)
        load_more = driver.find_element(By.CSS_SELECTOR, ".variant-subtle-link.line-height-150pct.text-size-default.spacing-none.weight-semibold.align-left.fullWidth.svelte-1aq1zn0")
        load_more.click()
    except Exception as e:
        break
data = driver.find_element(By.XPATH, "/html/body").text
data_list = data.split("Winner")
del data_list[0]
print(len(data_list))
# for a in data_list:
#     print("-------------------------------------------")
#     print(a)
driver.close()

