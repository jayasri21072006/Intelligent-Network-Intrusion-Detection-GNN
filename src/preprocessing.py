from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# EXACT 20 FEATURES USED BY THE TRAINED GCN
# ============================================================

FEATURE_COLUMNS = [
    "Source Port",
    "Destination Port",
    "Protocol",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Mean",
    "Bwd Packet Length Mean",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Flow IAT Mean",
    "Fwd IAT Mean",
    "Bwd IAT Mean",
    "Packet Length Mean",
    "Packet Length Variance",
    "Average Packet Size",
    "Active Mean",
    "Idle Mean",
]


# ============================================================
# REQUIRED NETWORK COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "Source IP",
    "Destination IP",
]


# ============================================================
# LOAD CSV
# ============================================================

def load_csv(csv_path):
    """
    Load a network traffic CSV file.
    """

    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}"
        )

    df = pd.read_csv(csv_path)

    print("=" * 60)
    print("CSV LOADED")
    print("=" * 60)

    print("File:", csv_path.name)
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    return df


# ============================================================
# VALIDATE CSV
# ============================================================

def validate_columns(df):
    """
    Check whether the uploaded CSV contains
    all columns required by the GCN pipeline.
    """

    required_columns = (
        REQUIRED_COLUMNS +
        FEATURE_COLUMNS
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "The uploaded CSV is missing required columns:\n\n"
            + "\n".join(
                f"- {column}"
                for column in missing_columns
            )
        )

    return True


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

def clean_column_names(df):
    """
    Remove accidental spaces from CSV column names.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


# ============================================================
# CLEAN NUMERICAL DATA
# ============================================================

def clean_data(df):
    """
    Clean network-flow feature values.
    """

    df = df.copy()

    # Replace infinity values
    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Convert the 20 model features to numeric
    for column in FEATURE_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove rows where required values are missing
    df = df.dropna(
        subset=(
            REQUIRED_COLUMNS +
            FEATURE_COLUMNS
        )
    ).copy()

    # Reset row index
    df.reset_index(
        drop=True,
        inplace=True
    )

    return df


# ============================================================
# EXTRACT MODEL FEATURES
# ============================================================

def extract_features(df):
    """
    Extract exactly the 20 features expected
    by the trained GCN model.
    """

    features = df[
        FEATURE_COLUMNS
    ].copy()

    return features


# ============================================================
# COMPLETE PREPROCESSING PIPELINE
# ============================================================

def preprocess_csv(csv_path):
    """
    Complete preprocessing pipeline:

    CSV
      ↓
    Load
      ↓
    Clean column names
      ↓
    Validate columns
      ↓
    Clean numerical values
      ↓
    Extract 20 model features

    Returns:
        cleaned_df
        feature_df
    """

    # Load
    df = load_csv(csv_path)

    # Clean column names
    df = clean_column_names(df)

    # Validate
    validate_columns(df)

    print("Column validation: PASSED")

    # Clean data
    cleaned_df = clean_data(df)

    print(
        "Valid rows after cleaning:",
        len(cleaned_df)
    )

    if len(cleaned_df) == 0:
        raise ValueError(
            "No valid network-flow rows remain "
            "after preprocessing."
        )

    # Extract model features
    feature_df = extract_features(
        cleaned_df
    )

    print(
        "Model features:",
        feature_df.shape
    )

    print("=" * 60)
    print("PREPROCESSING COMPLETED")
    print("=" * 60)

    return cleaned_df, feature_df