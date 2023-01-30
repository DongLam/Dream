

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:\chromedriver.exe")
url = "https://stake.games/sports/home/upcoming/counter-strike"
driver.get(url)
time.sleep(3)
