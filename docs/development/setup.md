# Development Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 16 or higher
- Docker and Docker Compose (optional but recommended)
- PostgreSQL (if not using Docker)
- Redis (if not using Docker)

## Quick Start with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/neoastra303/ai-resume-builder.git
   cd ai-resume-builder
   ```

2. Copy the environment example file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` with your configuration values

4. Build and start the services:
   ```bash
   docker-compose up --build
   ```

5. Run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. Access the application at `http://localhost:8000`

## Manual Setup

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/neoastra303/ai-resume-builder.git
   cd ai-resume-builder
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver --settings=resume_builder.settings.development
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Environment Variables

The following environment variables are required:

- `DJANGO_SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection URL
- `REDIS_URL`: Redis connection URL
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `DEBUG`: Set to True for development

See `.env.example` for a complete list of required variables.

## Running Tests

To run the test suite:

```bash
python manage.py test
```

## Code Quality

We use the following tools to maintain code quality:

- **Black**: Code formatter
- **Flake8**: Linting
- **isort**: Import sorting

Run these before committing:

```bash
black .
flake8 .
isort .
```

## Database Migrations

To create and apply migrations:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details on our development process and how to propose changes.