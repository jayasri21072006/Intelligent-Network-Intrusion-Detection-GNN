# Intelligent Network Intrusion Detection

A Flask application that uses a graph convolutional network (GCN) to classify network IP nodes as `ATTACK` or `BENIGN`. Network-flow CSV data is cleaned, converted into an IP graph, normalized with the training scaler, and passed to the trained model.

## Features

- Browser CSV upload
- Google Drive file ID or supported share URL input
- Local CSV path input
- IP-level predictions with confidence scores
- Summary counts for rows, nodes, edges, attacks, and benign nodes
- Health and capability endpoints

The current web application uses the GCN model. The repository also contains a GAT model artifact, but it is not wired into the Flask prediction path.

## Requirements

- Python 3.11 recommended (`runtime.txt` and `render.yaml` target Python 3.11.9)
- Dependencies from `requirements.txt`
- Runtime artifacts: `models/gcn_intrusion_model.pt` and `models/node_scaler.pkl`

## Setup

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run The Web App

Development server:

```powershell
python app\app.py
```

Open `http://127.0.0.1:5000` in a browser.

For a deployment-style server:

```bash
gunicorn --workers 1 --threads 2 --timeout 120 wsgi:app
```

The Render configuration is in `render.yaml`; the deployment entry point is `wsgi:app`.

## Input CSV Format

The CSV must contain `Source IP`, `Destination IP`, and these 20 numeric model features:

```text
Source Port
Destination Port
Protocol
Flow Duration
Total Fwd Packets
Total Backward Packets
Total Length of Fwd Packets
Total Length of Bwd Packets
Fwd Packet Length Mean
Bwd Packet Length Mean
Flow Bytes/s
Flow Packets/s
Flow IAT Mean
Fwd IAT Mean
Bwd IAT Mean
Packet Length Mean
Packet Length Variance
Average Packet Size
Active Mean
Idle Mean
```

Column-name whitespace is trimmed. Infinite values and rows with missing required values are removed. The request fails if no valid rows remain.

## API

### `GET /health`

Returns service status and whether Google Drive support is available:

```json
{
  "status": "running",
  "model": "GCN",
  "gdrive_support": true
}
```

### `GET /info`

Returns model, file-size, format, and input-method capabilities.

### `POST /predict`

Browser upload:

```bash
curl -X POST -F "file=@data/test/network_flow_test_sample.csv" http://127.0.0.1:5000/predict
```

Google Drive URL or ID:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"gdrive_url\":\"https://drive.google.com/file/d/FILE_ID/view\"}" http://127.0.0.1:5000/predict
```

Local path:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"local_path\":\"C:\\\\data\\\\traffic.csv\"}" http://127.0.0.1:5000/predict
```

Successful responses contain `filename`, `input_type`, `rows_analyzed`, `nodes_analyzed`, `edges_analyzed`, `attack_count`, `benign_count`, and `results`. Each result contains `node_id`, `ip_address`, `prediction`, and `confidence`.

Uploads are limited to 100 MB. Temporary upload and downloaded files are removed after processing.

## Run The Pipeline Check

The smoke test uses the bundled sample and runs the same preprocessing, graph construction, and GCN inference path as the application:

```powershell
python tests\test_pipeline.py
```

The test requires a working PyTorch installation and the model/scaler artifacts.

## Repository Layout

```text
app/                  Flask application and web template
src/                  preprocessing, graph building, model, and inference code
tests/                pipeline smoke test
models/               trained model and feature scaler artifacts
data/raw/             raw input data
data/test/            bundled test CSV
data/graph/           graph artifact
notebooks/            exploratory/training notebook
results/              saved experiment outputs
docs/                 setup and project notes
wsgi.py               WSGI entry point
Procfile              process command for hosting platforms
render.yaml           Render deployment configuration
requirements.txt      Python dependencies
```

## Documentation

- [Quick start](docs/QUICK_START.md)
- [Installation guide](docs/INSTALLATION_GUIDE.md)
- [Project notes](docs/CHANGES_SUMMARY.md)

## Limitations

- The web endpoint performs inference with the GCN only.
- `src/train.py` is currently empty; training is not exposed as a command-line workflow.
- The repository does not include automated accuracy evaluation; metrics should not be assumed from older notes.
- Local-path input is intended for trusted deployments because the server reads the path supplied by the client.
