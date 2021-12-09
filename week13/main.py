import requests
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


class Producer(Thread):
    def __init__(self, url):
        super().__init__()
        self._url = url
        self._html = ""

    def crawler(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": '1'}
        r = requests.get(self._url, headers=headers, allow_redirects=False, verify=True)
        if r.status_code == 200:
            # 状态正常
            # print(r.text)
            self._html = r.text

    def parser(self):
        soup = BeautifulSoup(self._html, "html.parser")
        playlist_htmls = soup.find_all(class_='u-cover u-cover-1')
        playlist = []
        for html in playlist_htmls:
            soup_temp = BeautifulSoup(str(html), "html.parser")
            # print(soup_temp)
            playlist_id = soup_temp.select('a[class="icon-play f-fr"]')[0]['data-res-id']
            playlist_url = "https://music.163.com/playlist?id=" + playlist_id
            playlist.append((playlist_id, playlist_url))
        print(playlist)

    def run(self):
        self.crawler()
        self.parser()


if __name__ == '__main__':
    cat = "古风".encode('utf-8')
    url = ["https://music.163.com/discover/playlist/?order=hot&cat=古风&limit=35&offset=0"]
    p = Producer(url[0])
    p.start()


