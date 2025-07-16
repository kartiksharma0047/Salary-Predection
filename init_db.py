# Script for creating a table
import sqlite3

# Connect (or create if not exists)
conn = sqlite3.connect("salary_cache.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_hash TEXT UNIQUE,
        result TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()

print("✅ Database and table created successfully.")
