def init_node(path):
    """
    Return node list from node file
    :Param path: file path
    :Return: node list
    """
    with open(path, 'r') as f:
        fstr = f.read()
    
    index = fstr.find('*Edges')
    fstr = fstr[:index-1]
    flist = fstr.split('\n')[1:]

    keys = ['Node Id', 'Node Name', 'Weight', 'Node Class', 'Other Info']
    NodeList =[]
    for i in range(len(flist)):
        value = flist[i].split('\t')
        node = dict(zip(keys, value))
        NodeList.append(node)
    
    return NodeList

def print_node(node):
    """
    print all the info of a node
    :Param node: a node, as a dict of attributes and its value
    :Return: None
    """
    keys = ['Node Id', 'Node Name', 'Weight', 'Node Class', 'Other Info']
    res = "{1[0]}: {0[Node Id]}\n{1[1]}: {0[Node Name]}\n{1[2]}: {0[Weight]}\n{1[3]}: {0[Node Class]}\n{1[4]}: {0[Other Info]}".format(node, keys)
    print(res)

def get_attribute(node, attr):
    """
    get attr from node
    :Param node: a node, as a dict of attributes
    :Param attr: string, node attribute
    """
    try:
        res_str = "{}: {}".format(attr, node[attr])
        print(res_str)
    except:
        print('Attr Error!')