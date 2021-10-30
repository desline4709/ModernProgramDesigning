import os
from PIL import ImageFilter, Image
from matplotlib import pyplot as plt
from . import mpsettings

class Filter:
    def __init__(self, image, **kwargs):
        self.__image = image
        self.arg_dict = kwargs

    def set_image(self,img):
        self.__image = img

    def get_image(self):
        return self.__image

    def filter(self):
        pass


class FindEdges(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

    def filter(self):
        self.__image = self.__image.filter(ImageFilter.FIND_EDGES)


class Blur(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

    def filter(self):
        img = self.__image.filter(ImageFilter.BLUR)
        return img


class Sharpen(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

    def filter(self):
        img = self.__image.filter(ImageFilter.SHARPEN)
        return img


class Adjust(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

    def filter(self):
        if self.arg_dict:
            width = self.arg_dict['width']
            height = self.arg_dict['height']
            self.__image = self.__image.resize((width, height))
        else:
            raise Exception('need width and height, given wrong!')


class ImageShop:
    def __init__(self):
        self.flag = 0
        self.__mode = ''
        self.__img_path = ''  # 是一个路径
        self.__img_instances = []
        self.__img_operated = []  # 处理过的图片

    def set_path(self,path,flag):
        """
        设定路径
        :param flag: 0表示是文件夹，1表示是文件
        :param path: 路径
        :return:
        """
        self.flag = flag
        self.__img_path = path

    def clean_operated_imgs(self):
        self.__img_operated = []

    def set_mode(self, mode):
        self.__mode = mode

    def load_images(self):
        files_list = os.listdir(self.__img_path)
        img_list = []
        if self.flag == 0:
            for i in files_list:
                if i.split('.')[1] == self.__mode:
                    img_list.append(i)
            for i in img_list:
                self.__img_instances.append(Image.open(self.__img_path + '\\' + i))
        elif self.flag == 1:
            self.__img_instances.append(Image.open(self.__img_path))

    def __batch_ps(self, f: Filter):
        for i in self.__img_instances:
            f.set_image(i)
            f.filter()
            self.__img_operated.append(f.get_image())

    def batch_ps(self, operations: list):
        """
        批处理图片
        :param operations: list of tuple,tuple(filter,paras),if no paras ,set (filter,-1)
        :return:
        """
        filters = [Blur, FindEdges, Sharpen, Adjust]
        filter_names = ['blur', 'find_edges', 'sharpen', 'adjust']
        if operations:
            for i in operations:
                if i[0] != 'adjust':
                    f = filters[filter_names.index(i[0])](Image)
                else:
                    # 默认adjust传的参数为('adjust',(width,height))
                    f = filters[filter_names.index(i[0])](Image, width=i[1][0], height=i[1][1])
                self.__batch_ps(f)

    def display(self, rows, columns, dpi):
        plt.figure(dpi=dpi)
        num = len(self.__img_operated)
        for i in range(num):
            plt.subplot(rows, columns, i+1)
            self.__img_operated[i].show()
        plt.show()

    def save(self, rows, columns, path, filename, dpi):
        plt.figure(dpi=dpi)
        num = len(self.__img_operated)
        for i in range(num):
            plt.subplot(rows, columns, i+1)
            self.__img_operated[i].show()
        plt.savefig(path+'\\'+filename)

    def get_op_nums(self):
        return len(self.__img_operated)


class TestImageShop:
    def __init__(self, imgshop: ImageShop):
        self.shop = imgshop

    def operate_image(self, mode, filepath, savepath, savename, flag, filter: tuple, plot, dpi, **kwargs):
        """
        对图片进行操作
        :param mode: 指定图片模式
        :param filepath: 图片路径
        :param savepath: 保存路径
        :param savename: 保存名字
        :param flag: 1-文件 or 0-文件夹
        :param filter: 一个长度为4的元组，分别代表是否使用 'blur', 'find_edges', 'sharpen', 'adjust' 滤镜
        :param plot: 一个元组 (行数或列数,按行或按列) 按行-0，按列-1
        :param dpi: 图片清晰度
        :param kwargs: 如果有adjust，必须有width和height；
        :return:
        """
        filter_names = ['blur', 'find_edges', 'sharpen', 'adjust']
        self.shop.set_path(filepath, flag)
        self.shop.set_mode(mode)
        self.shop.load_images()
        self.shop.clean_operated_imgs()
        op_list = []
        for i in range(4):
            if filter[i] == 1:
                if i != 3:
                    temp = (filter[i], -1)
                else:
                    if kwargs:
                        width = kwargs['width']
                        height = kwargs['height']
                        temp = (filter[i], (width, height))
                    else:
                        raise Exception
                op_list.append(temp)
        self.shop.batch_ps(op_list)
        op_num = self.shop.get_op_nums()
        if plot[1] == 0:
            rows = plot[0]
            columns = op_num // rows + 1
        else:
            columns = plot[0]
            rows = op_num // columns + 1
        self.shop.display(rows, columns, dpi)
        self.shop.save(rows, columns, savepath, savename, dpi)



if __name__ == '__main__':
    im = Image.open('a.jpg')
    # im.show()
    bl = Blur(im)
    im1 = bl.filter()
    # im1.show()
    fe = FindEdges(im)
    im2 = fe.filter()
    im2.show()
    sp = Sharpen(im2)
    im3 = sp.filter()
    # im3.show()
    ad = Adjust(im)
    im4 = ad.filter(500, 500)
    # sim4.show()