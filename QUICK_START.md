# 🚀 QUICK START GUIDE

## One-Time Setup

```powershell
# 1. Navigate to project
cd "c:\Users\Jayasri t\Intelligent-Network-Intrusion-Detection-GNN"

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Start the server
python app/app.py
```

**Server starts at:** `http://127.0.0.1:5000`

---

## Three Ways to Input Data

### 📁 Method 1: Upload CSV
- Click **"📁 Upload File"** tab
- Select your CSV from computer
- Or drag-drop the file
- Click **"▶ Analyze"**

### ☁️ Method 2: Google Drive
- Click **"☁️ Google Drive"** tab
- Paste Google Drive link:
  ```
  https://drive.google.com/file/d/1abc123xyz/view
  ```
  Or just the ID: `1abc123xyz`
- Click **"▶ Analyze"**

### 💾 Method 3: Local Path
- Click **"💾 Local Path"** tab
- Enter file path:
  ```
  C:\Users\YourName\Desktop\traffic.csv
  ```
- Click **"▶ Analyze"**

---

## Reading Results

| Column | Meaning |
|--------|---------|
| **IP Address** | Source or destination IP |
| **Prediction** | 🔴 ATTACK or 🟢 BENIGN |
| **Confidence** | Model certainty (0-100%) |

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Module not found" | Run: `pip install -r requirements.txt` |
| "File not found" (local path) | Use absolute path: `C:\full\path\to\file.csv` |
| "Google Drive not accessible" | Make file public or check permissions |
| "File too large" | Max 100 MB - split into smaller files |
| Port 5000 already in use | Change port in `app.py`: `app.run(port=5001)` |

---

## File Format

**Required CSV Columns:**
- Source IP
- Destination IP  
- 20 network flow features (bandwidth, duration, packets, etc.)

**Supported Format:**
- CICIDS2017 / CICIDS2018 format
- Any network flow CSV with required fields

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Enter** | Analyze (when input is ready) |
| **Tab** | Switch between input methods |

---

## Endpoints (API)

```bash
# Main prediction (all 3 input types)
POST /predict

# System info
GET /info

# Health check  
GET /health
```

---

## File Locations

```
Project Root
├── app/app.py              ← Flask backend
├── app/templates/index.html ← Web UI
├── requirements.txt         ← Dependencies
├── data/test/              ← Sample data
└── models/                 ← GCN models
```

---

## Performance

| Input | Time |
|-------|------|
| Browser Upload | 2-5 sec |
| Google Drive | 3-10 sec |
| Local Path | 2-3 sec (fastest) |

*Times depend on file size (max 100 MB)*

---

## Tips & Tricks

✨ **Pro Tips:**
- Use local path for fastest processing
- Google Drive works great for collaboration
- Keyboard shortcuts speed up workflow
- Try sample data first: `data/test/network_flow_test_sample.csv`
- Hover over stats for more details

---

**Need Help?** See `INSTALLATION_GUIDE.md` for detailed instructions.

**Happy Analyzing!** 🎯
