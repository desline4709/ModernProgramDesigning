import jieba


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

def emotion_analysing(splitlist, **method):
    """
    进行情感分析

    传入分词后的结果以及使用的情感分析方法，其中分词后的结果应该是二维列表，method分为"vector"和"value"，对应返回的是情绪值还是情绪向量

    :return:
    emotion: 情感分析结果
    """
    anger_dict = {}
    disgust_dict = {}
    fear_dict = {}
    joy_dict = {}
    sadness_dict = {}
    def loading_dict():
        with open("emotion dict\\anger.txt", "r", encoding='utf-8') as a:
            x = a.read().split()
            y = [1 for i in range(len(x))]
            nonlocal anger_dict
            anger_dict = dict(zip(x, y))
        with open("emotion dict\\disgust.txt", "r", encoding='utf-8') as a:
            x = a.read().split()
            y = [1 for i in range(len(x))]
            nonlocal disgust_dict
            disgust_dict = dict(zip(x, y))
        with open("emotion dict\\fear.txt", "r", encoding='utf-8') as a:
            x = a.read().split()
            y = [1 for i in range(len(x))]
            nonlocal fear_dict
            fear_dict = dict(zip(x, y))
        with open("emotion dict\\joy.txt", "r", encoding='utf-8') as a:
            x = a.read().split()
            y = [1 for i in range(len(x))]
            nonlocal joy_dict
            joy_dict = dict(zip(x, y))
        with open("emotion dict\\sadness.txt", "r", encoding='utf-8') as a:
            x = a.read().split()
            y = [1 for i in range(len(x))]
            nonlocal sadness_dict
            sadness_dict = dict(zip(x, y))
    loading_dict()
    # print(anger_dict)



def main():
    splitlist = clean()
    emotion_analysing(splitlist)

if __name__ == "__main__":
    main()