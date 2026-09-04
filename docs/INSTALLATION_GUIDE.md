# Installation Guide

## Supported Environment

Python 3.11.9 is the deployment target. Python 3.11 is recommended locally. Windows, macOS, and Linux are supported by the project layout, subject to PyTorch and PyTorch Geometric support for the selected platform.

## Create An Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The requirements file uses the PyTorch CPU package index. A CUDA-specific installation may require replacing the PyTorch packages with versions appropriate for the target machine.

## Verify The Installation

```bash
python -c "import flask, joblib, numpy, pandas, sklearn, torch, torch_geometric; print('dependencies ok')"
```

From the repository root, verify the model artifacts:

```powershell
Test-Path models\gcn_intrusion_model.pt
Test-Path models\node_scaler.pkl
```

Both commands should return `True`.

## Run Locally

```powershell
python app\app.py
```

The development server binds to `127.0.0.1:5000` and enables Flask debug mode. For hosting, use:

```bash
gunicorn --workers 1 --threads 2 --timeout 120 wsgi:app
```

## Deploy With Render

The repository includes `render.yaml`. It installs `requirements.txt` and starts Gunicorn with `wsgi:app`. The root-level `wsgi.py`, `Procfile`, and `render.yaml` should remain at the repository root for deployment discovery.

## Data And Models

- Put original datasets in `data/raw/`.
- Use `data/test/network_flow_test_sample.csv` for the bundled smoke test.
- Keep trained artifacts in `models/`.
- Results and exported experiment files belong in `results/`.

The web application loads the GCN checkpoint and scaler when `src.predict` is imported. If either artifact is missing or incompatible, the application will fail during startup.

## Validation

```powershell
python -m compileall -q app src tests wsgi.py
python tests\test_pipeline.py
```

The second command performs actual model inference and requires a functioning PyTorch installation.
