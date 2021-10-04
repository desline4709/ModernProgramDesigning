import jieba
import numpy as np
import re


def load_data(path, mode=0):
    """
    加载本地数据，只读取txt文本
    :param path: 文件相对位置
    :param mode: 加载文件的模式，0表示正常按行读取，1表示读取后的结果每条去掉末尾的换行符
    :return: 数据列表
    """
    with open(path, 'r', encoding='utf-8') as f:
        if mode == 0:
            data = f.readlines()
        elif mode == 1:
            data = f.read().split()
        else:
            raise Exception('Error mode')
    return data



def clean(wb_data, sw_data):
    """
    本函数进行微博语句的清洗
    :param wb_data: 微博分词数据
    :param sw_data: 停用词表
    :return:返回清洗后的分词情况
    """

    def cutting(wb_data):
        """
        将微博数据进行分词
        :param wb_data: 微博元数据
        :return: 分词后的二维列表
        """

        def init():
            # 加载情绪词典
            jieba.load_userdict("emotion dict\\anger.txt")
            jieba.load_userdict("emotion dict\\disgust.txt")
            jieba.load_userdict("emotion dict\\fear.txt")
            jieba.load_userdict("emotion dict\\joy.txt")
            jieba.load_userdict("emotion dict\\sadness.txt")

        init()
        split_list = []
        for wb in wb_data:
            split_list += [jieba.lcut(wb)]
        return split_list

    def remove_urls(wb_data):
        """
        去除微博文本中的URL
        :param wb_data: 微博元数据
        :return: 去除url后的微博数据
        """
        temp = []
        for wb in wb_data:
            try:
                end_index = re.search(r'https?://([\w-]+\.)+[\w-]+(/[\w./?%&=]*)?', wb).span()[0]  # 找到url的起始位置
                temp.append(wb[:end_index])
            except AttributeError:
                temp.append(wb)
        return temp

    def filtering(wordlist):
        """
        过滤停用词
        :param wordlist: 一条微博的分词列表
        :return: 过滤停用词后的分词列表
        """
        temp = []
        for i in wordlist:
            if i not in stopwords_list:
                temp += [i]
        # print(temp)
        return temp

    # 初始化数据结构
    split_list_filtered = []
    stopwords_list = sw_data
    wb_no_urls = remove_urls(wb_data)
    split_list = cutting(wb_no_urls)
    for i in split_list:
        y = filtering(i)
        split_list_filtered += [y]
    # print(split_list_filtered)
    return split_list_filtered


def emotion_analysing(wordlist, method):
    """
    进行情感分析

    传入分词后的结果以及使用的情感分析方法，其中每条微博分词后的结果应该是一维列表，method分为"vector"和"value"，对应返回的是情绪值还是情绪向量
    其中在外层函数传入method控制使用的内层函数，在内层函数传入分词结果

    :return:情感分析结果
    """
    with open("emotion dict\\anger.txt", "r", encoding='utf-8') as a:
        x = a.read().split()
        y = [1 for i in range(len(x))]
        anger_dict = dict(zip(x, y))
    with open("emotion dict\\disgust.txt", "r", encoding='utf-8') as a:
        x = a.read().split()
        y = [1 for i in range(len(x))]
        disgust_dict = dict(zip(x, y))
    with open("emotion dict\\fear.txt", "r", encoding='utf-8') as a:
        x = a.read().split()
        y = [1 for i in range(len(x))]
        fear_dict = dict(zip(x, y))
    with open("emotion dict\\joy.txt", "r", encoding='utf-8') as a:
        x = a.read().split()
        y = [1 for i in range(len(x))]
        joy_dict = dict(zip(x, y))
    with open("emotion dict\\sadness.txt", "r", encoding='utf-8') as a:
        x = a.read().split()
        y = [1 for i in range(len(x))]
        sadness_dict = dict(zip(x, y))
    # print(anger_dict)

    def vector():
        """
        返回情绪向量的方法，情绪向量的构成为 (anger, disgust, fear, joy, sadness)

        :return: 返回情绪向量，表示每个情绪词的个数比例
        """
        nonlocal wordlist
        num_vec = np.zeros(5)
        for word in wordlist:
            print(word)
            if word in anger_dict:
                num_vec[0] += anger_dict[word]
            elif word in disgust_dict:
                num_vec[1] += disgust_dict[word]
            elif word in fear_dict:
                num_vec[2] += fear_dict[word]
            elif word in joy_dict:
                num_vec[3] += joy_dict[word]
            elif word in sadness_dict:
                num_vec[4] += sadness_dict[word]
        num_total = np.sum(num_vec)
        if num_total == 0:
            res = num_vec
        else:
            res = num_vec / num_total
        return res

    def value():
        """
        返回情绪值（字符串）的方法，情绪向量的构成为 (anger, disgust, fear, joy, sadness)

        :return: 返回情绪向量，表示每个情绪词的个数比例
        """
        nonlocal wordlist
        rate_vec = vector()
        if max(rate_vec) == min(rate_vec):
            # 最大和最小相同（已经包括全是0的情况），表示无情绪
            res = '无情绪'
        else:  # 还有情绪冲突的情况未处理
            pass

    # def vector():
    #     pass
    #
    # def value():
    #     pass

    if method == 'vector':
        return vector
    elif method == 'value':
        return value


def emotion_timemode(wordlist, mode):
    """
    传入分词词表并制定返回模式，返回对应情绪的指定模式

    :param wordlist:
    :param mode: 控制返回的模式，包括小时、天、周等
    :return: 对应情绪的指定模式
    """


def main():
    wb_data = load_data('weibo.txt')

    sw_data = load_data('stopwords.txt', 1)
    if " " not in sw_data:
        sw_data += [' ']
    if "\n" not in sw_data:
        sw_data += ['\n']
    if "\t" not in sw_data:
        sw_data += ['\t']

    filteredwords = clean(wb_data, sw_data)
    # print(filteredwords == splitwords)
    # print(filteredwords)
    # ea = emotion_analysing(filteredwords[0], method='vector')



if __name__ == "__main__":
    main()
