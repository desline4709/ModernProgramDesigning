import jieba


class Tokenizer:
    def __init__(self, chars: list, coding='c', PAD=0):
        """
        Tokenizer类的初始化，构建分词词典
        :param chars: 将要操作的文本，字符串列表
        :param coding: 表示分词模式，'c'表示按字分，'w'表示按词分
        :param PAD: 填充字符，默认为0
        """
        self.status = coding
        if self.status == 'c' or 'w':
            keys = chars
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
        else:
            raise Exception('Error!')

    def tokenize(self, sentence: str):
        """
        对输入的一句话返回分词列表
        :param sentence: 要分词的句子
        :return: 字符串列表
        """
        if self.status == 'c':
            res = list(sentence)
        elif self.status == 'w':
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
            while(length < seq_len):
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
            if tokens[i] != 0:
                try:
                    res += self.dec_char_dict[tokens[i]]
                except KeyError:
                    res += ' '
            else:
                res += '[PAD]'
        return res

    # def encode(self, seq_len: int):
    #     pass

if __name__ == '__main__':
    with open('jd_comments.txt', 'r', encoding='utf-8') as f:
        text = f.read().split('\n')
    with open('gbChineseCharacters.txt', 'r', encoding='utf-8') as f:
        zh_characters = ''
        zh_characters += f.readline().strip('\n')
        zh_characters += f.readline()
        zh_characters = list(zh_characters)
    # print(zh_characters[:])

    tok = Tokenizer(zh_characters)
    list_of_chars = tok.tokenize(text[0])
    # print(list_of_chars)
    tokens = tok.encode(list_of_chars)
    # print(tokens)
    tokens = tok.trim(tokens, 60)
    sentence = tok.decode(tokens)
    # print(sentence)