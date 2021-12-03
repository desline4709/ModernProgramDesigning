import os
import abc
import jieba
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from matplotlib import animation as anime


class Plotter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def plot(self, data, *args, **kwargs):
        pass


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class PointPlotter(Plotter):
    def plot(self, data: list):
        plt.figure()
        x = [i.x for i in data]
        y = [i.y for i in data]
        plt.plot(x, y, '.')
        plt.show()


class ArrayPlotter(Plotter):
    def plot(self, data):
        length = len(data)
        if length == 2:
            # 二维数据
            plt.figure()
            x = data[0]
            y = data[1]
            plt.plot(x, y)
            plt.show()
        elif length == 3:
            # 三维数据
            x = data[0]
            y = data[1]
            z = data[2]
            plt.figure()
            ax = plt.axes(projection='3d')
            ax.plot(x, y, z)
            plt.show()


class Text:
    def __init__(self, text):
        self._text = text
        self._wordlist = []
        self._word_dict = {}
        if type(self._text) == str:
            # 是单句话
            self._wordlist.append(jieba.lcut(self._text))
        elif type(self._text) == list:
            # 是很多句话
            for text in self._text:
                self._wordlist.append(jieba.lcut(text))

        def filter(wordlist, stopwords=''):
            """
            :param wordlist: 分词结果（也是一个列表）的列表
            :param stopwords: 停用词表的路径
            :return:
            """
            stopwords_list = []
            if stopwords:
                with open(stopwords, 'r', encoding='utf-8') as f:
                    stopwords_list = f.read().split('\n')
                if '\n' not in stopwords_list:
                    stopwords_list.append('\n')
            if stopwords_list:
                x = []
                for words in wordlist:
                    y = []
                    for i in words:
                        if i not in stopwords_list:
                            y.append(i)
                    x.append(y)
                res = x
            else:
                res = wordlist
            return res

        self._wordlist = filter(self._wordlist)

    def get_frequency(self):
        for words in self._wordlist:
            for i in words:
                if i not in self._word_dict:
                    self._word_dict[i] = 1
                else:
                    self._word_dict[i] += 1
        return self._word_dict


    @property
    def wordlist(self):
        return self._wordlist


class TextPlotter(Plotter):
    def plot(self, data: Text):
        wc = WordCloud(background_color='white', font_path='经典行书简.TTF')
        wc.generate_from_frequencies(data.get_frequency())  # 生成词云图
        fig = plt.figure(1)
        plt.imshow(wc)  # 显示词云
        # plt.show()
        plt.axis('off')  # 关闭保存
        plt.savefig('wordcloud.jpg')
        print('Image has been saved!')


class Img:
    def __init__(self, imgs):
        """
        :param imgs: 图片路径或路径列表
        """
        self._imgs = []
        if type(imgs) == str:
            # 单一路径
            img = Image.open(imgs)
            self._imgs.append(img)
        elif type(imgs) == list:
            # 路径列表
            for img in imgs:
                temp = Image.open(img)
                self._imgs.append(temp)

    @property
    def images(self):
        return self._imgs

    def __len__(self):
        return len(self._imgs)


class ImagePlotter(Plotter):
    def plot(self, data, method, num):
        if type(data[0]) == str:
            # 是路径
            imgs = Img(data)
            images = imgs.images
        else:
            # 是图片
            images = data
        img_num = len(images)
        if method == 'column':
            columns = num
            if img_num % columns != 0:
                rows = img_num // columns + 1
            else:
                rows = img_num // columns
        elif method == 'row':
            rows = num
            if img_num % rows != 0:
                columns = img_num // rows + 1
            else:
                columns = img_num // rows
        else:
            raise Exception('Method Error!')
        plt.figure()
        for i in range(img_num):
            plt.subplot(rows, columns, i+1)
            plt.imshow(images[i])
            plt.axis('off')
        # plt.show()
        plt.savefig('pic.png')


class GifPlotter(Plotter):
    def plot(self, data, interval):
        """
        :param data:
        :param interval: 每帧画面停顿时间 单位为 ms
        :return:
        """
        if type(data[0]) == str:
            # 是路径
            imgs = Img(data)
            images = imgs.images
        else:
            # 是图片
            images = data
        img_num = len(images)
        i = 0
        fig, ax = plt.subplots()
        img = images[i]
        ax.imshow(img)
        ax.axis('off')

        def update(i):
            return ax.imshow(images[i])

        a = anime.FuncAnimation(fig, update, frames=range(img_num), interval=interval)
        a.save('Gif.gif', writer='pillow')
        # plt.show()


class Adapter:
    def _point_plot(self, data, *args, **kwargs):
        PointPlotter().plot(data, *args, **kwargs)

    def _array_plot(self, data, *args, **kwargs):
        ArrayPlotter().plot(data, *args, **kwargs)

    def _text_plot(self, data, *args, **kwargs):
        TextPlotter().plot(data, *args, **kwargs)

    def _image_plot(self, data, *args, **kwargs):
        ImagePlotter().plot(data, *args, **kwargs)

    def _gif_plot(self, data, *args, **kwargs):
        GifPlotter().plot(data, *args, **kwargs)

    def plot(self, data, *args, **kwargs):
        if type(data) == Text:
            self._text_plot(data, *args, **kwargs)
        elif type(data) == list:
            if type(data[0]) == Point:
                self._point_plot(data, *args, **kwargs)
            elif type(data[0]) == list:
                self._array_plot(data, *args, **kwargs)
            else:
                if 'interval' in kwargs:
                    self._gif_plot(data, *args, **kwargs)
                elif 'num' in kwargs:
                    self._image_plot(data, *args, **kwargs)





def main():

    p1 = Point(1, 1)
    p2 = Point(2, 1)
    a = Adapter()
    a.plot([p1, p2])
    print('-'*20+' PointPlotter '+'-'*20)
    # pplt = PointPlotter()
    # pplt.plot([p1,p2])

    a.plot([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print('-' * 20 + ' ArrayPlotter ' + '-' * 20)
    # ap = ArrayPlotter()
    # ap.plot([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    text = Text("Hi, I'm Harry Potter, nice to meet you!")
    a.plot(text)
    print('-' * 20 + ' TextPlotter ' + '-' * 20)
    # tp = TextPlotter()
    # tp.plot(text)

    os.chdir('imgs')
    img_path = os.listdir()
    a.plot(img_path, 'column', num=3)
    print('-' * 20 + ' ImagePlotter ' + '-' * 20)
    # ip = ImagePlotter()
    # ip.plot(img_path, 'column', 3)

    a.plot(img_path, interval=200)
    print('-' * 20 + ' GifPlotter ' + '-' * 20)
    # gp = GifPlotter()
    # gp.plot(img_path, 200)

    pass


if __name__ == '__main__':
    main()
