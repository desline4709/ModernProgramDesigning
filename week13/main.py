import re
import time
import random
import threading
import requests
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class StopParser(Exception):
    pass


class Producer(Thread):
    def __init__(self, url, q):
        super().__init__()
        self._url = url
        self._html = ""
        self._q = q

    def crawler(self):
        headers1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": '1'}
        headers2 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"}
        ran_int = random.random()
        if ran_int <=0.5:
            headers = headers1
        else:
            headers = headers2
        # time.sleep(10)
        r = requests.get(self._url, headers=headers)
        if r.status_code == 200:
            # 状态正常
            # print(r.text)
            self._html = r.text
        else:
            print(r.status_code)
            raise Exception("歌单页爬取错误！")

    def parser(self):
        soup = BeautifulSoup(self._html, "html.parser")
        if "古风" not in soup.title.string:
            print(self._url)
        playlist_htmls = soup.find_all(class_='u-cover u-cover-1')
        playlist = []
        for html in playlist_htmls:
            soup_temp = BeautifulSoup(str(html), "html.parser")
            # print(soup_temp)
            playlist_id = soup_temp.select('a[class="icon-play f-fr"]')[0]['data-res-id']
            playlist_url = "https://music.163.com/playlist?id=" + playlist_id
            playlist.append((playlist_id, playlist_url))
            q.put((playlist_id, playlist_url))
        # print(playlist)

    def run(self):
        try:
            self.crawler()
            self.parser()
        except Exception:
            time.sleep(random.random() + 1)
            print("Try angain!")
            self.crawler()
            self.parser()
        print(f"Producer {threading.current_thread()} finished!")


class Consumer(Thread):
    def __init__(self, q, lock, id):
        super().__init__()
        self._q = q
        self._url = ""
        self._html = ""
        self._list_id = 0
        self._lock = lock
        self._id = id

    def crawler(self):
        self._list_id,self._url = q.get()
        if self._list_id is None or self._url is None:
            raise StopParser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": '1'}
        r = requests.get(self._url, headers=headers, allow_redirects=False, verify=True)
        if r.status_code == 200:
            # 状态正常
            self._html = r.text
        else:
            raise Exception("详情页爬取错误！")

    def parser(self):
        soup = BeautifulSoup(self._html, "html.parser")
        img_url = soup.find_all(class_='j-img')[0]['data-src']
        playlist_title = str(soup.find_all(class_='f-ff2 f-brk')[0].string).replace(',','，').replace('\n','')
        creator_name = str(soup.find_all(class_='s-fc7')[0].string)
        creator_id = re.search('[0-9]+', soup.find_all(class_='s-fc7')[0]['href']).group()  # 以str形式储存
        song_num = str(soup.find_all(id="playlist-track-count")[0].string)
        play_num = str(soup.find_all(id="play-count")[0].string)  # 播放量
        add_to_num = soup.find_all(class_='u-btni u-btni-fav')[0].i.string.strip('()')  # 添加到播放列表次数
        shared_num = soup.find_all(class_='u-btni u-btni-share')[0].i.string.strip('()')  # 分享次数
        comments_num = soup.find_all(id='comment-box')[0]['data-count']
        cover_name = self._list_id + '-cover' + '.png'
        if shared_num == '分享':
            shared_num = '0'
        try:
            temp = list(soup.find_all(id="album-desc-more")[0].children)
            s = ""
            for i in temp:
                if type(i) == type(BeautifulSoup("<p>string</p>", "html.parser").string):
                    s += str(i)
            description = s.replace(',','，').replace('\n','')
        except IndexError:
            description = ''
        data = ','.join([cover_name,playlist_title,creator_id,creator_name,description,song_num,play_num,add_to_num,shared_num,comments_num])
        data = data + '\n'
        self._download_img(img_url)
        with self._lock:
            self._save_to_csv(data)

    def _download_img(self, url):
        r = requests.get(url)
        path = "result/" + self._list_id + '-cover' + '.png'
        if r.status_code == 200:
            with open(path, 'wb') as img:
                img.write(r.content)
        else:
            raise Exception('图片抓取错误！')

    def _save_to_csv(self, data):
        global flag
        if flag == 0:
            head = '封面名称,歌单标题,创建者id,创建者昵称,歌单描述,歌曲数目,播放次数,添加到播放列表次数,分享次数,评论数量\n'
            with open('result/playlist_info.csv', 'w', encoding='utf-8') as f:
                f.write(head)
            flag = 1
        with open('result/playlist_info.csv', 'a', encoding='utf-8') as f:
            f.write(data)

    def run(self):
        try:
            while 1:
                self.crawler()
                self.parser()
        except StopParser:
            print(f"Consumer thread {self._id} {threading.current_thread()} finished!")


if __name__ == '__main__':
    flag = 0
    cat = "古风"
    url = ["https://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}".format(cat, num*35) for num in range(38)]
    q = Queue()
    mutex = threading.Lock()
    plist = []
    for i in range(len(url)):
        p = Producer(url[i], q)
        plist.append(p)
        time.sleep(random.random() + 1)
        p.start()
    clist = []
    for i in range(40):
        c = Consumer(q, mutex, i+1)
        clist.append(c)
        c.start()
    for p in plist:
        p.join()

    while 1:
        time.sleep(3)
        if q.empty():
            for i in range(len(clist)):
                time.sleep(2)
                q.put((None,None))
            break
        else:
            continue

    for c in clist:
        c.join()

    print("main done!")



