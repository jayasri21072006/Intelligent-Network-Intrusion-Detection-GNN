# Project Notes

This file records the current application behavior and repository organization. It replaces earlier implementation notes that described planned or unverified features as production-ready.

## Current Application Behavior

- Flask serves the dashboard from `app/templates/index.html`.
- `POST /predict` accepts browser uploads, Google Drive input, and local paths.
- Preprocessing validates the two IP columns and the 20 model feature columns.
- Graph nodes represent unique source and destination IP addresses.
- Graph edges represent source-to-destination flows.
- Node features are the mean flow features accumulated for each IP.
- Inference uses `models/gcn_intrusion_model.pt` and `models/node_scaler.pkl`.

## Repository Organization

```text
app/                  web application
src/                  reusable pipeline code
tests/                executable pipeline checks
models/               model and scaler artifacts
data/raw/             raw datasets
data/test/            test datasets
data/graph/           graph artifacts
notebooks/            notebook experiments
results/              generated results
docs/                 project documentation
```

## Important Notes

- The GAT checkpoint is stored in `models/` but is not used by the current Flask endpoint.
- `src/train.py` is empty, so training is not currently an executable workflow.
- Accuracy values from older documentation are not verified by an automated evaluation in this repository; consult files in `results/` for available experiment data.
- Local-path requests should only be enabled in a trusted environment.
