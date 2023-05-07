import time
import datetime
import json
import asyncio
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

homeURL = "https://www.amazon.co.jp/"

def url_to_soup(url):
    # 一回のみアクセス
    response = requests.get(url)
    response.encoding = response.apparent_encoding 
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def main():
    homeURL = "https://www.amazon.co.jp/"
    soup = url_to_soup(homeURL)
    print(soup.text)

def initialize_json():
    today = datetime.date.today()
    with open('static/data.json', "w") as f:
        json.dump({"updated": today.strftime("%Y-%m-%d")}, f, indent=4)

def initialize_driver():
    d = DesiredCapabilities.CHROME
    d['good:loggingPrefs'] = {'performance': 'ALL'}
    options = Options()
    options.add_argument('--headless')  # ブラウザを表示するかどうか
    driver = ChromeDriverManager().install()
    driver = webdriver.Chrome(driver, options=options, desired_capabilities=d)
    driver.implicitly_wait(2)
    return driver

def get_leaving_soon(driver: webdriver.Chrome):

    url = f"https://www.amazon.co.jp/s?k=%E3%82%82%E3%81%86%E3%81%99%E3%81%90%E9%85%8D%E4%BF%A1%E7%B5%82%E4%BA%86&i=instant-video&&crid=2I5LS6EDFPF9G&sprefix=mou%2Cinstant-video%2C253&ref=nb_sb_ss_ts-doa-p_2_3"
    driver.get(url)
    leaving_soon = []
    for i in range(20):
        print(f"------------------------------------{i}--------------------------------------------")
        # driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        video_card = [tag for tag in soup.find_all('div', class_="a-section a-spacing-base")]
        try:
            for i in range(len(video_card)):
                flag_text = video_card[i].find_all("span")[-1].text 
                if "または、プライム会員は￥0" == flag_text or "プライム会員の方は￥0" == flag_text:
                    #タイトル
                    d = {
                        "path": homeURL + video_card[i].find_all("a", class_="a-link-normal s-no-outline")[0].get('href'),
                        "img":  video_card[i].find_all('img', class_="s-image")[0].get('src'),
                        "title": video_card[i].find_all("span", class_="a-size-base-plus a-color-base a-text-normal")[0].text
                    }
                    leaving_soon.append(d)
            item = driver.find_element(By.CSS_SELECTOR, ("a[class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"))
            item.click()
        except:
            print("breaked")
            break

    return leaving_soon

def get_top_rated(driver: webdriver.Chrome):
    url = f"https://www.amazon.co.jp/s?i=instant-video&bbn=2351649051&rh=p_72%3A2761627051&dc&ds=v1%3AvIJs7EZOk5y2I7yhzfRW1Z6EPjRWqAeZlk6mrWVybbE&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=14P7MYD0D8WNR&qid=1683450816&rnid=2761626051&sprefix=%E9%AB%98%2Cinstant-video%2C208&ref=sr_nr_p_72_1"
    driver.get(url)
    top_rated = []
    for i in range(150):
        print(f"------------------------------------{i}--------------------------------------------")
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        video_card = [tag for tag in soup.find_all('div', class_="a-section a-spacing-base")]
        try:
            for i in range(len(video_card)):
                flag_text = video_card[i].find_all("span")[-1].text 
                if "または、プライム会員は￥0" == flag_text or "プライム会員の方は￥0" == flag_text:
                    d = {
                        "path": homeURL + video_card[i].find_all("a", class_="a-link-normal s-no-outline")[0].get('href'),
                        "img": video_card[i].find_all('img', class_="s-image")[0].get('src'),
                        "title": video_card[i].find_all("span", class_="a-size-base-plus a-color-base a-text-normal")[0].text
                    }
                    top_rated.append(d)
            item = driver.find_element(By.CSS_SELECTOR, ("a[class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"))
            item.click()
        except:
            break

    return top_rated

def get_recently_added(driver: webdriver.Chrome):
    url = f"https://www.amazon.co.jp/s?k=%E6%9C%80%E8%BF%91%E8%BF%BD%E5%8A%A0%E3%81%95%E3%82%8C%E3%81%9F&dc&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=HK2B2T0WIND2&sprefix=%E6%9C%80%E8%BF%91%E8%BF%BD%E5%8A%A0%E3%81%95%E3%82%8C%E3%81%9F%2Caps%2C187&ref=a9_asc_1"
    driver.get(url)
    recently_added = []
    for i in range(100):
        print(f"------------------------------------{i}--------------------------------------------")
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        video_card = [tag for tag in soup.find_all('div', class_="a-section a-spacing-base")]
        try:
            for i in range(len(video_card)):
                flag_text = video_card[i].find_all("span")[-1].text 
                if "または、プライム会員は￥0" == flag_text or "プライム会員の方は￥0" == flag_text:
                    d = {
                        "path": homeURL + video_card[i].find_all("a", class_="a-link-normal s-no-outline")[0].get('href'),
                        "img": video_card[i].find_all('img', class_="s-image")[0].get('src'),
                        "title": video_card[i].find_all("span", class_="a-size-base-plus a-color-base a-text-normal")[0].text
                    }
                    recently_added.append(d)
            item = driver.find_element(By.CSS_SELECTOR, ("a[class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"))
            item.click()
        except:
            break

    return recently_added

def update_json(data, key):
    with open('static/data.json') as f:
        json_data = json.load(f)
    json_data[key] = data
    with open('static/data.json', "w") as f:
        json.dump(json_data, f, indent=4)

if __name__ == '__main__':
    driver = initialize_driver()
    initialize_json()
    leaving_soon = get_leaving_soon(driver)
    update_json(leaving_soon, "leaving_soon")
    top_rated = get_top_rated(driver)
    update_json(top_rated, "top_rated")
    recently_added = get_recently_added(driver)
    update_json(recently_added, "recently_added")

def scrape():
    driver = initialize_driver()
    leaving_soon = get_leaving_soon(driver)
    update_json(leaving_soon, "leaving_soon")
    top_rated = get_top_rated(driver)
    update_json(top_rated, "top_rated")
    recently_added = get_recently_added(driver)
    update_json(recently_added, "recently_added")