from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import preprocess_csv
from src.graph_builder import build_graph
from src.predict import predict_graph


# ============================================================
# CSV PATH
# ============================================================

CSV_PATH = PROJECT_ROOT / "data" / "test" / "network_flow_test_sample.csv"


# ============================================================
# PREPROCESS
# ============================================================

df, feature_df = preprocess_csv(
    CSV_PATH
)


# ============================================================
# BUILD GRAPH
# ============================================================

graph, node_mapping = build_graph(
    df,
    feature_df
)


# ============================================================
# PREDICT
# ============================================================

results = predict_graph(
    graph,
    node_mapping
)


# ============================================================
# DISPLAY
# ============================================================

print()
print("=" * 60)
print("GCN PREDICTIONS")
print("=" * 60)

for result in results:

    print(
        f"{result['ip_address']:>20} | "
        f"{result['prediction']:7} | "
        f"{result['confidence']:6.2f}%"
    )