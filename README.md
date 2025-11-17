# Family Chores - Docker Setup

This project includes Docker configuration for easy deployment and development with SQLite database.

## Database Schema

The application uses SQLite with 3 tables:

### 1. `chores` table
- `chore_id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `chore` (TEXT NOT NULL)
- `point_value` (INTEGER NOT NULL)
- `repeat` (TEXT)

### 2. `user` table
- `user_id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `full_name` (TEXT NOT NULL)
- `balance` (INTEGER DEFAULT 0)

### 3. `transactions` table
- `transaction_id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `user_id` (INTEGER NOT NULL, FOREIGN KEY)
- `chore_id` (INTEGER, FOREIGN KEY)
- `value` (INTEGER NOT NULL)
- `timestamp` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

## Quick Start

### Build and run with Docker Compose
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

### Build Docker image manually
```bash
docker build -t family-chores .
docker run -p 8000:8000 family-chores
```

### Stop containers
```bash
docker-compose down
```

## API Endpoints

The Flask API provides the following endpoints:

### Chores
- `GET /api/chores` - Get all chores
- `POST /api/chores` - Create a new chore
  ```json
  {
    "chore": "Take out trash",
    "point_value": 5,
    "repeat": "daily"
  }
  ```

### Users
- `GET /api/users` - Get all users
- `POST /api/users` - Create a new user
  ```json
  {
    "full_name": "John Doe",
    "balance": 0
  }
  ```

### Transactions
- `GET /api/transactions` - Get all transactions
- `POST /api/transactions` - Create a new transaction
  ```json
  {
    "user_id": 1,
    "chore_id": 1,
    "value": 5,
    "timestamp": "2024-01-01T12:00:00"
  }
  ```

## Database

The SQLite database file (`family_chores.db`) is created automatically when the application starts. The database is persisted in a Docker volume, so your data will survive container restarts.

### Access database directly

```bash
# From within the container
docker-compose exec app sqlite3 family_chores.db

# Or from your host machine (if sqlite3 is installed)
sqlite3 family_chores.db
```

### Database location

The database file is stored in the application directory and is persisted via Docker volumes.

## Notes

- The database is automatically initialized when the container starts
- SQLite is file-based, so the database file is stored in the container volume
- For production, consider using PostgreSQL or MySQL for better performance and concurrent access
