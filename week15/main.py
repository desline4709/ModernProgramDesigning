import re
import asyncio
import requests
from bs4 import BeautifulSoup as bs


async def producer(url,i):
    l_playlist = []

    async def crawler(url=url):
        headers1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": '1'}
        r = requests.get(url, headers=headers1)
        if r.status_code == 200:
            # 状态正常
            # print(r.text)
            html = r.text
            return html
        else:
            print(r.status_code)
            raise Exception("歌单页爬取错误！")
    
    async def parser(html):
        """
        解析歌单页面，将页面中所有的歌单id和url打包放入l_playlist
        """
        soup = bs(html, parser="html.parser")
        if "古风" not in soup.title.string:
            print(url)
        playlist_htmls = soup.find_all(class_='u-cover u-cover-1')
        for h in playlist_htmls:
            soup_temp = bs(str(h), "html.parser")
            # print(soup_temp)
            playlist_id = soup_temp.select('a[class="icon-play f-fr"]')[0]['data-res-id']
            playlist_url = "https://music.163.com/playlist?id=" + playlist_id
            l_playlist.append((playlist_id, playlist_url))
        print(l_playlist)

    html = await crawler(url)
    await parser(html)
    for playlist in l_playlist:
        await consumer(playlist)
    print(f"Producer {i} done!")

async def consumer(playlist):
    l_songs = []
    wanted_l_playlist =[]

    async def crawler(url):
        headers1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": '1'}
        r = requests.get(url)
        if r.status_code == 200:
            # 状态正常
            # print(r.text)
            html = r.text
            return html
        else:
            print(r.status_code)
            raise Exception("歌单详情爬取错误！")

    async def filter(html):
        soup = bs(html, "html.parser")
        play_num = int(str(soup.find_all(id="play-count")[0].string))  # 播放量
        if play_num > 100000:
            wanted_l_playlist.append(playlist)

    async def songs_parser(playlist_id,html):
        soup = bs(html, "html.parser")
        s = bs(str(soup.find_all("ul","f-hide")[0]), "html.parser")  # 获取歌单前10首歌曲的url
        songs = s.find_all("a")
        host = "https://music.163.com/"
        for i in songs:
            url = host + i["href"]
            l_songs.append((playlist_id,url))
    
    async def songs_info_download(playlist_id,html):
        soup = bs(html, "html.parser")
        title = str(soup.find_all(class_="f-ff2")[0].string)
        singer = str(soup.find_all(class_="des s-fc4")[0].span["title"])
        try:
            album = str(soup.find_all(class_="des s-fc4")[1].a.string)
        except IndexError:
            album = "无"
        with open(f"result/{playlist_id}-details.csv",'a', encoding='utf-8') as f:
            f.write(",".join([title,singer,album])+'\n')

    async def downloads_parser(playlist_id,html):
        soup = bs(html, "html.parser")
        img_url = soup.find_all(class_='j-img')[0]['data-src']
        playlist_title = str(soup.find_all(class_='f-ff2 f-brk')[0].string).replace(',','，').replace('\n','')
        creator_name = str(soup.find_all(class_='s-fc7')[0].string)
        creator_id = re.search('[0-9]+', soup.find_all(class_='s-fc7')[0]['href']).group()  # 以str形式储存
        song_num = str(soup.find_all(id="playlist-track-count")[0].string)
        play_num = str(soup.find_all(id="play-count")[0].string)  # 播放量
        add_to_num = soup.find_all(class_='u-btni u-btni-fav')[0].i.string.strip('()')  # 添加到播放列表次数
        shared_num = soup.find_all(class_='u-btni u-btni-share')[0].i.string.strip('()')  # 分享次数
        comments_num = soup.find_all(id='comment-box')[0]['data-count']
        cover_name = playlist_id + '-cover' + '.png'
        if shared_num == '分享':
            shared_num = '0'
        try:
            temp = list(soup.find_all(id="album-desc-more")[0].children)
            s = ""
            for i in temp:
                if type(i) == type(bs("<p>string</p>", "html.parser").string):
                    s += str(i)
            description = s.replace(',','，').replace('\n','')
        except IndexError:
            description = ''
        data = ','.join([cover_name,playlist_title,creator_id,creator_name,description,song_num,play_num,add_to_num,shared_num,comments_num])
        data = data + '\n'
        await _download_img(playlist_id,img_url)
        await _save_to_csv(data)

    async def _download_img(playlist_id,url):
        r = requests.get(url)
        path = "result/" + playlist_id + '-cover' + '.png'
        if r.status_code == 200:
            with open(path, 'wb') as img:
                img.write(r.content)
        else:
            raise Exception('图片抓取错误！')

    async def _save_to_csv(data):
        global flag
        if flag == 0:
            head = '封面名称,歌单标题,创建者id,创建者昵称,歌单描述,歌曲数目,播放次数,添加到播放列表次数,分享次数,评论数量\n'
            with open('result/playlist_info.csv', 'w', encoding='utf-8') as f:
                f.write(head)
            flag = 1
        with open('result/playlist_info.csv', 'a', encoding='utf-8') as f:
            f.write(data)

    async def _details_init(playlist_id):
        with open(f'result/{playlist_id}-details.csv', 'w', encoding='utf-8') as f:
            f.write("歌曲名称,歌手,歌曲专辑\n")


    playlist = playlist
    playlist_id = playlist[0]
    playlist_url = playlist[1]
    playlist_html = await crawler(playlist_url)
    await filter(playlist_html)
    # print(f"wanted playlist: {wanted_l_playlist}")
    for i in wanted_l_playlist[:]:
        await _details_init(i[0])
        html = await crawler(i[1])
        await downloads_parser(i[0], html)
        await songs_parser(i[0], html)
        wanted_l_playlist.remove(i)
    for i in l_songs[:]:
        html = await crawler(i[1])
        await songs_info_download(i[0],html)
        l_songs.remove(i)
    print(f"Consumer playlist: {playlist_id} done")

if __name__ == '__main__':
    cat = "古风"
    urls = ["https://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}".format(cat, num*35) for num in range(38)]
    flag = 0
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(producer(url,urls.index(url)+1)) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
