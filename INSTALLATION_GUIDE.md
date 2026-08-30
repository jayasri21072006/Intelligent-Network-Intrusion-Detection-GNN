# 🚀 Network Intrusion Detection - Complete Setup Guide

## Overview
Your GCN-based intrusion detection system now supports **3 input methods** for analyzing network traffic:

### ✅ Input Methods Supported:
1. **📁 Local File Upload** - Select CSV from your computer's file browser
2. **☁️ Google Drive** - Paste Google Drive share link or file ID
3. **💾 Local Path** - Enter direct file system path (e.g., `C:\Users\YourName\Desktop\data.csv`)

---

## 📋 Installation & Setup

### Step 1: Install Python Dependencies

```powershell
# Navigate to project directory
cd "c:\Users\Jayasri t\Intelligent-Network-Intrusion-Detection-GNN"

# Install all required packages
pip install -r requirements.txt
```

**Key dependencies added:**
- `Flask==3.1.2` - Web server framework
- `gdown==5.2.0` - Google Drive file download (optional, but required for Google Drive support)

### Step 2: Verify Installation

```powershell
# Check Flask installation
python -c "import flask; print(f'Flask {flask.__version__} installed')"

# Check gdown installation
python -c "import gdown; print(f'gdown {gdown.__version__} installed')"
```

### Step 3: Start the Flask Server

```powershell
cd "c:\Users\Jayasri t\Intelligent-Network-Intrusion-Detection-GNN"
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

📝 Supported Input Formats:
   • Browser: Upload CSV file
   • Google Drive: Paste share link or file ID
   • Local Path: Direct file system path (e.g., C:\data\traffic.csv)

✅ Google Drive support: ENABLED (gdown installed)

======================================================================
```

### Step 4: Open the UI

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🎯 Using Each Input Method

### Method 1: Local File Upload ✅

**Best for:** Quick testing with files on your computer

1. Click the **"📁 Upload File"** tab
2. Click **"📁 Select CSV File"** button
3. Browse and select your CSV file (or drag & drop)
4. File information will display (name + size)
5. Click **"▶ Analyze Network Traffic"** button
6. Results appear within seconds

**Supports:**
- Max file size: 100 MB
- Format: CSV only
- Network flow data with 20 features + Source/Destination IPs

---

### Method 2: Google Drive ☁️

**Best for:** Sharing datasets or analyzing files stored in Google Drive

#### Get Your Google Drive File Link:

