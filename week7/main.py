from PIL import ImageFilter, Image


ImageFilter.BLUR

class Filter:
    def __init__(self, image, **kwargs):
        self.image = image
        self.arg_dict = kwargs

    def filter(self):
        pass

class Find_Edges(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(self, image, kwargs)

    def filter(self):
        image.filter(ImageFilter.FIND_EDGES)

class Blur(Filter):
    def __init__(self, image, **kwargs):
        super().__init__(self, image, kwargs)

    def filter(self):
        pass