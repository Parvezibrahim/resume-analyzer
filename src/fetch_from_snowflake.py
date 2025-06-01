import pandas as pd
import snowflake.connector
from src.config import SNOWFLAKE_CONFIG
from src.config import SNOWFLAKE_CONFIG  # ✅ use the dictionary

def fetch_saved_analytics():
    """Fetches saved resume analysis data from Snowflake and returns it as a DataFrame."""
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_CONFIG["user"],
        password=SNOWFLAKE_CONFIG["password"],
        account=SNOWFLAKE_CONFIG["account"],
        warehouse=SNOWFLAKE_CONFIG["warehouse"],
        database=SNOWFLAKE_CONFIG["database"],
        schema=SNOWFLAKE_CONFIG["schema"]
    )

    query = f"SELECT * FROM {SNOWFLAKE_CONFIG['table']}"  # ✅ fixed
    df = pd.read_sql(query, conn)
    conn.close()
    return df
