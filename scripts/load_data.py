import pandas as pd
import os
from db.db_config import engine

# Build path relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "sales.csv")

try:
    print(f"📂 Loading CSV from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)

    print(f"📊 Rows found in CSV: {len(df)}")
    print(f"📋 Columns: {list(df.columns)}")

    df.to_sql("sales", con=engine, if_exists="replace", index=False)

    print("✅ Data loaded into MySQL successfully!")
    print(f"✅ {len(df)} rows inserted into 'sales' table.")

except FileNotFoundError:
    print(f"❌ CSV file not found at: {CSV_PATH}")
    print("Make sure 'sales.csv' is inside the 'data/' folder.")
except Exception as e:
    print(f"❌ Error loading data: {e}")