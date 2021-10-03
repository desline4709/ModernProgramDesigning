import jieba
import numpy as np
from wordcloud import WordCloud  #词云
from PIL import Image
import matplotlib.pyplot as plt


class Documents:
    def __init__(self):
        self.document_list = []
        self.stopwords_list = []
        self.split_list = []
        self.split_list_filtered = []
        self.features_set = {0}
        self.vectors_list = []
        self.gravity_center = 0
        with open('jd_comments.txt', 'r', encoding='utf-8') as f:
            self.document_list = f.readlines()
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            self.stopwords_list = f.read().split('\n')
        if ('\n' not in self.stopwords_list):
            self.stopwords_list.append('\n')
        print(self.stopwords_list)

    def getDocuments(self):
        for doc in self.document_list:
            print(doc)

    def wordSplitting(self):
        # jieba分词
        for doc in self.document_list:
            self.split_list.append(jieba.lcut(doc))

    def filtering(self):
        # 利用停用词表删除不要的词
        assert(len(self.stopwords_list) != 0)  # self.stopwords_list为空时报错
        y = []
        for doc in self.split_list:
            x = []
            for word in doc:
                if (word not in self.stopwords_list):
                    x.append(word)
                # else:
                #     print(word)
            self.split_list_filtered.append(x)
        # print(self.split_list_filtered)
        # print(self.split_list)

    def calculating(self):
        wordlist = []
        numlist = []
        for doc in self.split_list_filtered:
            for word in doc:
                if (word not in wordlist):
                    wordlist.append(word)
                    numlist.append(1)
                else:
                    index = wordlist.index(word)
                    numlist[index] += 1
        self.word_dict = dict(zip(wordlist, numlist))  # 通过zip合成一个字典
        print('词频如下：\n')
        print(self.word_dict)

    def getFeatures(self, frequency):
        self.features_set.discard(0)
        for word in self.word_dict:
            if (self.word_dict[word] > frequency):
                self.features_set.add(word)
        print('词频大于100的高频词（特征集）：\n')
        print(self.features_set)

    def vectorization(self):
        dim = len(self.features_set)
        features_list = list(self.features_set)
        assert (dim > 1)  # dim <= 1时，抛出异常
        for doc in self.document_list:
            vec = np.zeros(dim)
            for feature in features_list:
                if (feature in doc):
                    index = features_list.index(feature)
                    vec[index] = 1
            self.vectors_list.append(vec)
        print('向量化表示：\n')
        print(self.vectors_list)

    def getGravityCenter(self):
        def getDistance(vec_x, vec_y):
            # vec_x 和vec_y均为ndarray类型；采用欧氏距离计算
            distance = np.sqrt(np.sum(np.square(vec_x - vec_y)))
            return distance

        def getRepresent():
            dis_list = []
            assert(type(self.gravity_center) == np.ndarray) # 不是ndarray类型时抛出异常
            for vec in self.vectors_list:
                dis = getDistance(vec, self.gravity_center)
                dis_list.append(dis)
            min_index = dis_list.index(min(dis_list))
            return min_index

        num = len(self.vectors_list)
        center = 0
        for vec in self.vectors_list:
            center += vec
        center = center / num
        self.gravity_center = center
        rep_index = getRepresent()
        print('代表性文档是：\n')
        print(self.document_list[rep_index])

    def getWordloud(self):
        wc = WordCloud(background_color='white', font_path='经典行书简.TTF')
        wc.generate_from_frequencies(self.word_dict)  # 生成词云图
        fig = plt.figure(1)
        plt.imshow(wc)  # 显示词云
        #plt.show()
        plt.axis('off')  # 关闭保存
        plt.savefig('wordcloud.jpg')
        print('Image has been saved!')

def main():
    d = Documents()
    # d.wordSplitting()
    # d.filtering()
    # d.calculating()
    # d.getFeatures(100)
    # d.vectorization()
    # d.getGravityCenter()
    # d.getWordloud()


if __name__ == '__main__':
    main()
