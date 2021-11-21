import os
import numpy as np
from PIL import Image


class PathNotExistError(Exception):
    pass


class RandomWalk:
    def __init__(self, mu, X_0, sigma2, N):
        self._x_0 = X_0
        self._mu = mu
        self._sigma2 = sigma2
        self._N = N

    @property
    def x_0(self):
        return self._x_0

    @x_0.setter
    def x_0(self, value):
        self._x_0 = value

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, value):
        self._mu = value

    @property
    def sigma2(self):
        return self._sigma2

    @sigma2.setter
    def sigma2(self, value):
        self._sigma2 = value

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, value):
        self._N = value

    def walk(self):
        cot = 0
        x_list = [self._x_0]
        for i in range(self._N):
            if i == 0:
                x = self._x_0
            else:
                sigma = np.sqrt(self._sigma2)
                w_t = np.random.normal(self._mu, sigma, 1)
                x = float(self._mu + x_list[i-1] + w_t)
                x_list.append(x)
            yield x
            cot += 1
        return "现有的序列为{}".format(x_list)

    @property
    def params(self):
        return "参数如下：mu-{}, x_0-{}, sigma^2-{}, N-{}".format(self._mu, self._x_0, self._sigma2, self._N)


class RandomWalks:
    """
    实现多个RandomWalk的合并
    """
    def __init__(self, length):
        self._walk_list = []
        self._length = length

    def add_walk(self, rw: RandomWalk):
        rw.N = self._length  # 长度对齐
        walk = rw.walk()
        self._walk_list.append(walk)

    def walks(self):
        return zip(self._walk_list)


class ImageIter:
    def __init__(self, pic_dir):
        """
        :param pic_dir: 图片文件夹路径
        """
        self._pic_dir = pic_dir
        self._pic_name_list = []
        self._cot = 0

    @property
    def pic_dir(self):
        return self._pic_dir

    @pic_dir.setter
    def pic_dir(self, new_dir):
        self._pic_dir = new_dir

    @pic_dir.deleter
    def pic_dir(self):
        self._pic_dir = None

    def _check_path(self):
        if not os.path.exists(self.pic_dir):
            raise PathNotExistError

    def _load_dir(self):
        try:
            self._check_path()
        except PathNotExistError:
            print("directory {} does not found".format(self.pic_dir))
        else:
            os.chdir(self.pic_dir)
            self._pic_name_list = os.listdir()

    def _digit_pic(self, image: Image):
        res = np.array(image)
        return res

    def __iter__(self):
        return self

    def __next__(self):
        if self._cot == 0:
            self._load_dir()
        length = len(self._pic_name_list)
        if self._cot < length:
            path = self._pic_name_list[self._cot]
            img = Image.open(path)
            dig_img = self._digit_pic(img)
            self._cot += 1
            return dig_img
        else:
            raise StopIteration('所有图片遍历完成！')


def main():
    '''
    # Test RandomWalk

    test = RandomWalk(0, 0, 1, 5)
    for i in test.walk():
        print(i)
    print(test.params)
    '''
    '''
    # Test RandomWalks
    
    rw1 = RandomWalk(0, 0, 1, 5)
    rw2 = RandomWalk(1, 1, 1, 8)
    rws = RandomWalks(10)
    rws.add_walk(rw1)
    rws.add_walk(rw2)
    walks = list(rws.walks())
    try:
        while 1:
            res = []
            for walk in walks:
                temp = next(walk[0])
                res.append(temp)
            print(res)
    except StopIteration:
        print('done')
    '''
    imageiter = ImageIter('Pics/2002/07/19/big')
    # for i in range(1):
    #     print(next(imageiter))
    try:
        while 1:
            next(imageiter)
    except StopIteration as si:
        print(si.value)
    # for i in imageiter:
    #     print("-"*30)
    #     print(i)



if __name__ == "__main__":
    main()