#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import networkx as nx
import matplotlib.pyplot as plt

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def draw_network(network, node_positions, node_size=3200, node_class_colours=None, node_text_size=10,
                 edge_class_colours=None, edge_width=10, filename=None, figsize=(10,10)):
    """
    Draw a network
    :param network: The network to draw
    :param node_positions: Dictionary of positions of nodes- key:Patch, value:tuple (x,y) coordinates
    :param node_size: Size of node
    :param node_class_colours: Colours for nodes based on class- key:Subclass of patch, value=Colour
    :param node_text_size: Size of text in nodes (0 to omit)
    :param edge_class_colours: Colours for edges based on class- key:Subclass of edge, value=Colour
    :param edge_width: Size of edges
    :param filename: Filename if save is required
    :param figsize: Size of figure
    :return:
    """

    fig = plt.figure(figsize=figsize)
    # Create a networkx graph
    g = nx.Graph()

    # Add nodes and egdes
    for node in network.nodes:
        g.add_node(node)
    for e in network.edges:
        g.add_edge(e.nodes[0], e.nodes[1])

    # Get positions
    pos = {}
    for node_id in node_positions:
        node = network.get_node_by_id(node_id)
        pos[node] = node_positions[node_id]

    # If node colours specified, go through each class and pull nodes from that class, draw with associated colour
    if node_class_colours:
        for cl in node_class_colours:
            nodes = [n for n in network.nodes if isinstance(n, cl)]
            nx.draw_networkx_nodes(g, pos, nodelist=nodes, node_size=node_size, node_color=node_class_colours[cl])
    else:
        # Draw all nodes - default colour green
        nx.draw_networkx_nodes(g, pos, node_size=node_size, node_color='green')

    # If ede colours specified, go through each class and pull edges from that class, draw with associated colour
    if edge_class_colours:
        for cl in edge_class_colours:
            edges = [(e.nodes[0], e.nodes[1]) for e in network.edges if isinstance(e, cl)]
            nx.draw_networkx_edges(g, pos, edgelist=edges, width=edge_width, edge_color=edge_class_colours[cl])
    else:
        nx.draw_networkx_edges(g, pos, width=edge_width, edge_color='green')
    # Node labels
    if node_text_size:
        nx.draw_networkx_labels(g, pos, font_size=node_text_size)
    #  Turn axis off
    plt.axis('off')
    # Display
    plt.show()
    # Save if required
    if filename:
        fig.savefig(filename + ".png")
