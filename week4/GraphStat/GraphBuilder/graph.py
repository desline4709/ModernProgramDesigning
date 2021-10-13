import pickle as pkl


def init_graph(path):
    """
    return a dict of vertices and edges
    :param path: the path of graph file
    :return: a dict of vertices and edges with keys NodeList and EdgeList
    """
    with open(path, 'r', encoding='utf-8') as f:
        fstr = f.read()

    index = fstr.find('*Edge')
    ver_keys = ['Node Id', 'Node Name', 'Weight', 'Node Class', 'Other Info']
    vertices = fstr[:index - 1].split('\n')[1:]
    edges = fstr[index:].split('\n')[1:-1]
    edg_keys = ['Edge Id-1', 'Edge Id-2', 'Edge Weight']

    NodeList = []
    EdgeList = []
    for i in range(len(vertices)):
        value = vertices[i].split('\t')
        node = dict(zip(ver_keys, value))
        NodeList.append(node)
    for i in range(len(edges)):
        value = edges[i].split('\t')
        edge = dict(zip(edg_keys, value))
        EdgeList.append(edge)
    res = {'NodeList': NodeList, 'EdgeList': EdgeList}
    return res


def save_graph(filepath, graph):
    """
    save the graph
    :param filepath: path of the saving file
    :param graph:
    :return: None
    """
    with open(filepath, 'wb') as f:
        pkl.dump(graph, f)
    print('Graph Saved')


def load_graph(filepath):
    """
    load graph from savings
    :param filepath:
    :return: graph
    """
    with open(filepath, 'rb') as f:
        res = pkl.load(f)
    print('Graph Loaded')
    return res