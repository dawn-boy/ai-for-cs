import networkx as nx
import torch
from torch_geometric.data import Data

def build_networkx_graph(dep_dict):
    G = nx.DiGraph()
    for pkg, deps in dep_dict.items():
        G.add_node(pkg)
        for dep in deps:
            G.add_edge(pkg, dep)
    return G

def extract_features(G, vulns_dict):
    """
    Features:
    0: Depth (shortest path from root)
    1: In-degree
    2: Out-degree
    3: Is leaf (1 if out-degree == 0 else 0)
    4: Vulnerability prior (1 if has known vulns else 0)
    """
    # Assuming the first node added is the root
    root = list(G.nodes())[0] if G.nodes() else None
    
    if root:
        lengths = nx.single_source_shortest_path_length(G, root)
    else:
        lengths = {}
        
    features = []
    node_mapping = {}
    
    for i, node in enumerate(G.nodes()):
        node_mapping[node] = i
        depth = lengths.get(node, 0)
        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)
        is_leaf = 1.0 if out_deg == 0 else 0.0
        has_vuln = 1.0 if len(vulns_dict.get(node, [])) > 0 else 0.0
        
        features.append([depth, in_deg, out_deg, is_leaf, has_vuln])
        
    x = torch.tensor(features, dtype=torch.float)
    
    edges = []
    for u, v in G.edges():
        edges.append([node_mapping[u], node_mapping[v]])
        
    if edges:
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    else:
        edge_index = torch.empty((2, 0), dtype=torch.long)
        
    data = Data(x=x, edge_index=edge_index)
    return data, node_mapping
