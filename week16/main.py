import time
import random
import asyncio
import aiohttp
from pymongo import MongoClient


BASE_URL = 'https://s.search.bilibili.com/cate/search'
sleep_choice = [1,1.5,2,2.5,5]

class BiliHotCrawler:
    def __init__(self,cate,limit=300, time_from=20211110, time_to=20211117):
        self.cate_id = cate
        self.limit = limit
        self.page = 1
        self.pagesize = 100
        self.time_from = time_from
        self.time_to = time_to
        self.bulid_param(time_from=self.time_from, time_to=self.time_to)
        self.url = BASE_URL
        self.result_list = []
        
    def bulid_param(self, time_from, time_to):
        self.params = {
            'main_ver':'v3',
            'search_type':'video',
            'view_type':'hot_rank',
            'order':'click',
            'cate_id':self.cate_id,
            'page':self.page,
            'pagesize':self.pagesize,
            'time_from':20211110,
            'time_to':20211117
        }
        self.params['time_from'] = time_from
        self.params['time_to'] = time_to
        
    async def get_resp(self):
        time.sleep(random.choice(sleep_choice))
        self.bulid_param(time_from=self.time_from, time_to=self.time_to)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url,params=self.params) as response:
                self.resp = await response.read()
        self.page += 1

    def save_resp(self):
        self.resp = eval(self.resp.decode('utf-8').replace('null','None').replace('false',"False").replace("true","True").replace("\n"," "))
        for item in self.resp["result"]:
            # 分类 排名 bv号 时长 播放量 弹幕 标题 封面 评论 收藏 描述 直链
            temp_dict = {}
            temp_dict["createtime"] = time.ctime()
            temp_dict["current_rank"] = item["rank_offset"]
            temp_dict["video_title"] = item["title"]
            temp_dict["bvid"] = item["bvid"]
            temp_dict["time_period"] = "from {} to {}".format(self.params["time_from"], self.params["time_to"])
            self.result_list.append(temp_dict)
            

    def log(self,isend=False):
        print(f"\rCrawlering {self.cate_id} {(self.page - 1)*self.pagesize}/{self.limit}",end="")
        if isend:
            print()

    async def start(self):
        while self.pagesize * self.page <= self.limit:
            self.log()
            await self.get_resp()
            self.save_resp()
        self.log(isend=True)
        return self.result_list

def test1():
    loop = asyncio.get_event_loop()
    task = loop.create_task(BiliHotCrawler(28).start())
    loop.run_until_complete(task)
    print(task.result()[200])  # 得到了第一次爬取的记录

def test2():
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(BiliHotCrawler(28, limit=10000).start())
    task2 = loop.create_task(BiliHotCrawler(28, limit=10000, time_from=20211117,time_to=20211124).start())
    tasks = [task1,task2]
    loop.run_until_complete(asyncio.wait(tasks))
    with MongoClient('localhost',27017) as client:
        db = client.test
        collection = db.bili_test

        # print(type(task1.result()))
        # print(task1.result()[0])
        # collection.insert_many(task1.result())  # 将第一次的爬虫结果存入数据库
        for i in task1.result():
            try:
                collection.insert_one(i)
            except:
                # print(i)
                i["video_title"] = i["video_title"].encode("utf-8","replace").decode("utf-8")
                collection.insert_one(i)
                continue
        
        record1 = [i for i in collection.find().sort("current_rank",1)]  # 第一次的记录是从数据库中取出的
        record2 = task2.result()  # 第二次的记录是爬取的记录
        r1_id = [i["bvid"] for i in record1]
        r2_id = [i["bvid"] for i in record2]
        print(len(record1))
        print(len(record2))
        # print(r1_id[0])
        # print(r2_id[0])
        for i in r2_id:
            if i not in r1_id:
                # 只在第二次的记录
                index = r2_id.index(i)
                rec = record2[index]
                try:
                    collection.insert_one(rec)
                except:
                    rec["video_title"] = rec["video_title"].encode("utf-8","replace").decode("utf-8")
                    collection.insert_one(rec)
                    continue
                # print(rec)
            else:
                # print(i)
                index = r2_id.index(i)
                rec_new = record2[index]
                rec_ori = record1[r1_id.index(i)]
                collection.update_one(rec_ori,{"$set":{"current_rank":rec_new["current_rank"],"update_time":time.ctime()}})

        for i in r1_id:
            if i not in r2_id:
                # 只在第一次的记录
                index = r1_id.index(i)
                rec = record1[index]
                collection.delete_one(rec)

    


def reset_db():
    with MongoClient('localhost',27017) as client:
        db = client.test
        collection = db.bili_test
        collection.delete_many({})


if __name__ == "__main__":
    # test1()
    reset_db()
    test2()
    
