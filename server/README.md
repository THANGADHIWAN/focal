# Sample Management API

A FastAPI-based backend for managing laboratory samples, aliquots, and tests.

## Features

- **Sample Management**: Create, read, update, and delete samples
- **Aliquot Management**: Create and track aliquots from samples
- **Test Tracking**: Schedule and record test results for aliquots
- **Metadata Management**: Manage sample types, lab locations, and users
- **Data Export**: Export sample data as CSV
- **Authentication**: Secure API endpoints with JWT authentication
- **Pagination and Filtering**: Advanced filtering options for samples

## Getting Started

### Prerequisites

- Python 3.9+
- Python 3.8 or higher
- Docker and Docker Compose (for PostgreSQL)
- pip (Python package installer)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd server

# Create and activate a virtual environment
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
# Start PostgreSQL with Docker
docker-compose up -d

# Run database migrations
alembic upgrade head

# Seed the database with initial data
python -m app.db.seed_data
```

### Running the Application

```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Obtain a token by sending a POST request to `/auth/token` with your credentials.
2. Include the token in the `Authorization` header for protected endpoints:

```
Authorization: Bearer your_jwt_token
```

## Project Structure

```
server/
├── alembic/              # Database migration scripts
├── app/
│   ├── api/
│   │   └── routes/       # API route definitions
│   ├── core/             # Core application settings
│   ├── db/               # Database configuration and scripts
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic schemas for request/response validation
│   ├── services/         # Business logic services
│   └── utils/            # Utility functions
├── requirements.txt      # Project dependencies
├── alembic.ini           # Alembic configuration
└── docker-compose.yml    # Docker Compose configuration for services
```
