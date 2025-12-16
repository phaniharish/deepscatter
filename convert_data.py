import pandas as pd
import glob
import os
import sys

DEST = "public/points.feather"
MANUAL_SRC = "/home/ubuntu/dataprep/data/duplicate_eval/asset_id_to_xy_coordinate_umap_100_neighbors_pca.parquet"

# 1. Locate the Parquet file
src_file = None
if MANUAL_SRC and os.path.exists(MANUAL_SRC):
    src_file = MANUAL_SRC
else:
    # Auto-search recursively if no path provided
    candidates = glob.glob("*.parquet") + glob.glob("../*.parquet") + glob.glob("/data/**/*.parquet", recursive=True)
    # Prefer files with "asset_id" in the name
    for f in candidates:
        if "asset_id" in f:
            src_file = f
            break
    if not src_file and candidates:
        src_file = candidates[0]

if not src_file:
    print("❌ FATAL: Could not find any .parquet file. Please edit PARQUET_FILE in the script.")
    sys.exit(1)

print(f"📄 Processing Data Source: {src_file}")

try:
    if not os.path.exists("public"): os.makedirs("public")

    df = pd.read_parquet(src_file)
    
    # Standardize Column Names (0->x, 1->y)
    rename_map = {}
    for col in df.columns:
        if str(col) in ['0', 'x']: rename_map[col] = 'x'
        if str(col) in ['1', 'y']: rename_map[col] = 'y'
    df.rename(columns=rename_map, inplace=True)

    # Ensure 'item_id' column exists
    if 'item_id' not in df.columns:
        if 'asset_id' in df.columns:
            df['item_id'] = df['asset_id']
        else:
            print("⚠️ No ID column found. Using DataFrame Index.")
            df['item_id'] = df.index.astype(str)
    
    # CRITICAL: Force ID to string (prevents missing data in visualization)
    df['item_id'] = df['item_id'].astype(str)
    
    # Save as uncompressed Feather (Fastest load time for Browser)
    df[['item_id', 'x', 'y']].to_feather(DEST, compression='uncompressed')
    print(f"✅ Success: Saved {len(df)} points to {DEST}")

except Exception as e:
    print(f"❌ Data Conversion Failed: {e}")
    sys.exit(1)
