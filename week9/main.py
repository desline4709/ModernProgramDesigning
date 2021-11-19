import os
import sys
import time
import inspect
import pickle as pkl
from tqdm import tqdm
from faker import Faker
import line_profiler as lp
from functools import wraps
import memory_profiler as mp
from playsound import playsound



class WasteBase:
    """
    Base class for do something to waste time
    properties: size path faker
    """
    def __init__(self, size=1000000, path='data'):
        self._size = size
        self._path = path
        self._faker = Faker('zh_CN')

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @size.deleter
    def size(self):
        self._size = 0

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path

    @path.deleter
    def path(self):
        self._path = None

    @property
    def faker(self):
        return self._faker

    @faker.setter
    def faker(self, new_locale):
        self._faker = Faker(new_locale)

    @faker.deleter
    def faker(self):
        self._faker = None


class Waste(WasteBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_big_data(self):
        """
        创建大型数据
        :return:
        """
        print('创建数据量为{}的数据'.format(self.size))
        self._data = []
        for i in range(self.size):
            self._data.append(self.faker.name())
        print('创建完成')

    def pickle_data(self, filepath, is_raleative_path):
        """
        大型数据的序列化
        :param filepath: 文件路径
        :param is_raleative_path: 是否为相对路径
        :return:
        """
        if is_raleative_path:
            filepath = self.path + filepath
        with open(filepath, 'wb') as f:
            pkl.dump(self._data, f)
        print('序列化完成')


class Decorator:
    """
    对浪费时间、空间的操作的类进行装饰的类
    """
    @staticmethod
    def show_runtime(func):
        """
        :param func: 被装饰的函数
        :return: 装饰器
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            print('function {} has ron for {} seconds'.format(func.__name__, end - start))
            return res

        return wrapper

    @staticmethod
    def show_lineinfo(func):
        """
        逐行分析代码运行耗时
        :param func: 需要分析的函数
        :return: 装饰器
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            profile = lp.LineProfiler(func)  # 将函数传递到分析器
            profile.enable()  # 开始分析
            res = func(*args, **kwargs)
            profile.disable()  # 停止分析
            profile.print_stats(sys.stdout)  # 打印出性能分析结果
            return res

        return wrapper

    @staticmethod
    def check_path(func):
        """
        检查函数中的路径是否正确
        :param path: 路径参数的名称
        :return: 装饰器
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            pathflag = kwargs.get('filepath', False)
            if not pathflag:
                # 这个路径参数不存在
                raise Exception("No path parameter \'filepath\'")
            # 下面检查路径本身是否存在
            path_value = kwargs['filepath']
            os_path_list = os.listdir()
            if path_value not in os_path_list:
                # 需要新建文件夹
                print('文件夹{}不存在，下面开始创建...'.format(path_value))
                os.mkdirs(path_value)
            res = func(*args, **kwargs)
            return res

        return wrapper

    @staticmethod
    def play_sound_after_incident(soundpath):
        """
        在某个事件完成后播放声音进行提示
        :param soundpath: 声音文件的路径
        :return: 装饰器
        """
        def decorator(func):  # 高阶函数
            @wraps(func)
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                print('事件已发生！播放声音进行提示...')
                playsound(soundpath)
                return res
            return wrapper
        return decorator


class WasteProxy(Waste):
    @Decorator.show_runtime
    @Decorator.show_lineinfo
    def generate_big_data(self):
        print('创建数据量为{}的数据'.format(self.size))
        self._data = []
        for i in tqdm(range(self.size)):
            self._data.append(self.faker.name())
        print('创建完成')

    @Decorator.play_sound_after_incident('music/sound1')
    @Decorator.check_path
    @mp.profile
    def pickle_data(self, filename, is_raleative_path):
        if is_raleative_path:
            filepath = self.path + filepath
        with open(filepath, 'wb') as f:
            pkl.dump(self._data, f)
        print('序列化完成')
    

    

class Test:
    def __init__(self, WasteProxy: WasteProxy):
        self.wp = WasteProxy
    
    def test(self):
        self.wp.generate_big_data()
        self.wp.pickle_data('data/data.pkl', is_raleative_path=True)


if __name__ == '__main__':
    pass