from GraphStat.GraphBuilder import node as nd
from GraphStat.GraphBuilder import graph as gh
from GraphStat.GraphBuilder import stat
from GraphStat.Visualization import plotgraph
from GraphStat.Visualization import plotnodes

NodeList = nd.init_node('newmovies.txt')
# print(NodeList)
# nd.print_node(NodeList[-1])
# x = nd.get_attribute(NodeList[0], 'Node Name')

Graph = gh.init_graph('newmovies.txt')
# print(Graph['EdgeList'][-1])
# gh.save_graph('graph1.txt', Graph)
# Graph1 = gh.load_graph('graph1.txt')
# print(Graph1['NodeList'][-1])
# x = stat.cal_average_degree(Graph)
# print(x)
# res = stat.cal_attr_distribute(Graph, 'Node Class')
# print(res)
# plotgraph.plot_degree_distribution(Graph)
# plotnodes.plot_nodes_attr(Graph, "Node Class")