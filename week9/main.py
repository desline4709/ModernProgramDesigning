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
    def __init__(self)


if __name__ == '__main__':



