from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from GetData import get_path
from GetData import write_data
import time
import json

def scrollByElemAndOffset(self, element, offset = 0):
    
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        if (offset != 0):
            script = "window.scrollTo(0, window.pageYOffset + " + str(offset) + ");"
            self.driver.execute_script(script)

def main():
    domain = "https://www.amazon.co.jp"
    url_table = get_path()
    driver = webdriver.Chrome()
    table = {}
    for (key, path) in url_table.items():
        if key == 'new_releases':
            continue
        url = domain + path
        driver.get(url)
        for i in range(40):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
            time.sleep(3)
        info_list = []
        for each in driver.find_elements(By.CLASS_NAME, 'av-hover-wrapper'):
            info = {}
            info['path'] = each.find_element(By.TAG_NAME, 'a').get_attribute('href')
            info['title'] = each.find_element(By.TAG_NAME, 'a').get_attribute('aria-label')
            info['img'] = each.find_element(By.TAG_NAME, 'img').get_attribute('src')
            info_list.append(info)
        table[key] = info_list
    path = 'src/assets/data.json'
    with open(path, 'w') as f:
        f.write(json.dumps(table))

if __name__ == '__main__':
    main()
