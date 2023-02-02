

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

def lol():
    url = "https://stake.games/sports/home/upcoming/league-of-legends"
    driver.get(url)
    time.sleep(10)
    # while True:
    #     try:
    #         time.sleep(5)
    #         load_more = driver.find_element(By.CSS_SELECTOR, ".variant-subtle-link.line-height-150pct.text-size-default.spacing-none.weight-semibold.align-left.fullWidth.svelte-1aq1zn0")
    #         load_more.click()
    #         break
    #     except Exception as e:
    #         break
    data = driver.find_element(By.XPATH, "/html/body").text
    data_list = data.split("Winner")
    del data_list[0]
    print(len(data_list))
    for a in data_list:
        try:
            b = a.split("\n")

            tmp = {
                'team1': b[1],
                'odds1': float(b[2]),
                'team2': b[3],
                'odds2': float(b[4]),
                'site': 1,
                'game': 2
            }
            # tmp = sort_team_name(tmp)
            print(tmp)
            # matchSerializer = MatchSerializer(data=tmp)
            # if matchSerializer.is_valid():
            #     print(matchSerializer)
            #     # matchSerializer.save()
        except Exception as e:
            print(e)
            continue
    driver.close()

if __name__ == '__main__':
    lol()