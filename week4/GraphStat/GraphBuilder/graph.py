def init_graph(path):
    """
    return a dict of vertices and edges
    :Param path: the path of graph file
    :Return: a dict of vertices and edges
    """
    with open(path, 'r') as f:
        fstr = f.read()
    
    index = fstr.find('*Edge')
    ver_keys = ['Node Id', 'Node Name', 'Weight', 'Node Class', 'Other Info']
    vertices = fstr[:index-1].split('\n')[1:]
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
    res = {'NodeList':NodeList, 'EdgeList':EdgeList}
    return res

