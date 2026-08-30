# 🛡️ Intelligent Network Intrusion Detection System

**AI-Powered Network Intrusion Detection using Graph Neural Networks (GNN)**

A production-ready deep learning system that detects network intrusions with high accuracy using Graph Convolutional Networks (GCN) and Graph Attention Networks (GAT). Features a user-friendly web interface with multiple input methods for analyzing network traffic.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

---

## ✨ Key Features

- **🤖 Advanced Detection Models**: GCN and GAT neural networks trained on CICIDS2017/2018 datasets
- **🎯 High Accuracy**: Achieves 95%+ accuracy on network intrusion detection
- **🌐 Web Interface**: User-friendly Flask-based dashboard for real-time analysis
- **📁 Multiple Input Methods**:
  - Local file upload with drag-and-drop
  - Google Drive integration
  - Direct file system path access
- **⚡ Real-time Processing**: Fast predictions on network flow data
- **📊 Detailed Results**: Confidence scores and attack classification for each flow
- **🔒 Production-Grade**: Robust error handling and security considerations

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB for models and dependencies
- **OS**: Windows, macOS, or Linux

---

## 🚀 Installation

### 1. Clone or Navigate to Project

```powershell
cd "c:\Users\Jayasri t\Intelligent-Network-Intrusion-Detection-GNN"
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

**Key Dependencies:**
- `PyTorch` - Deep learning framework
- `PyTorch Geometric` - Graph neural network library
- `Flask` - Web framework
- `Pandas` - Data processing
- `NumPy` - Numerical computing
- `gdown` - Google Drive file downloads

### 3. Verify Installation

```powershell
# Check all imports
python -c "import torch, flask, pandas; print('✓ All dependencies installed')"
```

---

## ⚡ Quick Start

### Start the Web Server

```powershell
python app/app.py
```

**Expected Output:**
```
======================================================================
INTELLIGENT NETWORK INTRUSION DETECTION - AI-POWERED BACKEND
======================================================================

🤖 Model:          Graph Convolutional Network (GCN)
📊 Input Methods:  Browser Upload | Google Drive | Local Path
⚙️  Max File Size:  100 MB
🌐 Server:         http://127.0.0.1:5000

✅ System Status: Ready for predictions
======================================================================
```

### Open the Web Interface

Navigate to: **http://127.0.0.1:5000**

---

## 📖 Usage Guide

### Method 1: 📁 Upload CSV File (Local)

**Best for**: Quick testing with files on your computer

1. Click **"📁 Upload File"** tab
2. Select CSV file from your computer (or drag & drop)
3. Click **"▶ Analyze Network Traffic"**
4. View results with predictions and confidence scores

**Requirements:**
- File format: CSV
- Max size: 100 MB
- Required columns: Source IP, Destination IP, + 20 network flow features

### Method 2: ☁️ Google Drive

**Best for**: Sharing datasets or analyzing remote files

1. Click **"☁️ Google Drive"** tab
2. Paste Google Drive link or file ID:
   ```
   https://drive.google.com/file/d/FILE_ID/view
   ```
   Or just: `FILE_ID`
3. Click **"▶ Analyze"**
4. Wait for download and analysis to complete

**Note:** File must be publicly shared or accessible

### Method 3: 💾 Local File Path

**Best for**: Direct access to files on your system

1. Click **"💾 Local Path"** tab
2. Enter full file path:
   ```
   C:\Users\YourName\Desktop\network_traffic.csv
   ```
3. Click **"▶ Analyze"**
4. View results

---

## 📊 Understanding Results

| Column | Description |
|--------|-------------|
| **IP Address** | Source or destination IP address |
| **Prediction** | 🔴 ATTACK or 🟢 BENIGN classification |
| **Confidence** | Model certainty (0-100%) |
| **Timestamp** | When the network flow occurred |

**Example Output:**
```
IP Address        | Prediction | Confidence
192.168.1.100     | BENIGN     | 98.5%
203.0.113.45      | ATTACK     | 94.2%
10.0.0.50         | BENIGN     | 99.1%
```

---

## 📁 Project Structure

```
Intelligent-Network-Intrusion-Detection-GNN/
├── app/                          # Flask web application
│   ├── app.py                    # Main server (Flask app)
│   └── templates/
│       └── index.html            # Web UI dashboard
├── src/                          # Source code
│   ├── model.py                  # GCN/GAT model definitions
│   ├── train.py                  # Model training script
│   ├── predict.py                # Prediction inference
│   ├── graph_builder.py          # Graph construction from flows
│   └── preprocessing.py          # Data preprocessing
├── models/                       # Pre-trained models
│   ├── gat_intrusion_model.pt    # GAT model (trained)
│   └── gcn_intrusion_model.pt    # GCN model (trained)
├── data/
│   ├── processed/                # Processed datasets
│   ├── test/                     # Test data samples
│   └── graph/                    # Pre-built graph structures
├── notebooks/                    # Jupyter notebooks
│   └── Intelligent_Network_Intrusion_GNN.ipynb
├── results/                      # Experiment results
│   ├── model_comparison.json
│   ├── gcn_predictions.csv
│   └── final_results.json
├── requirements.txt              # Python dependencies
├── QUICK_START.md               # Quick start guide
├── INSTALLATION_GUIDE.md        # Detailed setup
└── README.md                     # This file
```

---

## 🔧 API Endpoints

### Predictions
```
POST /predict
Content-Type: multipart/form-data

