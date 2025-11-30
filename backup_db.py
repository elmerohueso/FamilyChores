import os
import subprocess
from datetime import datetime

# Database connection configuration from environment variables
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE', 'family_chores')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'family_chores')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'family_chores')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

def backup_database(output_dir="backups"):

    backup_dir = "/data/backups"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{POSTGRES_DATABASE}_backup_{timestamp}.sql")

    cmd = [
        "pg_dump",
        "-h", POSTGRES_HOST,
        "-p", POSTGRES_PORT,
        "-U", POSTGRES_USER,
        "-f", backup_file,
        POSTGRES_DATABASE
    ]

    try:
        env = os.environ.copy()
        env["PGPASSWORD"] = POSTGRES_PASSWORD
        subprocess.run(cmd, check=True, env=env)
        print(f"Backup successful: {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return None

if __name__ == '__main__':
    backup_database()