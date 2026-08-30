from pathlib import Path

import joblib
import torch
import torch.nn.functional as F

from src.model import GCN


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "gcn_intrusion_model.pt"
SCALER_PATH = BASE_DIR / "models" / "node_scaler.pkl"


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# LOAD SCALER
# ============================================================

scaler = joblib.load(SCALER_PATH)


# ============================================================
# LOAD GCN MODEL
# ============================================================

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE,
    weights_only=False
)


# ------------------------------------------------------------
# Handle checkpoint format
# ------------------------------------------------------------

if isinstance(checkpoint, dict):

    if "model_state_dict" in checkpoint:

        state_dict = checkpoint["model_state_dict"]

    elif "state_dict" in checkpoint:

        state_dict = checkpoint["state_dict"]

    else:

        # Sometimes the checkpoint itself is a state dict
        state_dict = checkpoint

else:

    raise ValueError(
        "Unsupported model checkpoint format."
    )


# ============================================================
# CREATE MODEL
# ============================================================

model = GCN(
    input_features=20,
    hidden_features=64,
    num_classes=2
).to(DEVICE)


# ============================================================
# LOAD WEIGHTS
# ============================================================

model.load_state_dict(
    state_dict
)

model.eval()


# ============================================================
# PREDICT GRAPH
# ============================================================

def predict_graph(graph, node_mapping):

    # --------------------------------------------------------
    # Scale using the SAME scaler used during training
    # --------------------------------------------------------

    scaled_features = scaler.transform(
        graph.x.numpy()
    )

    graph.x = torch.tensor(
        scaled_features,
        dtype=torch.float32
    )

    graph = graph.to(DEVICE)

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    with torch.no_grad():

        output = model(
            graph.x,
            graph.edge_index
        )

        probabilities = F.softmax(
            output,
            dim=1
        )

        predictions = output.argmax(
            dim=1
        )

    # --------------------------------------------------------
    # Convert predictions to readable results
    # --------------------------------------------------------

    reverse_mapping = {
        node_id: ip
        for ip, node_id in node_mapping.items()
    }

    results = []

    for node_id in range(graph.num_nodes):

        predicted_class = predictions[
            node_id
        ].item()

        confidence = (
            probabilities[
                node_id,
                predicted_class
            ].item() * 100
        )

        label = (
            "ATTACK"
            if predicted_class == 1
            else "BENIGN"
        )

        results.append({
            "node_id": node_id,
            "ip_address": reverse_mapping[node_id],
            "prediction": label,
            "confidence": round(
                confidence,
                2
            )
        })

    return results