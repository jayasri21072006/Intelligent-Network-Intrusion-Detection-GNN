import numpy as np
import pandas as pd
import torch
from torch_geometric.data import Data

from src.preprocessing import FEATURE_COLUMNS


def build_graph(df, feature_df):
    """
    Convert network-flow data into a graph using high-performance vectorized operations.

    Nodes:
        Unique Source/Destination IP addresses

    Edges:
        Source IP -> Destination IP

    Node features:
        Mean of the network-flow features associated with each IP.
    """

    # ========================================================
    # 1. CREATE IP → NODE ID MAPPING (Vectorized)
    # ========================================================

    all_ips_series = pd.concat([df["Source IP"], df["Destination IP"]])
    unique_ips = all_ips_series.drop_duplicates().values

    node_mapping = {ip: idx for idx, ip in enumerate(unique_ips)}
    num_nodes = len(unique_ips)

    # ========================================================
    # 2. VECTORIZED EDGE MAPPING
    # ========================================================

    cat_type = pd.CategoricalDtype(categories=unique_ips)
    src_ids = pd.Categorical(df["Source IP"], dtype=cat_type).codes
    dst_ids = pd.Categorical(df["Destination IP"], dtype=cat_type).codes

    edges = np.vstack((src_ids, dst_ids))

    # ========================================================
    # 3. VECTORIZED NODE FEATURE AGGREGATION
    # ========================================================

    feature_values = feature_df.to_numpy(dtype=np.float64)

    node_sum = np.zeros(
        (num_nodes, feature_values.shape[1]),
        dtype=np.float64
    )
    node_count = np.zeros(
        num_nodes,
        dtype=np.float64
    )

    # Aggregate flow features for both source and destination nodes
    np.add.at(node_sum, src_ids, feature_values)
    np.add.at(node_count, src_ids, 1.0)

    np.add.at(node_sum, dst_ids, feature_values)
    np.add.at(node_count, dst_ids, 1.0)

    # Compute mean node features
    node_features = np.divide(
        node_sum,
        node_count[:, None],
        out=np.zeros_like(node_sum),
        where=node_count[:, None] != 0
    )

    # ========================================================
    # 4. CONVERT TO PYTORCH GEOMETRIC GRAPH
    # ========================================================

    x = torch.tensor(
        node_features,
        dtype=torch.float32
    )

    edge_index = torch.tensor(
        edges,
        dtype=torch.long
    ).contiguous()

    # ========================================================
    # 5. CREATE PYTORCH GEOMETRIC GRAPH
    # ========================================================

    graph = Data(
        x=x,
        edge_index=edge_index
    )

    print("=" * 60)
    print("GRAPH CREATED (Vectorized Pipeline)")
    print("=" * 60)

    print("Nodes   :", graph.num_nodes)
    print("Edges   :", graph.num_edges)
    print("Features:", graph.x.shape)

    return graph, node_mapping