1. Go to [Google Drive](https://drive.google.com)
2. Right-click your CSV file → **"Share"**
3. Click **"Copy link"** (or change to public access)
4. Your link looks like:
   ```
   https://drive.google.com/file/d/1abc123xyz456/view?usp=share_link
   ```

#### In the Application:

1. Click the **"☁️ Google Drive"** tab
2. Paste the link in the text field
3. The file ID will be extracted automatically
4. Click **"▶ Analyze Network Traffic"**
5. System will download and process the file

**Options:**
- **Share Link:** `https://drive.google.com/file/d/1abc123.../view`
- **File ID Only:** `1abc123xyz456` (extracted from the link)
- **Open Link:** `https://drive.google.com/file/d/1abc123.../`

**Note:** File must be publicly shared or you must grant access

---

### Method 3: Local File Path 💾

**Best for:** Automated workflows or files on your computer/network

#### How to Use:

1. Click the **"💾 Local Path"** tab
2. Enter the full file path:
   - Windows: `C:\Users\YourName\Desktop\network_traffic.csv`
   - Network: `\\server\share\data\traffic.csv`
   - UNC Path: `C:\Absolute\Path\To\File.csv`
3. Click **"▶ Analyze Network Traffic"**
4. File will be read directly from disk

**Examples:**
```
C:\Users\John\Downloads\CICIDS2017.csv
D:\NetworkData\attack_samples.csv
\\192.168.1.100\shared_folder\traffic.csv
C:\Temp\network_flow_test_sample.csv
```

---

## 🔄 Backend Processing Pipeline

### All Input Methods Follow This Flow:

```
Your Input
    ↓
[Upload / Google Drive Download / Local Path Read]
    ↓
CSV Loaded into Memory
    ↓
Preprocessing
├── Extract 20 network features
├── Source/Destination IP mapping
└── Graph node preparation
    ↓
Graph Building
├── Create IP nodes
├── Build relationships (edges)
└── Aggregate features
    ↓
GCN Model Inference
├── Forward pass through 2 layers
├── Classification: ATTACK / BENIGN
└── Confidence scores
    ↓
Results Display
├── Summary statistics
├── Per-IP predictions
└── Interactive table
```

---

## 📊 Results Interpretation

After analysis, you'll see:

1. **Summary Cards:**
   - 📈 **Rows Analyzed** - Total network flows processed
   - ⚠️ **Attack Nodes** - IPs classified as malicious
   - ✓ **Benign Nodes** - IPs classified as safe

2. **Results Table:**
   - **IP Address** - Source or destination IP from your data
   - **Prediction** - ATTACK (red) or BENIGN (green)
   - **Confidence** - Model confidence percentage (0-100%)

---

## ⚙️ Backend API Endpoints

### POST /predict
Unified prediction endpoint supporting all input methods

**Request Examples:**

```bash
# Method 1: Browser Upload (multipart/form-data)
curl -X POST -F "file=@traffic.csv" http://127.0.0.1:5000/predict

# Method 2: Google Drive
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"gdrive_url":"https://drive.google.com/file/d/1abc123/view"}' \
  http://127.0.0.1:5000/predict

# Method 3: Local Path
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"local_path":"C:\\\\data\\\\traffic.csv"}' \
  http://127.0.0.1:5000/predict
```

**Response:**
```json
{
  "success": true,
  "filename": "traffic.csv",
  "input_type": "upload",
  "rows_analyzed": 1000,
  "nodes_analyzed": 45,
  "edges_analyzed": 234,
  "attack_count": 12,
  "benign_count": 33,
  "results": [
    {
      "ip_address": "192.168.1.1",
      "prediction": "BENIGN",
      "confidence": 0.98
    },
    {
      "ip_address": "10.0.0.5",
      "prediction": "ATTACK",
      "confidence": 0.95
    }
  ]
}
```

### GET /info
Get backend capabilities and supported features

```bash
curl http://127.0.0.1:5000/info
```

### GET /health
Health check endpoint

```bash
curl http://127.0.0.1:5000/health
```

---

## 🐛 Troubleshooting

### Problem: "gdown module not installed"
```powershell
pip install gdown==5.2.0
```

### Problem: "File not found" with local path
- Verify the path is correct (copy from Windows Explorer)
- Ensure the file has `.csv` extension
- Use absolute paths (not relative)
- For network paths, ensure access is granted

### Problem: "Google Drive file not accessible"
- Ensure the file is publicly shared
- Generate a new share link
- Try the file ID directly instead of the full URL
- Check that the file hasn't been deleted

### Problem: "File exceeds size limit"
- Max file size: 100 MB
- Reduce file size or split into smaller datasets
- Remove unnecessary columns or rows

### Problem: "Only CSV files are supported"
- Ensure file has `.csv` extension
- Export from Excel as CSV (comma-separated values)
- Don't use `.xlsx` or `.json` formats

---

## 🎨 UI Features

✨ **FAANG-Level Design:**
- Modern glassmorphism effects
- Smooth gradient animations
- Advanced micro-interactions
- Responsive design (mobile to desktop)
- Real-time validation feedback
- Smooth number animations in results
- Professional error handling
- Dark mode optimized

⌨️ **Keyboard Shortcuts:**
- **Enter Key**: Analyze (when input is ready)

🖱️ **Mouse Interactions:**
- Drag & drop file upload
- Hover effects on all interactive elements
- Real-time input validation

---

## 📁 Project Structure

```
Intelligent-Network-Intrusion-Detection-GNN/
├── app/
│   ├── app.py                    ← Flask backend (ENHANCED)
│   └── templates/
│       └── index.html            ← Web UI (ENHANCED)
├── src/
│   ├── preprocessing.py
│   ├── graph_builder.py
│   ├── model.py
│   ├── train.py
│   └── predict.py
├── models/
│   ├── gat_intrusion_model.pt
│   └── gcn_intrusion_model.pt
├── data/
│   ├── graph/
│   ├── processed/
│   └── test/
├── requirements.txt              ← UPDATED (Flask + gdown added)
└── INSTALLATION_GUIDE.md        ← This file
```

---

## 🚀 Next Steps

1. **Start the server:**
   ```powershell
   python app/app.py
   ```

2. **Open the UI:**
   ```
   http://127.0.0.1:5000
   ```

3. **Choose your input method:**
   - Upload a CSV file
   - Paste a Google Drive link
   - Enter a local file path

4. **Click "Analyze Network Traffic"**

5. **View real-time results!**

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all Python packages are installed
3. Ensure Flask server is running
4. Check browser console for error messages (F12)
5. Verify network connectivity for Google Drive downloads

---

**Version:** 2.0 (Multi-Input Support)  
**Last Updated:** August 30, 2026  
**Status:** ✅ Production Ready
