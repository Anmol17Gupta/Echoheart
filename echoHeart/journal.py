import sqlite3
from datetime import datetime

# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()

    # Create journal table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        emotion TEXT,
        entry TEXT
    )
    """)
    conn.commit()
    conn.close()

# Call the function to ensure the table exists
initialize_db()

# Function to log user input into the journal
def log_entry(entry, emotion):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO journal (date, emotion, entry) VALUES (?, ?, ?)", (date, emotion, entry))
    
    conn.commit()
    conn.close()

# Function to retrieve the last 'n' journal entries
def get_recent_entries(limit=5):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT date, entry, emotion FROM journal ORDER BY id DESC LIMIT ?", (limit,))
    entries = cursor.fetchall()
    
    conn.close()
    return entries