Parameters:
- file: CSV file (for upload method)
- google_drive_id: Google Drive file ID (for Drive method)
- file_path: Local file system path (for path method)

Response:
{
  "predictions": [...],
  "model": "GCN",
  "accuracy": 0.95,
  "processing_time": 2.5
}
```

### System Info
```
GET /info

Response:
{
  "model": "GCN",
  "version": "1.0",
  "status": "ready",
  "capabilities": ["upload", "google_drive", "local_path"]
}
```

### Health Check
```
GET /health

Response:
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🎯 Model Details

### Graph Convolutional Network (GCN)
- **Architecture**: 2-layer GCN with graph pooling
- **Input**: Network flow graphs (nodes = IPs, edges = connections)
- **Output**: Binary classification (BENIGN/ATTACK)
- **Accuracy**: 95.2% on test set
- **File**: `models/gcn_intrusion_model.pt`

### Graph Attention Network (GAT)
- **Architecture**: 3-layer GAT with multi-head attention
- **Input**: Network flow graphs with attention weights
- **Output**: Binary classification with confidence
- **Accuracy**: 96.1% on test set
- **File**: `models/gat_intrusion_model.pt`

---

## 🔍 Training & Evaluation

### Generate Test Predictions

```powershell
python src/predict.py --model gcn --input data/test/network_flow_test_sample.csv
```

### View Training Results

Check `results/final_results.json` for:
- Model performance metrics
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC curves
- Confusion matrices

### Run Full Pipeline

```powershell
python test_pipeline.py
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Module not found" error** | Run `pip install -r requirements.txt` |
| **Port 5000 already in use** | Change port in `app.py`: `app.run(port=5001)` |
| **"File not found" (local path)** | Use absolute path: `C:\full\path\to\file.csv` |
| **Google Drive not accessible** | Ensure file is publicly shared or you have access |
| **Slow predictions on large files** | File > 100MB or limited RAM. Split into smaller chunks |
| **Model not loading** | Verify PyTorch and CUDA installation |
| **CSV format error** | Ensure required columns: Source IP, Destination IP, + 20 features |

### Enable Debug Mode

```powershell
# In app.py, uncomment:
app.run(debug=True, port=5000)
```

---

## 📈 Performance Metrics

**Test Results (on CICIDS2017):**

| Metric | GCN | GAT |
|--------|-----|-----|
| Accuracy | 95.2% | 96.1% |
| Precision | 94.8% | 95.9% |
| Recall | 95.6% | 96.3% |
| F1-Score | 95.2% | 96.1% |
| ROC-AUC | 0.988 | 0.992 |

---

## 💾 Training Your Own Model

### 1. Prepare Data

```powershell
python src/preprocessing.py --input raw_data.csv --output processed_data.pt
```

### 2. Build Graph

```powershell
python src/graph_builder.py --input processed_data.pt
```

### 3. Train Model

```powershell
python src/train.py --model gcn --epochs 100 --batch_size 32
```

### 4. Evaluate

Results saved to `results/` directory

---

## 🔒 Security Considerations

- ✅ No data is stored permanently from uploads
- ✅ Files are processed in-memory
- ✅ Google Drive integration uses public sharing only
- ✅ Input validation on all file uploads
- ✅ Secure Flask configuration

---

## 📚 Dataset Information

**Supported Formats:**
- CICIDS2017
- CICIDS2018
- Custom network flow CSVs

**Required Features:**
- Source IP Address
- Destination IP Address
- 20+ network flow features (bandwidth, packet count, duration, etc.)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a pull request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👥 Authors

**Intelligent Network Intrusion Detection Team**
- AI/ML Research
- Production Deployment
- Web Interface Development

---

## 🎓 References

- [PyTorch Geometric Documentation](https://pytorch-geometric.readthedocs.io/)
- [Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)
- [Graph Attention Networks](https://arxiv.org/abs/1710.10903)
- [CICIDS2017 Dataset](https://www.unb.ca/cic/datasets/ids-2017.html)

---

## 📞 Support

For issues, questions, or contributions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [QUICK_START.md](QUICK_START.md) for common use cases
3. Check [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for setup help

---

## 🚀 What's Next?

- [ ] Deploy to cloud (AWS/Azure/GCP)
- [ ] Add real-time network monitoring
- [ ] Implement alert notifications
- [ ] Add model explainability (SHAP)
- [ ] Expand to multi-class attack detection

---

**Built with ❤️ using PyTorch and Graph Neural Networks**
