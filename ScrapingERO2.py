import os
import random
import string
import time
import requests
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def make_randname():
    letters = string.ascii_uppercase + string.digits
    return ''.join([random.choice(letters) for x in range(20)])


def get_img(url):
    print('fetching images from {}'.format(url))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'}
    res = requests.get(url, headers=headers)  # 子ページを取得する。
    soup = BeautifulSoup(res.text, 'lxml')

    # img タグを探して、ダウンロードする。
    for img_tag in soup.find_all('img', src=True):
        img_url = img_tag['src']
        print('downlaoding image... ', img_url)

        parsed_url = urlparse(img_url)
        ext = os.path.splitext(parsed_url.path)[1]  # 拡張子抽出
        save_path = os.path.join('images', '{basename}{ext}'.format(
            basename=make_randname(), ext=ext))

        # 画像をダウンロードして、保存する。
        img = requests.get(img_url).content
        with open(save_path, 'wb') as f:
            f.write(img)
        print('image saved ', save_path)

        time.sleep(0.5)  # 画像取得間隔


def get_url(url):
    print('fetching html... ', url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    for a_tag in soup.findAll('a', href=True):
        get_img(a_tag['href'])
        time.sleep(1)  # 子ページへのアクセス間隔


def main():
    os.makedirs('images', exist_ok=True)
    for i in range(1, 2):
        url = 'http://hnalady.com/page-{}.html'.format(i)
        get_url(url)


if __name__ == '__main__':
    main()