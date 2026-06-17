from sqlalchemy import create_engine, text

DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "3308"
DB_NAME = "sales_db"

DB_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"

try:
    engine = create_engine(DB_URI)
    # Test the connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ DB CONFIG LOADED")
except Exception as e:
    print(f"❌ DB CONNECTION FAILED: {e}")
    raise