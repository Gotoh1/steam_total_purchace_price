from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
URL = "https://store.steampowered.com/login/"  # <= ここにスクレイピングしたい対象URLを書いてください
ID = ""                        # <= ここにログインIDを書いてください
ID_sel = "#input_username"               # <= ここにログインID欄のCSSセレクタを書いてください
PASS = ""                        # <= ここにログインパスワードを書いてください
PASS_sel = "#input_password"               # <= ここにログインパスワード欄のCSSセレクタを書いてください
# <= ここにスクレイピングしたい対象URLを書いてください
Selector = "https://store.steampowered.com/account/history/"

# 必須

# Selenium用オプション
"""
op = Options()
op.add_argument("--disable-gpu")
op.add_argument("--disable-extensions")
op.add_argument("--proxy-server='direct://'")
op.add_argument("--proxy-bypass-list=*")
op.add_argument("--start-maximized")
op.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=op)
"""
driver = webdriver.Chrome()

driver.get(URL)


WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, PASS_sel))
)
driver.find_elements_by_css_selector(ID_sel)[0].send_keys(ID)
driver.find_elements_by_css_selector(PASS_sel)[0].send_keys(PASS)
driver.find_elements_by_css_selector(PASS_sel)[0].send_keys(Keys.ENTER)

# ターゲット出現を待機
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#account_dropdown"))
)

driver.get("https://store.steampowered.com/account/history/")
soup = BeautifulSoup(driver.page_source, features="html.parser")

table = soup.findAll("table", {"class": "wallet_history_table"})[0]
rows = table.findAll("tr")
for row in rows:
    for cell in row.findAll("td", {"class": "wht_total "}):
        if "クレジット" in cell.text:
            continue
        p = cell.text.replace(",", "").replace(" ", "").replace("\\", "")
        print(p)
