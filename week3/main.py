import jieba
import re
import numpy as np
import time


def load_data(path, mode=0):
    """
    加载本地数据，只读取txt文本
    :param path: 文件相对位置
    :param mode: 加载文件的模式，0表示正常按行读取，1表示读取后的结果每条去掉末尾的换行符，2表示读取为1类型且值为1的字典
    :return: 数据列表
    """
    with open(path, 'r', encoding='utf-8') as f:
        if mode == 0:
            data = f.readlines()
        elif mode == 1:
            data = f.read().split()
        elif mode == 2:
            data1 = f.read().split()
            lis = [1 for i in range(len(data1))]
            data = dict(zip(data1, lis))
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


def emotion_analysing(method):
    """
    进行情感分析，传入分词后的结果以及使用的情感分析方法，其中每条微博分词后的结果应该是一维列表，
    :param method: method分为"vector"和"value"，对应返回的是情绪值还是情绪向量
    其中在外层函数传入method控制使用的内层函数，在内层函数传入分词结果
    :return:情感分析结果
    """
    anger_dict = load_data("emotion dict\\anger.txt", 2)
    disgust_dict = load_data("emotion dict\\disgust.txt", 2)
    fear_dict = load_data("emotion dict\\fear.txt", 2)
    joy_dict = load_data("emotion dict\\joy.txt", 2)
    sadness_dict = load_data("emotion dict\\sadness.txt", 2)
    # print(anger_dict)

    def vector(wordlist):
        """
        返回情绪向量的方法，情绪向量的构成为 (anger, disgust, fear, joy, sadness)

        :return: 返回情绪向量，表示每个情绪词的个数比例
        """
        num_vec = [0 for i in range(5)]
        for word in wordlist:
            # print(word)
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
        num_total = sum(num_vec)
        if num_total == 0:
            res = num_vec
        else:
            res = [(i/num_total) for i in num_vec]
        return res

    def value(wordlist):
        """
        返回情绪值（字符串）的方法，情绪向量的构成为 (anger, disgust, fear, joy, sadness)

        :return: 返回情绪向量，表示每个情绪词的个数比例
        """
        rate_vec = vector(wordlist)
        em_flag = ['single', 'mixed', 'plain']  # 单一情绪，多情绪混合，无显著情绪
        em_tag = ['angry', 'disgusting', 'fear', 'joy', 'sad']  # 详细的情绪标签
        if max(rate_vec) == min(rate_vec):
            # 最大和最小相同（已经包括全是0的情况），表示无显著情绪
            res = (em_flag[2], -1)
        elif rate_vec.count(max(rate_vec)) >1 :
            # 出现重复的最大值时，混合情绪
            res = (em_flag[1], -1)
        else:
            # 有独立最大值，单一情绪
            res = (em_flag[0], em_tag[rate_vec.index(max(rate_vec))])
        return res

    if method == 'vector':
        return vector
    elif method == 'value':
        return value


def emotion_tagging(wb_data, method):
    """
    给每条微博数据进行情绪标记
    :param wb_data: 微博数据列表
    :param method: 采用的情绪判定方法，'vector'或'value'
    :return: 返回情绪标记列表
    """
    res = []
    em_tagging = emotion_analysing(method)
    for i in wb_data:
        tag = em_tagging(i)
        res.append(tag)
    return res


def extract_time(wb_data):
    """
    提取时间信息
    :param wb_data: 微博元数据
    :return: 时间戳的列表
    """
    timetick_list = []
    re_str = '(?P<week>\w{3}) (?P<mon>\w{3}) (?P<day>\d+) (?P<time>\d+:\d+:\d+) (?P<zone>\+\d+) (?P<year>\d{4})'
    for wb in wb_data:
        totaltime_str = re.search(re_str, wb)
        timetick_list.append(time.mktime(time.strptime(totaltime_str.group(),"%a %b %d %H:%M:%S %z %Y")))
    return timetick_list


