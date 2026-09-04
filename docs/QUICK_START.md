# Quick Start

## Install

Run these commands from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Start The Server

```powershell
python app\app.py
```

Then open `http://127.0.0.1:5000`.

## Try The Bundled Sample

Use `data/test/network_flow_test_sample.csv` in the upload tab, or run the pipeline check:

```powershell
python tests\test_pipeline.py
```

## Input Methods

- **Upload:** choose a CSV file in the web interface.
- **Google Drive:** provide a public Drive share URL or file ID. This requires `gdown`.
- **Local path:** provide an absolute path to a CSV file visible to the server.

Every CSV needs `Source IP`, `Destination IP`, and the 20 numeric features listed in the [README](../README.md#input-csv-format).

## API Smoke Checks

```powershell
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/info
curl -X POST -F "file=@data/test/network_flow_test_sample.csv" http://127.0.0.1:5000/predict
```

## Common Problems

- **ImportError:** activate the virtual environment and install `requirements.txt`.
- **Model or scaler not found:** verify `models/gcn_intrusion_model.pt` and `models/node_scaler.pkl` exist.
- **Invalid CSV:** check the required columns and numeric values.
- **Port 5000 in use:** change the development server port in `app/app.py`.
- **PyTorch DLL error on Windows:** reinstall a compatible CPU PyTorch build in a clean virtual environment.
