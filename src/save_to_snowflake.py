import snowflake.connector
from src.config import SNOWFLAKE_CONFIG
import uuid
import datetime
from config import SNOWFLAKE_CONFIG

def save_resume_analysis(user_email, industry, job_role, score, matched_keywords, missing_keywords):
    conn = snowflake.connector.connect(
    account=SNOWFLAKE_CONFIG["account"],
    user=SNOWFLAKE_CONFIG["user"],
    password=SNOWFLAKE_CONFIG["password"],
    role=SNOWFLAKE_CONFIG["role"],
    warehouse=SNOWFLAKE_CONFIG["warehouse"],
    database=SNOWFLAKE_CONFIG["database"],
    schema=SNOWFLAKE_CONFIG["schema"]
    )

    try:
        cursor = conn.cursor()

        # Optional: Debug current DB and schema
        cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();")
        print("Connected to →", cursor.fetchone())

        insert_query = """
        INSERT INTO RESUME_ANALYTICS (
            id, timestamp, user_email, industry, job_role, match_score, matched_keywords, missing_keywords
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            str(uuid.uuid4()),
            datetime.datetime.utcnow(),
            user_email,
            industry,
            job_role,
            score,
            ", ".join(matched_keywords),
            ", ".join(missing_keywords)
        ))

        conn.commit()
    finally:
        cursor.close()
        conn.close()
