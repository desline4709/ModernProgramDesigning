class Tokenizer():
    def __init__(self, chars: list, coding='c', PAD=0):
        if coding == 'c':
            keys = chars
            keys.insert('PAD')
            values = [i for i in range(len(keys))]
            char_dict = dict(zip(keys, values))
        elif coding == 'w':
            pass
        else:
            raise Exception('Error!')