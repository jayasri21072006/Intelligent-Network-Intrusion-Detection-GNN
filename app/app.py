from flask import Flask, render_template, request, jsonify
from pathlib import Path
import sys
import tempfile
import os
import io
import re

try:
    import gdown
except ImportError:
    gdown = None

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from src.preprocessing import preprocess_csv
from src.graph_builder import build_graph
from src.predict import predict_graph


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def extract_google_drive_id(url_or_id):
    """
    Extract Google Drive file ID from various URL formats.
    
    Supports:
    - Direct ID: 1abc123...xyz
    - Long share link: https://drive.google.com/file/d/1abc123.../view?...
    - Short link: https://drive.google.com/file/d/1abc123.../
    """
    if not isinstance(url_or_id, str):
        return None
    
    # If it looks like a Drive ID (32-44 chars, alphanumeric + dashes/underscores)
    if re.match(r'^[a-zA-Z0-9_-]{25,100}$', url_or_id.strip()):
        return url_or_id.strip()
    
    # Extract from URL
    patterns = [
        r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
        r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    return None


def download_from_google_drive(drive_id):
    """
    Download file from Google Drive using gdown.
    Returns file bytes or raises error.
    """
    if not gdown:
        raise ImportError("gdown is not installed. Install with: pip install gdown")
    
    try:
        url = f"https://drive.google.com/uc?id={drive_id}"
        
        # Download to BytesIO instead of temp file
        output = io.BytesIO()
        gdown.download(url, output=None, quiet=True, fuzzy=True)
        
        # Alternative: download to temp and read
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            gdown.download(url, output=tmp.name, quiet=True, fuzzy=True)
            tmp.flush()
            return tmp.name
            
    except Exception as e:
        raise Exception(f"Failed to download from Google Drive: {str(e)}")


def load_csv_from_path(file_path):
    """
    Load CSV file from local system path.
    Validates that file exists and is a CSV.
    """
    path = Path(file_path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.suffix.lower() == ".csv":
        raise ValueError(f"File must be CSV, got: {path.suffix}")
    
    return str(path)


def get_csv_file(input_source):
    """
    Determine input type and return path to CSV file.
    
    Input types:
    1. Browser upload: request.files object
    2. Google Drive: URL or file ID string
    3. Local path: file system path string
    
    Returns: (file_path, filename, input_type)
    """
    
    # Type 1: Browser file upload
    if hasattr(input_source, 'filename'):
        if input_source.filename == "":
            raise ValueError("No file selected.")
        if not input_source.filename.lower().endswith(".csv"):
            raise ValueError("Only CSV files are supported.")
        
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        ) as temp_file:
            input_source.save(temp_file.name)
            return temp_file.name, input_source.filename, "upload"
    
    # Type 2: String input (Drive ID/URL or local path)
    if isinstance(input_source, str):
        input_source = input_source.strip()
        
        # Check if it's a Google Drive link
        drive_id = extract_google_drive_id(input_source)
        if drive_id:
            temp_path = download_from_google_drive(drive_id)
            filename = f"gdrive_{drive_id[:8]}.csv"
            return temp_path, filename, "gdrive"
        
        # Assume it's a local file path
        try:
            file_path = load_csv_from_path(input_source)
            filename = Path(input_source).name
            return file_path, filename, "local"
        except (FileNotFoundError, ValueError) as e:
            raise ValueError(
                f"Invalid input: {str(e)}. "
                f"Provide a valid local path or Google Drive link."
            )
    
    raise ValueError("Invalid input format")


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# CSV PREDICTION - UNIFIED ENDPOINT
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():
    """
    Unified prediction endpoint supporting:
    - Browser file upload: multipart/form-data with 'file'
    - Google Drive: JSON with 'gdrive_url' or 'gdrive_id'
    - Local path: JSON with 'local_path'
    """
    
    temp_paths = []
    
    try:
        # Determine input source
        input_source = None
        filename = None
        input_type = None
        
        # Try browser file upload first
        if "file" in request.files:
            input_source = request.files["file"]
            input_type = "upload"
        
        # Try JSON input (Google Drive or local path)
        elif request.is_json:
            data = request.get_json()
            
            if "gdrive_url" in data or "gdrive_id" in data:
                input_source = data.get("gdrive_url") or data.get("gdrive_id")
                input_type = "gdrive"
            elif "local_path" in data:
                input_source = data.get("local_path")
                input_type = "local"
        
        if not input_source:
            return jsonify({
                "error": "Please provide input: file upload, Google Drive link, or local file path."
            }), 400
        
        # Get CSV file (handles all input types)
        csv_path, filename, input_type = get_csv_file(input_source)
        temp_paths.append(csv_path)
        
        # ====================================================
        # PREPROCESS
        # ====================================================
        
        df, feature_df = preprocess_csv(csv_path)
        
        # ====================================================
        # BUILD GRAPH
        # ====================================================
        
        graph, node_mapping = build_graph(df, feature_df)
        
        # ====================================================
        # PREDICT
        # ====================================================
        
        results = predict_graph(graph, node_mapping)
        
        # ====================================================
        # SUMMARY
        # ====================================================
        
        attack_count = sum(
            1 for result in results
            if result["prediction"] == "ATTACK"
        )
        
        benign_count = sum(
            1 for result in results
            if result["prediction"] == "BENIGN"
        )
        
        return jsonify({
            "success": True,
            "filename": filename,
            "input_type": input_type,
            "rows_analyzed": len(df),
            "nodes_analyzed": graph.num_nodes,
            "edges_analyzed": graph.num_edges,
            "attack_count": attack_count,
            "benign_count": benign_count,
            "results": results
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except FileNotFoundError as e:
        return jsonify({"error": f"File not found: {str(e)}"}), 404
    except ImportError as e:
        return jsonify({"error": f"Missing dependency: {str(e)}. Install with: pip install gdown"}), 500
    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500
    
    finally:
        # Clean up temporary files
        for temp_path in temp_paths:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass


# ============================================================
# INFO ENDPOINT
# ============================================================

@app.route("/info", methods=["GET"])
def info():
    """
    Get backend capabilities and supported input methods.
    """
    gdrive_available = gdown is not None
    
    return jsonify({
        "backend": "Flask + GCN",
        "model": "Graph Convolutional Network",
        "max_file_size_mb": 100,
        "supported_formats": ["CSV"],
        "input_methods": {
            "browser_upload": True,
            "local_path": True,
            "google_drive": gdrive_available
        },
        "gdrive_note": "gdown module must be installed" if not gdrive_available else "Ready"
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():
    return jsonify({
        "status": "running",
        "model": "GCN",
        "gdrive_support": gdown is not None
    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("INTELLIGENT NETWORK INTRUSION DETECTION - AI-POWERED BACKEND")
    print("=" * 70)
    print()
    print("🤖 Model:          Graph Convolutional Network (GCN)")
    print("📊 Input Methods:  Browser Upload | Remote URL | Local Path")
    print("⚙️  Max File Size:  100 MB")
    print("🌐 Server:         http://127.0.0.1:5000")
    print()
    print("📝 Supported Input Formats:")
    print("   • Browser: Upload CSV file from your device")
    print("   • Remote: Paste a Google Drive or shared file URL")
    print("   • Local Path: Direct file system path (e.g., C:\\data\\traffic.csv)")
    print()
    
    if gdown:
        print("✅ Remote URL support: ENABLED (gdown installed)")
    else:
        print("⚠️  Remote URL support: DISABLED")
        print("   Install with: pip install gdown")
    print()
    print("=" * 70)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )