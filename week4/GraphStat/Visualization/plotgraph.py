import matplotlib.pyplot as plt
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
    # print(dis_dict)