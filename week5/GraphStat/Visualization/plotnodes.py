import matplotlib.pyplot as plt
from GraphStat.GraphBuilder import stat
import numpy as np

def plot_nodes_attr(graph, feature):
    """
    画出图的制定属性的分布
    :param graph:
    :param feature:
    :return:
    """
    attr_num_dict = stat.cal_attr_distribute(graph, feature)
    num = len(attr_num_dict)
    x = np.arange(num)
    y = list(attr_num_dict.values())
    labels = list(attr_num_dict.keys())
    plt.figure()
    bar_width = 0.5
    plt.bar(x, y, bar_width)
    plt.xticks(x, labels)
    plt.title("{}的分布图".format(feature), fontfamily = 'SimHei')
    for i in range(num):
        plt.text(x[i]-0.15, y[i]+0.5, str(y[i]))
    plt.savefig("{}的分布图".format(feature))
    plt.show()
