import time
import json
import asyncio
import requests
from bs4 import BeautifulSoup

def url_to_soup(url):
    # 一回のみアクセス
    response = requests.get(url)
    response.encoding = response.apparent_encoding 
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_info_from_url(flag_text, url):
    # 成功するまで0.1sごとにアクセス
    soup = url_to_soup(url)
    print(soup.text)
    path = "" 
    print(flag_text)
    while path == "":
        soup = url_to_soup(url)
        for each in soup.find_all('a'):
            if flag_text in each.text:
                path = each.get('href')
        time.sleep(0.1)
    return {'path':path, 'soup':soup}

def get_path_from_soup(text, soup):
    # アクセスなし
    url = ''
    for each in soup.find_all('a'):
        if text in each.text:
            url = each.get('href')
    if url == '':
        print('%sは見つかりません'.format(text))
    return url

def get_list_from_category_url(url):
    # 一回のみアクセス
    soup = url_to_soup(url)
    info_list = []
    for each in soup.select('.av-hover-wrapper'):
        info = {}
        info['path'] = each.find('a').get('href')
        info['title'] = each.find('a').get('aria-label')
        info['img'] = each.find('img').get('src')
        info_list.append(info)
    return info_list

def get_path():
    homeURL = "https://www.amazon.co.jp"
    prime_video_path = get_info_from_url('Prime Video', homeURL)['path']
    prime_video_soup = get_info_from_url('もうすぐ配信終了', homeURL+prime_video_path)['soup']
    new_releases_path = get_path_from_soup('新作', prime_video_soup)
    recently_added_path = get_path_from_soup('プライムに最近追加された作品', prime_video_soup)
    leaving_soon_path = get_path_from_soup('もうすぐ配信終了', prime_video_soup)
    top_rated_path = get_path_from_soup('高評価された作品', prime_video_soup)
    table = {}
    table['new_releases'] = new_releases_path
    table['recently_added'] = recently_added_path
    table['leaving_soon'] = leaving_soon_path
    table['top_rated'] = top_rated_path
    return table

def get_table():
    homeURL = "https://www.amazon.co.jp"
    prime_video_path = get_info_from_url('Prime Video', homeURL)['path']
    prime_video_soup = get_info_from_url('もうすぐ配信終了', homeURL+prime_video_path)['soup']
    new_releases_path = get_path_from_soup('新作', prime_video_soup)
    recently_added_path = get_path_from_soup('プライムに最近追加された作品', prime_video_soup)
    leaving_soon_path = get_path_from_soup('もうすぐ配信終了', prime_video_soup)
    top_rated_path = get_path_from_soup('高評価された作品', prime_video_soup)
    table = {}
    table['new_releases'] = get_list_from_category_url(homeURL+new_releases_path)
    table['recently_added'] = get_list_from_category_url(homeURL+recently_added_path)
    table['leaving_soon'] = get_list_from_category_url(homeURL+leaving_soon_path)
    table['top_rated'] = get_list_from_category_url(homeURL+top_rated_path)
    return table

def write_data():
    path = 'static/data.json'
    with open(path, 'w') as f:
        f.write(json.dumps(get_table()))

async def get_data():
    try:
        print('get_data() start ...')
        await asyncio.wait_for(write_data(), timeout=10)
        print('get_data() finished ...')
    except asyncio.TimeoutError:
        print('time out ...')

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_data())

if __name__ == '__main__':
    main()
