#!/usr/bin/env python
# coding: utf-8

# In[168]:


"""
Weighted Graph generator
Generate nodes and edges with weighted value
use getweigt() function to get weight between two nodes
and use getnearnodes() to get nodes near a node
the weight and node's values are saved in a single dictionary variable called totale
"""


import matplotlib.pyplot as plt
import networkx as nx
import random

G = nx.Graph()
nodesname = "sabcdefghijklmnopqrtuvwxyz"
nodes = 15 #nodes should be more than one and less than 26
edgescarcity = 4 #density = 1: all nodes are connected, edge generation probablity = 1/scarcity

for i in range (nodes):
    for n in range(i+1):
        if i != n and random.randint(1,edgescarcity) == 1: #node net density can be changed here
            G.add_edge(nodesname[n], nodesname[i], weight=random.randint(0,20))
plt.figure(figsize=(20,10))

#elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
total = [(u, v, d) for (u, v, d) in G.edges(data=True)]

pos = nx.spring_layout(G)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(G, pos, node_size=900)

# edges
nx.draw_networkx_edges(G, pos, edgelist=total, width=1)
#nx.draw_networkx_edges(
#    G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed")

# labels
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_labels(G, pos, font_size=25,edge_labels=labels, font_family="sans-serif")
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

plt.axis("off")
plt.show()

#Functions to do tests
def getweight(node1,node2): #input should be 2 strings, returns the integer value: weight between 2 nodes
    node1 = str(node1)
    node2 = str(node2)
    print (node1,node2)
    for (a,b,c) in total:
        if a == node1 or a == node2:
            if b == node1 or b == node2:
                return (c["weight"])
            
def getnearnodes(node): #input should be 2 strings, returns the integer value: weight between 2 nodes
    node = str(node)
    for (a,b,c) in total:
        if a == node:
            print (b)
        elif b == node:
            print (a)


# In[167]:


print (total)


# In[169]:


getnearnodes("s")


# In[ ]:




