import networkx as nx
import matplotlib.pyplot as plt


G=nx.Graph()

G.add_node('ITB', pos=(-6.893218,107.610454))
G.add_node('SR', pos=(-6.893776,107.612961 ))
G.add_node('Dago', pos=(-6.887364,107.613542))
G.add_node('Mcd Dago', pos=(-6.885198,107.61375))
G.add_node('Hokben', pos=(-6.885250,107.612913))
G.add_node('Siliwangi', pos=(-6.884937,107.611520))
G.add_node('DS1', pos=(-6.886412,107.611706))
G.add_node('DS2',pos=(-6.887245,107.611489))
G.add_node('SBM',pos=(-6.887853,107.608307))
G.add_node('Sipil',pos=(-6.893838,107.608571))
G.add_weighted_edges_from([('ITB', 'SR', 10), ('ITB', 'Sipil',10), ('SR','Dago',100),('Dago','Mcd Dago',8),('Mcd Dago', 'Hokben',88),('Hokben', 'Siliwangi',76),('Hokben','DS1',80),('Siliwangi','DS1',66),('DS1','DS2',69),('DS2','SBM',70),('DS2','Dago',88),('SBM','Sipil',100)])


#elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 50]
#esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 50]

#positioin
pos = nx.get_node_attributes(G, 'pos')
#labels
labels = nx.get_edge_attributes(G, 'weight')
# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

#biar ada weight
nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)
nx.draw(G,pos,node_color='blue',with_labels=True)
plt.show()
#warna sisi edges
#nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
#nx.draw_networkx_edges(
#    G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
#)
asu=input("awalnya :")
asi=input("akhirnya :")

p = nx.shortest_path(G, source=asu,target=asi)

#positioin
pos = nx.get_node_attributes(G, 'pos')
#labels
labels = nx.get_edge_attributes(G, 'weight')
# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

#biar ada weight
nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)

print(p)

# Set all edge color attribute to black
for e in G.edges():
    G[e[0]][e[1]]['color'] = 'black'
# Set color of edges of the shortest path to green
for i in range(len(p)-1):
    G[p[i]][p[i+1]]['color'] = 'blue'
# Store in a list to use for drawing
edge_color_list = [ G[e[0]][e[1]]['color'] for e in G.edges() ]
node_colors = ["red" if n in p else "blue" for n in G.nodes()]

nx.draw(G,pos,node_color=node_colors,edge_color = edge_color_list, with_labels = True)
plt.show()




