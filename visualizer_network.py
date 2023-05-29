import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import numpy as np


# Read the CSV file
df = pd.read_csv("/Users/mehdigreefhorst/Desktop/StakeholdersTool/similarity_data_AI_to_check.csv")
# Create a directed graph

G = nx.MultiDiGraph()


def draw_diagram():

    # Iterate through the DataFrame rows and add nodes and edges to the graph
    for index, row in df.iterrows():
        url_link = row['url_link']
        parent_url = row['parent_url']
        similarity_score = row['similarity_score']
        outgoing_link_on_webpage_with_similarity = eval(row["outgoing_link_on_webpage_with_similarity"])
        """print(outgoing_link_on_webpage_with_similarity[0])
        print(url_link)
        print(parent_url)
        print(similarity_score)"""


        # Add nodes with similarity_score as an attribute
        #G.add_node(url_link, similarity_score=similarity_score)

        # Add edges
        G.add_edge(parent_url, url_link)

        #links_on_webpage_with_parent = [(parent_url, out_going_link[1]) for out_going_link in outgoing_link_on_webpage_with_similarity]
        #print(links_on_webpage_with_parent)
        #G.add_edges_from(links_on_webpage_with_parent, weight = 0.1)

    # Draw the graph
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    #labels = nx.get_node_attributes(G, 'similarity_score')
    #nx.draw_networkx_labels(G, pos, labels=labels)
    nx.draw_networkx(G, pos, with_labels=False, node_color='skyblue')
    plt.show()


draw_diagram()