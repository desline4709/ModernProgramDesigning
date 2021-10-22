import jieba


class Tokenizer:
    def __init__(self, chars: list, coding='c', PAD=0):
        """
        Tokenizer类的初始化，构建分词词典
        :param chars: 将要操作的文本，如微博数据、京东评论等，字符串列表
        :param coding: 表示分词模式，'c'表示按字分，'w'表示按词分
        :param PAD: 填充字符，默认为0
        """
        self.__status = coding
        self.__chars = chars
        self.__PAD = PAD
        temp = []
        for i in chars:
            if coding == 'c':
                temp += list(i)
            elif coding == 'w':
                temp += jieba.lcut(i)
            else:
                raise Exception('Error!')
        keys = list(set(temp))
        keys.insert(0, 'PAD')
        values = [i for i in range(len(keys))]

        if PAD != 0:
            if type(PAD) != int:
                # PAD是字符
                values[0] = PAD
            else:
                # PAD是非字符且非0
                raise TypeError("PAD can't be in this type")
        self.char_dict = dict(zip(keys, values))
        self.dec_char_dict = dict(zip(values, keys))

    def tokenize(self, sentence: str):
        """
        对输入的一句话返回分词列表
        :param sentence: 要分词的句子
        :return: 字符串列表
        """
        if self.__status == 'c':
            res = list(sentence)
        elif self.__status == 'w':
            res = jieba.lcut(sentence)
        else:
            raise Exception('Error!')
        return res

    def encode(self, list_of_chars: list):
        """
        输入分词的字符列表，返回字符的数字列表
        :param list_of_chars: 分词的字符列表
        :return: 数字列表
        """
        length = len(list_of_chars)
        res = [0 for i in range(length)]
        for i in range(length):
            try:
                res[i] = self.char_dict[list_of_chars[i]]
            except KeyError:
                res[i] = -1
                continue
        return res

    def trim(self, tokens: list, seq_len: int):
        """
        数字列表长度整理
        :param tokens: 数字列表
        :param seq_len: 要求的序列长度
        :return: 调整后的数字列表
        """
        length = len(tokens)
        res = tokens[:]
        if length < seq_len:
            while length < seq_len:
                res.append(self.char_dict['PAD'])
                length += 1
        elif length > seq_len:
            res = res[:seq_len]
        return res

    def decode(self, tokens):
        """
        将数字列表翻译回句子
        :param tokens: 数字列表
        :return: 完整句子的字符串
        """
        length = len(tokens)
        res = ''
        for i in range(length):
            if tokens[i] != self.__PAD:
                try:
                    res += self.dec_char_dict[tokens[i]]
                except KeyError:
                    res += ' '
            else:
                res += '[PAD]'
        return res

    def encode_all(self, seq_len: int):
        """
        返回所有文本(chars)的长度为seq_len的tokens
        :param seq_len: 指定长度
        :return: tokens list
        """
        res = []
        for i in self.__chars:
            res.append(self.trim(self.encode(self.tokenize(i)), seq_len))
        return res


def main():
    with open('jd_comments.txt', 'r', encoding='utf-8') as f:
        text = f.read().split('\n')[:-1]

    tok_c = Tokenizer(text, coding='c')
    tok_w = Tokenizer(text, coding='w')
    list_of_chars_1 = tok_c.tokenize(text[-1])
    list_of_chars_2 = tok_w.tokenize(text[-1])
    # print('list_of_chars1: {}'.format(list_of_chars_1))
    # print('list_of_chars2: {}'.format(list_of_chars_2))
    tokens1 = tok_c.encode(list_of_chars_1)
    tokens2 = tok_w.encode(list_of_chars_2)
    tokens1 = tok_c.trim(tokens1, 20)
    tokens2 = tok_w.trim(tokens2, 20)
    # print('tokens1: {}'.format(tokens1))
    # print('tokens2: {}'.format(tokens2))
    sentence1 = tok_c.decode(tokens1)
    sentence2 = tok_w.decode(tokens2)
    # print('sentence1(without trim): {}'.format(sentence1))
    # print('sentence2(without trim): {}'.format(sentence2))
    # print('sentence1: {}'.format(sentence1))
    # print('sentence2: {}'.format(sentence2))
    txt1 = tok_c.encode_all(80)
    txt2 = tok_w.encode_all(80)
    # print('text1_all: {}'.format(txt1))
    # print('text2_all: {}'.format(txt2))




if __name__ == '__main__':
    main()