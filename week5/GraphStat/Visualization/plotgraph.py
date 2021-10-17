import matplotlib.pyplot as plt
import numpy as np
from GraphStat.GraphBuilder import stat

def plot_degree_distribution(graph):
    """
    画出度分布
    :param graph:
    """
    NodeList = graph['NodeList']
    node_dict = stat.cal_attr_distribute(graph, 'degree')
    # node_num = len(NodeList)
    # edge_num_fullconnected = int(node_num * (node_num-1) /2)
    # edge_keys = [i for i in range(edge_num_fullconnected)]
    dis_dict = {}
    for i in node_dict:
        if node_dict[i] not in dis_dict:
            dis_dict[node_dict[i]] = 1
        else:
            dis_dict[node_dict[i]] +=1
    dis_dict = dict(sorted(dis_dict.items(), key=lambda item:item[1], reverse=True))

    dict_num = len(dis_dict)
    x = np.arange(dict_num)
    y = list(dis_dict.values())
    labels = [str(i) for i in dis_dict]
    bar_width = 0.5
    plt.figure(0,figsize=(80,10),dpi=300)
    plt.bar(x, y, bar_width)
    plt.xticks(x, labels)
    for i in range(len(x)):
        plt.text(x[i]-0.35,y[i]+0.5,str(y[i]), fontsize = 6)
    plt.title('节点度分布', fontfamily='SimHei', fontsize = 15)
    plt.xlabel('节点度数', fontfamily='SimHei', fontsize = 15)
    plt.ylabel('频数', fontfamily='SimHei', fontsize = 15)
    plt.savefig('度分布.png')
    plt.show()