from tqdm import tqdm
import line_profiler as lp
import memory_profiler as mp
import time
import pickle as pkl
from faker import Faker


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





if __name__ == '__main__':