def emotion_timemode(wbemo_tag, time_list, mood, timemode, method):
    """
    传入标签列表并制定返回模式，返回对应情绪的指定模式，经分析，微博数据时间分布从2013.10.11零点-2013.10.13零点共两天的时间
    :param wbemo_tag:微博情绪标签列表
    :param mood: 情绪
    :param timemode: 控制返回的模式，包括小时(hour--0)、固定时段(fixed--1)、天(day--2)等
    :param method: 指定计量情绪的方法，'vector' 或 'value'
    :return: 对应情绪的指定模式
    """
    start_str = '2013 Oct 11 00:00:00'  # 开始时间
    end_str = '2013 Oct 13 01:00:00'  # 结束时间
    start_tick = time.mktime(time.strptime(start_str, "%Y %b %d %X"))  # 转换为时间戳
    end_tick = time.mktime(time.strptime(end_str, "%Y %b %d %X"))
    hour_num = int((end_tick - start_tick) // 3600)  # 一共几个小时
    em_flag = ['single', 'mixed', 'plain']  # 单一情绪，多情绪混合，无显著情绪
    em_flag_cot = [0 for i in range(len(em_flag))]  # flag计数器
    em_tag = ['angry', 'disgusting', 'fear', 'joy', 'sad']  # 详细的情绪标签
    em_tag_cot = np.zeros(len(em_tag))
    em_flag_cot_arr = [np.zeros(len(em_flag) * hour_num).reshape((hour_num, len(em_flag))),
                       np.zeros(len(em_flag) * 24).reshape((24, len(em_flag))),
                       np.zeros(len(em_flag) * 3).reshape((3, len(em_flag)))]  # 分别代表3种模式的计数器，3维数组
    em_tag_cot_arr = [np.zeros(len(em_tag) * 49).reshape((49, len(em_tag))),
                       np.zeros(len(em_tag) * 24).reshape((24, len(em_tag))),
                       np.zeros(len(em_tag) * 3).reshape((3, len(em_tag)))]
    em_vecnum_arr = [np.zeros(hour_num), np.zeros(24), np.zeros(3)]  # 每个模式下对应向量的计数器
    em_tagnum = 0  # 计算非零的向量标签总数

    def vector():
        nonlocal em_tag_cot, em_flag_cot, em_tagnum
        for i in range(len(wbemo_tag)):
            # vector计量情绪，只有情绪比例;wbemo_tag是二维列表
            em_tag_cot += np.array(wbemo_tag[i])
            try:
                if timemode == 0:
                    time_index = int((time_list[i] - start_tick) //3600)
                elif timemode == 1:
                    time_index = eval(time.strftime("%H", time.localtime(time_list[i])))
                elif timemode == 2:
                    time_index = int((time_list[i] - start_tick) // (3600*24))
                em_tag_cot_arr[timemode][time_index] += np.array(wbemo_tag[i])
                if np.sum(wbemo_tag[i]) != 0:
                    em_vecnum_arr[timemode][time_index] += 1
                    em_tagnum += 1
            except NameError:
                raise Exception('No time_index')
            except IndexError:
                raise Exception('Wrong index')
        em_tag_cot = em_tag_cot / em_tagnum  # 总的情绪比例
        # print(np.sum(em_tag_cot_arr[timemode]))
        # print(np.sum(em_vecnum_arr[timemode]))
        # print(em_tagnum, em_tag_cot)
        try:
            if timemode == 0:
                num_of_index = hour_num
            elif timemode == 1:
                num_of_index = 24
            elif timemode == 2:
                num_of_index = 3
            for hour in range(num_of_index):
                em_tag_cot_arr[timemode][hour] /= em_vecnum_arr[timemode][hour]
        except:
            raise Exception('No num_of_index')
        return em_tag_cot, em_tag_cot_arr[timemode]

    def value():
        pass

    if method == 'vector':
        return vector
    elif method == 'value':
        value()


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
    wb_value_tag = emotion_tagging(wb_data, 'value')
    wb_vector_tag = emotion_tagging(wb_data, 'vector')

    time_list = extract_time(wb_data)
    wb_vector_res, wb_vector_hour_res = emotion_timemode(wb_vector_tag, time_list, 'joy', 0, 'vector')()
    # print(wb_vector_res)


if __name__ == "__main__":
    main()
