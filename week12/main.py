import os
import time
import jieba
# from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Lock


word_dict = {}
q = Queue()
mutex = Lock()


def generator(text: list):
    max_index = len(text) - 1
    i = 0
    while i < max_index:
        yield text[i]
        i += 1
    return 'generator done!'


class Map(Process):
    def __init__(self, id, text: list, n, q):
        super().__init__()
        self._id = id  # 进程编号
        self._text = text  # 字符串列表
        self._n = n  # 一共有几个进程
        self._q = q

    @property
    def id(self):
        return self._id

    def run(self):
        print(f'Map-{self.id} running with pid {os.getpid()}...')
        index_0 = self.id % self._n
        length = len(self._text)
        index = index_0
        prt_flag = 0
        while index < length:
            # soup = BeautifulSoup(i)
            content = self._text[index]
            if '<content>' in content:
                self._q.put(self.cut_and_calculate(content), timeout=3)
            if index >= 1000000 and prt_flag == 0:
                print("1000000")
                prt_flag = 1
            elif index >= 5000000 and prt_flag == 1:
                print("5000000")
                prt_flag = 2
            elif index >= 8000000 and prt_flag == 2:
                print("8000000")
            # print(index)
            index += self._n

        print(f'Process Map {self.id} with pid {os.getpid()} finished!')
        # self._q.put(None, timeout=3)

    def cut_and_calculate(self, text: str):
        text = text.replace('<content>', '')
        text = text.replace('</content>', '')
        text = text.replace('\u3000', ' ')
        text = text.strip('\n')
        wordlist = jieba.lcut(text)
        w_dict = {}
        for i in wordlist:
            if i not in w_dict:
                w_dict[i] = 1
            else:
                w_dict[i] += 1
        return w_dict


class Reduce(Process):
    def __init__(self, id, q):
        super().__init__()
        self._id = id
        self._q = q

    @property
    def id(self):
        return self._id

    def run(self):
        print(f'Redude-{self.id} running with pid {os.getpid()}...')
        while 1:
            w_dict = self._q.get(timeout=10)
            # print(f'w_dict: {w_dict}')
            if w_dict is None:
                break
            for i in w_dict:
                with mutex:
                    if i not in word_dict:
                        word_dict[i] = 1
                    else:
                        word_dict[i] += 1
        # print(word_dict)
        with open('result.txt', 'w') as f:
            f.write(str(word_dict))
        print(f"Reduce-{self.id} finished with id {os.getpid()}...")


if __name__ == '__main__':
    start = time.time()
    with open('news_.txt', 'r', encoding='GBK', errors='ignore') as f:
        text = f.readlines(10000000)
    print(len(text))
    mlist = []
    rlist = []
    m_num = 6
    r_num = 1
    for i in range(m_num):
        m = Map(i+1, text, m_num, q)
        mlist.append(m)
    for i in range(r_num):
        r = Reduce(i+1, q)
        rlist.append(r)

    for m in mlist:
        # print('m1')
        m.start()

    for r in rlist:
        # print('r1')
        r.start()

    for m in mlist:
        m.join()

    for i in range(r_num):
        q.put(None)

    for r in rlist:
        r.join()

    # print(word_dict)
    end = time.time()
    print(f'main has ron for {end-start} seconds with {m_num} Map Procession and {r_num} Reduce Procession!')

