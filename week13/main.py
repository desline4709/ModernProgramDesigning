import requests
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


class Crawler(Thread):
    def __init__(self, url):
        super().__init__()
        self._url = url

    def run(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": '1'}
        r = requests.get(self._url,headers=headers,allow_redirects=False,verify=True)
        global html
        if r.status_code == 200:
            # 状态正常
            print(r.text)
            html.append(r.text)


class Parser(Thread):
    def __init__(self, html):
        super().__init__()
        self._html = html

    def run(self):
        print(self._html)


if __name__ == '__main__':
    cat = "古风".encode('utf-8')
    url = ["https://music.163.com/discover/playlist/?order=hot&cat=古风&limit=35&offset=0"]
    html = []
    c = Crawler(url[0])
    c.start()
    c.join()
    p = Parser(html[0])
    p.start()

