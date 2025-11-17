import sqlite3
import os

# Database file path - use /data directory for persistence
DB_DIR = '/data'
os.makedirs(DB_DIR, exist_ok=True)
DB_FILE = os.path.join(DB_DIR, 'family_chores.db')

def init_database():
    """Initialize the SQLite database with the required tables."""
    
    # Remove existing database if it exists (for clean initialization)
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create chores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chores (
            chore_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chore TEXT NOT NULL,
            point_value INTEGER NOT NULL,
            repeat TEXT
        )
    ''')
    
    # Create user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            balance INTEGER DEFAULT 0,
            avatar_path TEXT
        )
    ''')
    
    # Add avatar_path column if it doesn't exist (for existing databases)
    try:
        cursor.execute('ALTER TABLE user ADD COLUMN avatar_path TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chore_id INTEGER,
            value INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(user_id),
            FOREIGN KEY (chore_id) REFERENCES chores(chore_id)
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database '{DB_FILE}' initialized successfully!")
    print("Tables created: chores, user, transactions")

if __name__ == '__main__':
    init_database()

