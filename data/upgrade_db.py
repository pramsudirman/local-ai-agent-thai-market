import apsw
import sqlite_vec
import json
from sentence_transformers import SentenceTransformer

def upgrade_to_vector_db():
    print("🔌 Connecting to database using APSW...")
    db_path = "data/thai_news.db"
    
    # 1. Load the AI Model
    print("🧠 Loading AI Model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    conn = apsw.Connection(db_path)
    conn.enableloadextension(True)
    conn.loadextension(sqlite_vec.loadable_path()) 
    
    cursor = conn.cursor()

    # 2. RESET THE TABLE (Crucial to fix your schema error)
    print("🧹 Cleaning up old vector table...")
    cursor.execute("DROP TABLE IF EXISTS vec_news")

    # 3. Create the table correctly
    # NOTE: We removed 'PRIMARY KEY' from id. 
    # Virtual tables use an internal integer rowid automatically.
    print("📦 Creating vector table...")
    cursor.execute("""
        CREATE VIRTUAL TABLE vec_news USING vec0(
            news_id TEXT,
            embedding FLOAT[384]
        )
    """)

    # 4. Generate embeddings
    print("🔄 Reading existing news...")
    rows = list(cursor.execute("SELECT id, full_content FROM news"))
    
    print(f"🚀 Generating embeddings for {len(rows)} articles...")
    count = 0
    
    cursor.execute("BEGIN TRANSACTION")
    for news_id, content in rows:
        embedding = model.encode(content).tolist()
        
        # Save to DB
        cursor.execute(
            "INSERT INTO vec_news(news_id, embedding) VALUES (?, ?)",
            (news_id, json.dumps(embedding))
        )
        count += 1
    
    cursor.execute("COMMIT")
    conn.close()
    print(f"✅ Success! Database upgraded. Added {count} new vectors.")

if __name__ == "__main__":
    upgrade_to_vector_db()