import networkx as nx
import pandas as pd
import dash_cytoscape as cyto
import column as col


def init_graph(df):
    # Fix weights by converting values to float
    # Divide it by 2 to scale them better
        
    Graphtype = nx.DiGraph()
    G = nx.from_pandas_edgelist(
            df,
            col.ID,
            col.OUTCOME,
            #edge_attr=[df[col.CORRELATION], col.WEIGHT],
            create_using=Graphtype)

    return G


# Converting networkx data into cytoscape format
def convert_nx_to_cyto(G):
    pos = nx.get_node_attributes(G, "pos")
    cy = nx.readwrite.json_graph.cytoscape_data(G)

    # Create node labels for cytoscape
    for n in cy["elements"]["nodes"]:
        for k,v in n.items():
            v["label"] = v.pop("value")
    
    # Add the node positions as a value for data in the nodes portion of cy
    for n,p in zip(cy["elements"]["nodes"], pos.values()):
        n["pos"] = {"x":p[0],"y":p[1]}
      
    # Combine the dicts of nodes and edges to generate a list
    elements = cy["elements"]["nodes"] + cy["elements"]["edges"]

    return elements


def visualize_graph(elements):
    cytoscape = cyto.Cytoscape(
            id="knowledge-graph",
            layout={ "name" : "circle" },
            elements=elements,
            style={
                "width": "100%", 
                "height": "720px", 
                "background-color": "#f4f4f4", 
                "margin-top": "1em"
            },
            userZoomingEnabled=False,
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "content": "data(label)",
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "width": "data(weight)",
                        "curve-style": "straight",
                        "target-arrow-shape": "triangle",
                        "source-endpoint": "inside-to-node"
                    }
                },
                {
                    "selector": "[correlation = 0]",
                    "style": {
                        "width": "1",
                    }
                },
                {
                    "selector": "[correlation < 0]",
                    "style": {
                        "target-arrow-color": "#f92411",
                        "line-color": "#f92411"
                    }
                },
                {
                    "selector": "[correlation > 0]",
                    "style": {
                        "target-arrow-color": "#61bbfc",
                        "line-color": "#61bbfc"
                    }
                },    
            ]
        )

    return cytoscape