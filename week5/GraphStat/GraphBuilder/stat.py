def cal_average_degree(graph):
    """
    计算图的平均度
    :param graph:
    :return:
    """
    EdgeList = graph['EdgeList']
    NodeList = graph["NodeList"]
    # 总度数是边数的两倍
    degree = len(EdgeList) / 2
    res = degree / len(NodeList)
    return res

def cal_attr_distribute(graph, attr):
    """
    计算指定属性的分布
    :param graph:
    :param attr: 节点的属性'Node Id', 'Node Name', 'Weight', 'Node Class', 'Other Info'以及度 'degre'
    :return:
    """
    NodeList = graph['NodeList']
    EdgeList = graph['EdgeList']
    attr_num = {}
    if attr != 'degree':
        for i in NodeList:
            if i[attr] not in attr_num:
                attr_num[i[attr]] = 1
            else:
                attr_num[i[attr]] += 1
    else:
        # 计算度分布
        node_num = len(NodeList)
        keys = [str(i) for i in range(node_num)]
        attr_num = attr_num.fromkeys(keys, 0)
        # print(attr_num)
        for i in EdgeList:
            attr_num[i['Edge Id-1']] +=1
            attr_num[i['Edge Id-2']] +=1
    return attr_num

