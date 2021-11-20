import numpy as np


class RandomWalk:
    def __init__(self, mu, X_0, sigma2, N):
        self._x_0 = X_0
        self._mu = mu
        self._sigma2 = sigma2
        self._N = N

    @property
    def x_0(self):
        return self._x_0

    @x_0.setter
    def x_0(self, value):
        self._x_0 = value

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, value):
        self._mu = value

    @property
    def sigma2(self):
        return self._sigma2

    @sigma2.setter
    def sigma2(self, value):
        self._sigma2 = value

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, value):
        self._N = value

    def walk(self):
        cot = 0
        x_list = [self._x_0]
        for i in range(self._N):
            if i == 0:
                x = self._x_0
            else:
                sigma = np.sqrt(self._sigma2)
                w_t = np.random.normal(self._mu, sigma, 1)
                x = float(self._mu + x_list[i-1] + w_t)
                x_list.append(x)
            yield x
            cot += 1
        return "现有的序列为{}".format(x_list)

    @property
    def params(self):
        return "参数如下：mu-{}, x_0-{}, sigma^2-{}, N-{}".format(self._mu, self._x_0, self._sigma2, self._N)


def main():
    '''
    RandomWalk

    test = RandomWalk(0, 0, 1, 5)
    for i in test.walk():
        print(i)
    print(test.params)
    '''


if __name__ == "__main__":
    main()