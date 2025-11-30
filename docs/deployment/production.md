# Deployment Guide

## Production Deployment with Docker

The recommended way to deploy the AI Resume Builder is using Docker Compose.

### Prerequisites

- Docker 20.10 or higher
- Docker Compose 1.29 or higher
- Domain name (optional but recommended)
- SSL certificate (optional but recommended)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/neoastra303/ai-resume-builder.git
   cd ai-resume-builder
   ```

2. Copy the production environment example:
   ```bash
   cp .env.production.example .env
   ```

3. Edit `.env` with your production configuration:
   - Set strong secrets for `DJANGO_SECRET_KEY`
   - Configure your database settings
   - Add your OpenAI API key
   - Set `DEBUG=False`

4. Build and start the services:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

5. Run migrations:
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   ```

7. Collect static files:
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   ```

## Manual Deployment

### Server Requirements

- Ubuntu 20.04 LTS or higher (recommended)
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher
- Nginx
- Certbot (for SSL)

### Steps

1. Update system packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install dependencies:
   ```bash
   sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib redis nginx -y
   ```

3. Create database and user:
   ```sql
   sudo -u postgres psql
   CREATE DATABASE resume_builder;
   CREATE USER resume_user WITH PASSWORD 'strong_password';
   ALTER ROLE resume_user SET client_encoding TO 'utf8';
   ALTER ROLE resume_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE resume_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE resume_builder TO resume_user;
   \q
   ```

4. Clone the repository:
   ```bash
   git clone https://github.com/neoastra303/ai-resume-builder.git
   cd ai-resume-builder
   ```

5. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

6. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

7. Configure environment variables in `.env`:
   ```bash
   cp .env.production.example .env
   nano .env  # Edit with your values
   ```

8. Run migrations:
   ```bash
   python manage.py migrate --settings=resume_builder.settings.production
   ```

9. Create superuser:
   ```bash
   python manage.py createsuperuser --settings=resume_builder.settings.production
   ```

10. Collect static files:
    ```bash
    python manage.py collectstatic --noinput --settings=resume_builder.settings.production
    ```

11. Configure Gunicorn:
    ```bash
    sudo nano /etc/systemd/system/resume-builder.service
    ```

    Add the following content:
    ```
    [Unit]
    Description=AI Resume Builder
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/path/to/your/project
    ExecStart=/path/to/your/project/venv/bin/gunicorn --workers 3 --bind unix:/path/to/your/project/resume_builder.sock resume_builder.wsgi:application
    ExecReload=/bin/kill -s HUP $MAINPID
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

12. Start and enable the service:
    ```bash
    sudo systemctl start resume-builder
    sudo systemctl enable resume-builder
    ```

13. Configure Nginx:
    ```bash
    sudo nano /etc/nginx/sites-available/resume-builder
    ```

    Add the following content:
    ```
    server {
        listen 80;
        server_name your_domain.com;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /path/to/your/project;
        }

        location /media/ {
            root /path/to/your/project;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/path/to/your/project/resume_builder.sock;
        }
    }
    ```

14. Enable the site:
    ```bash
    sudo ln -s /etc/nginx/sites-available/resume-builder /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

15. Set up SSL with Certbot:
    ```bash
    sudo certbot --nginx -d your_domain.com
    ```

## Monitoring and Maintenance

### Logs

View application logs:
```bash
docker-compose logs -f web
```

For manual deployments:
```bash
journalctl -u resume-builder -f
```

### Backups

Regular database backups are essential:
```bash
docker-compose exec db pg_dump -U resume_user resume_builder > backup_$(date +%F).sql
```

### Updates

To update to the latest version:
```bash
git pull origin master
docker-compose down
docker-compose up --build -d
docker-compose exec web python manage.py migrate
```

## Scaling

For high-traffic deployments, consider:

1. Load balancing multiple application instances
2. Database read replicas
3. CDN for static assets
4. Redis cluster for caching
5. Horizontal pod autoscaling (if using Kubernetes)

## Troubleshooting

### Common Issues

1. **Permission errors**: Ensure proper file ownership and permissions
2. **Database connection failures**: Check database credentials and network connectivity
3. **Static files not loading**: Verify `collectstatic` was run and Nginx configuration
4. **Memory issues**: Monitor resource usage and adjust container limits

### Health Checks

Implement health checks for your services:
```bash
# Application health check
curl -f http://localhost:8000/health/

# Database health check
docker-compose exec db pg_isready
```

For production environments, set up proper monitoring and alerting systems.