"""
init_db.py

Creates the original database schema (tables) used by the application.
This file intentionally contains only the original schema creation SQL
and does not include migration logic.
"""

import os
import psycopg2

# Database connection configuration from environment variables
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE', 'family_chores')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'family_chores')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'family_chores')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

# Construct database connection string
DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'


def init_database():
    """Create the original database schema matching the provided SQL dump."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        cursor = conn.cursor()

        # Original `user` table (named "user" in the dump)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "user" (
                user_id SERIAL PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                balance INTEGER DEFAULT 0,
                avatar_path VARCHAR(500)
            )
        """)

        # Chores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chores (
                chore_id SERIAL PRIMARY KEY,
                chore VARCHAR(255) NOT NULL,
                point_value INTEGER NOT NULL,
                repeat VARCHAR(50),
                last_completed TIMESTAMP,
                requires_approval BOOLEAN DEFAULT FALSE
            )
        """)

        # Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                description VARCHAR(255),
                value INTEGER NOT NULL,
                transaction_type VARCHAR(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES "user"(user_id)
            )
        """)

        # Cash balances
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cash_balances (
                user_id INTEGER PRIMARY KEY,
                cash_balance DOUBLE PRECISION DEFAULT 0.0,
                FOREIGN KEY (user_id) REFERENCES "user"(user_id)
            )
        """)

        # Settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                setting_key VARCHAR(100) PRIMARY KEY,
                setting_value VARCHAR(255) NOT NULL
            )
        """)

        # System log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_log (
                log_id SERIAL PRIMARY KEY,
                "timestamp" TIMESTAMP,
                log_type VARCHAR(100),
                message TEXT,
                details TEXT,
                status VARCHAR(50),
                ip_address VARCHAR(50)
            )
        """)

        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    init_database()

