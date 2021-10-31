import os
from PIL import ImageFilter, Image
from matplotlib import pyplot as plt


class Filter:
    def __init__(self, image, **kwargs):
        self.image = image
        self.arg_dict = kwargs

    def set_image(self, img):
        self.image = img

    def get_image(self):
        return self.image

    def filter(self):
        pass


class FindEdges(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

    def filter(self):
        self.image = self.image.filter(ImageFilter.FIND_EDGES)


class Blur(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

    def filter(self):
        self.image = self.image.filter(ImageFilter.BLUR)


class Sharpen(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

    def filter(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)


class Adjust(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

    def filter(self):
        if self.arg_dict:
            width = self.arg_dict['width']
            height = self.arg_dict['height']
            self.image = self.image.resize((width, height))
        else:
            raise Exception('need width and height, given wrong!')


class ImageShop:
    def __init__(self, image_list=[]):
        self.flag = 0
        self.__ins_setted = 0
        self.__mode = ''
        self.__img_path = ''  # 是一个路径
        self.__img_instances = image_list
        if image_list:
            self.__ins_setted = 1
        self.__img_operated = []  # 处理过的图片

    def set_path(self, path, flag):
        """
        设定路径
        :param flag: 0表示是文件夹，1表示是文件
        :param path: 路径
        :return:
        """
        self.flag = flag
        self.__img_path = path

    def get_path(self):
        return self.__img_path

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
                self.__img_instances = self.__img_operated[:]
                if operations.index(i) < len(operations)-1:
                    self.clean_operated_imgs()

    def display(self, rows, columns, dpi):
        plt.figure(dpi=dpi)
        if self.__img_operated:
            num = len(self.__img_operated)
            for i in range(num):
                plt.subplot(rows, columns, i + 1)
                plt.imshow(self.__img_operated[i])
                plt.axis('off')
        else:
            num = len(self.__img_instances)
            for i in range(num):
                plt.subplot(rows, columns, i + 1)
                plt.imshow(self.__img_instances[i])
                plt.axis('off')
        plt.show()

    def save(self, rows, columns, path, filename, dpi):
        plt.figure(dpi=dpi)
        if self.__img_operated:
            num = len(self.__img_operated)
            for i in range(num):
                plt.subplot(rows, columns, i + 1)
                plt.imshow(self.__img_operated[i])
                plt.axis('off')
        else:
            num = len(self.__img_instances)
            for i in range(num):
                plt.subplot(rows, columns, i + 1)
                plt.imshow(self.__img_instances[i])
                plt.axis('off')
        if path:
            plt.savefig(path + '\\' + filename)
        else:
            plt.savefig(filename)
        print('image has been saves in {}'.format(os.getcwd()))

    def get_op_nums(self):
        return len(self.__img_operated)

    def get_ins_nums(self):
        return len(self.__img_instances)

    def get_operated_imgs(self):
        return self.__img_operated

    def if_loaded(self):
        if self.__ins_setted:
            return True
        else:
            return False


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
        if not self.shop.if_loaded():
            self.shop.set_path(filepath, flag)
            self.shop.set_mode(mode)
            self.shop.load_images()
        self.shop.clean_operated_imgs()
        op_list = []
        for i in range(4):
            if filter[i] == 1:
                if i != 3:
                    temp = (filter_names[i], -1)
                else:
                    if kwargs:
                        width = kwargs['width']
                        height = kwargs['height']
                        temp = (filter_names[i], (width, height))
                    else:
                        raise Exception
                op_list.append(temp)
        self.shop.batch_ps(op_list)
        op_num = self.shop.get_op_nums()
        if not op_num:
            op_num = self.shop.get_ins_nums()
        if plot[1] == 0:
            rows = plot[0]
            if (op_num % rows) != 0:
                columns = op_num // rows + 1
            else:
                columns = op_num // rows
        else:
            columns = plot[0]
            if (op_num % columns):
                rows = op_num // columns + 1
            else:
                rows = op_num // columns
        self.shop.display(rows, columns, dpi)
        self.shop.save(rows, columns, savepath, savename, dpi)

    def get_operated_imgs(self):
        return self.shop.get_operated_imgs()



def test_filter():
    im = Image.open('a.jpg')
    # im.show()
    # bl = Blur(im)
    # bl.filter()
    # im1 = bl.get_image()
    # im1.save('blur.png')
    fe = FindEdges(im)
    fe.filter()
    im2 = fe.get_image()
    # im2.save('findedges.png')
    # sp = Sharpen(im2)
    # sp.filter()
    # im3 = sp.get_image()
    # im3.save('sharpen.png')
    ad1 = Adjust(im, width=20, height=20)
    ad1.filter()
    im4 = ad1.get_image()
    im4.save('ad1.png')
    ad2 = Adjust(im, width=500, height=500)
    ad2.filter()
    im5 = ad2.get_image()
    im5.save('ad2.png')


if __name__ == '__main__':
    IS = ImageShop()
    tis = TestImageShop(IS)
    tis.operate_image(mode='jpg', filepath='imgs', savepath='', savename='FAimgs.png', flag=0, filter=(0, 1, 0, 1),
                      plot=(3, 1), dpi=300, width=1280, height=800)
    fa_imgs = tis.get_operated_imgs()
    IS1 = ImageShop(fa_imgs)
    tis1 = TestImageShop(IS1)
    tis1.operate_image(mode='jpg', filepath='imgs', savepath='', savename='FASimgs.png', flag=0, filter=(0, 0, 1, 1),
                      plot=(3, 1), dpi=300, width=1280, height=800)

