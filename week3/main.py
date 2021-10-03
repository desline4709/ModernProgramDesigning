import jieba
import numpy as np


def clean():
    """
    本函数进行微博语句的分词，同时清洗分词数据

    :return:
    返回过滤后的分词情况
    """
    def init(weibolist, stopwordslist):
        # 读取微博数据
        with open("weibo.txt", 'r', encoding='utf-8') as f:
            weibolist += f.readlines()
        # 加载情绪词典
        jieba.load_userdict("emotion dict\\anger.txt")
        jieba.load_userdict("emotion dict\\disgust.txt")
        jieba.load_userdict("emotion dict\\fear.txt")
        jieba.load_userdict("emotion dict\\joy.txt")
        jieba.load_userdict("emotion dict\\sadness.txt")
        # 加载停用词表
        with open("stopwords.txt", "r", encoding='utf-8') as f:
            stopwordslist += f.read().split()
        if " " not in stopwordslist:
            stopwordslist += [' ']
        if "\n" not in stopwordslist:
            stopwordslist += ['\n']
        if "\t" not in stopwordslist:
            stopwordslist += ['\t']

    def cutting(sentence):
        return jieba.lcut(sentence)

    def filtering(wordlist):
        temp = []
        for i in wordlist:
            if i not in stopwords_list:
                temp += [i]
        return temp

    # 初始化数据结构
    split_list_filtered = []
    weibo_list = []
    stopwords_list = []
    init(weibo_list, stopwords_list)
    # print(weibo_list, stopwords_list)
    for i in weibo_list:
        x = cutting(i)
        y = filtering(x)
        split_list_filtered += [y]
    # print(split_list_filtered)
    return split_list_filtered


def emotion_analysing(wordlist, method):
    """
    进行情感分析

    传入分词后的结果以及使用的情感分析方法，其中每条微博分词后的结果应该是一维列表，method分为"vector"和"value"，对应返回的是情绪值还是情绪向量
    其中在外层函数传入method控制使用的内层函数，在内层函数传入分词结果

    :return:
    emotion: 情感分析结果
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


def main():
    splitwords = clean()
    ea = emotion_analysing(splitwords[0], method='vector')
    print(ea())


if __name__ == "__main__":
    main()
