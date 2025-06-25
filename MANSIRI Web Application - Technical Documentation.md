# MANSIRI Web Application - Technical Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [Deployment](#deployment)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Testing](#testing)
9. [Maintenance](#maintenance)
10. [Troubleshooting](#troubleshooting)

## Project Overview

MANSIRI is a comprehensive personal dashboard web application built with Django that provides users with an integrated platform for productivity and information management.

### Key Features

- **User Authentication**: Secure registration, login, and profile management
- **Task Management**: Complete task lifecycle with categories, priorities, and time tracking
- **Weather Integration**: Real-time weather data from OpenWeatherMap API
- **World Clock**: Multi-timezone clock display with user preferences
- **News Aggregator**: Latest news from multiple sources via NewsAPI
- **Personal Blog**: Full-featured blogging system with comments and categories
- **Responsive Design**: Mobile-friendly interface with modern UI/UX

### Technology Stack

- **Backend**: Django 4.2.7, Python 3.11
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Task Queue**: Celery with Redis broker
- **Deployment**: Docker, Docker Compose, Nginx
- **Monitoring**: Sentry (optional)

## Architecture

### Application Structure

```
mansiri_project/
├── mansiri/                 # Main project directory
│   ├── settings.py         # Development settings
│   ├── settings_production.py  # Production settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── views.py            # Main views (home, dashboard)
├── accounts/               # User authentication module
├── tasks/                  # Task management module
├── weather/                # Weather integration module
├── worldclock/             # World clock module
├── news/                   # News aggregator module
├── blog/                   # Personal blog module
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── manage.py              # Django management script
```

### Database Design

The application uses a modular database design with the following key models:

#### User Management
- `User`: Extended Django user model with additional profile fields
- `UserProfile`: Additional user preferences and settings

#### Task Management
- `Task`: Core task model with status, priority, and categorization
- `TaskCategory`: User-defined task categories
- `TaskPriority`: System-defined priority levels
- `TaskReminder`: Task reminder system
- `TaskComment`: Task collaboration comments
- `TaskTimeLog`: Time tracking for tasks
- `TaskTemplate`: Reusable task templates
- `TaskBoard`: Kanban-style task boards
- `TaskStatistics`: User productivity analytics

#### Weather System
- `City`: Weather location data
- `WeatherData`: Current weather information
- `UserWeatherPreference`: User weather preferences
- `WeatherAlert`: Weather alert system

#### World Clock
- `TimeZone`: Timezone information
- `WorldClock`: User's world clocks
- `ClockAlarm`: Clock-based alarms
- `UserClockPreferences`: Clock display preferences

#### News System
- `NewsSource`: News source information
- `Article`: News articles
- `NewsCategory`: Article categorization
- `UserNewsPreference`: User news preferences
- `SavedArticle`: User-saved articles

#### Blog System
- `BlogPost`: Blog post content
- `BlogCategory`: Blog categorization
- `BlogTag`: Blog tagging system
- `BlogComment`: Blog comments
- `BlogSeries`: Multi-part blog series

## Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (for frontend assets)
- Docker & Docker Compose (for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mansiri_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Docker Development Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | - | Yes |
| `DEBUG` | Debug mode | False | No |
| `DB_NAME` | Database name | mansiri_prod | Yes |
| `DB_USER` | Database user | mansiri_user | Yes |
| `DB_PASSWORD` | Database password | - | Yes |
| `DB_HOST` | Database host | localhost | No |
| `DB_PORT` | Database port | 5432 | No |
| `REDIS_URL` | Redis connection URL | redis://127.0.0.1:6379/1 | No |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | - | Yes |
| `NEWS_API_KEY` | NewsAPI key | - | Yes |
| `EMAIL_HOST` | SMTP host | smtp.gmail.com | No |
| `EMAIL_HOST_USER` | SMTP username | - | No |
| `EMAIL_HOST_PASSWORD` | SMTP password | - | No |
| `SENTRY_DSN` | Sentry monitoring DSN | - | No |

### API Keys Setup

#### OpenWeatherMap API
1. Register at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Add to environment variables: `OPENWEATHER_API_KEY=your_key_here`

#### NewsAPI
1. Register at [NewsAPI](https://newsapi.org/)
2. Get your free API key
3. Add to environment variables: `NEWS_API_KEY=your_key_here`

### Database Configuration

#### PostgreSQL Setup
```sql
CREATE DATABASE mansiri_prod;
CREATE USER mansiri_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mansiri_prod TO mansiri_user;
ALTER USER mansiri_user CREATEDB;
```

#### Redis Setup
```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

## Deployment

### Production Deployment with Docker

1. **Prepare environment**
   ```bash
   cp .env.example .env
   # Configure production values in .env
   ```

2. **Build and deploy**
   ```bash
   docker-compose -f docker-compose.yml up -d --build
   ```

3. **Run initial setup**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py collectstatic --noinput
   docker-compose exec web python manage.py createsuperuser
   ```

### Manual Production Deployment

1. **Server setup**
   ```bash
   # Install dependencies
   sudo apt-get update
   sudo apt-get install python3.11 python3.11-venv postgresql redis-server nginx
   ```

2. **Application setup**
   ```bash
   # Clone and setup application
   git clone <repository-url> /var/www/mansiri
   cd /var/www/mansiri
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure services**
   ```bash
   # Configure Gunicorn
   pip install gunicorn
   
   # Configure Nginx
   sudo cp nginx.conf /etc/nginx/sites-available/mansiri
   sudo ln -s /etc/nginx/sites-available/mansiri /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

4. **Setup systemd services**
   ```bash
   # Create systemd service files for Gunicorn, Celery, etc.
   sudo systemctl enable mansiri
   sudo systemctl start mansiri
   ```

### SSL Configuration

1. **Install Certbot**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. **Obtain SSL certificate**
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Auto-renewal**
   ```bash
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

## API Documentation

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts/login/` | POST | User login |
| `/accounts/register/` | POST | User registration |
| `/accounts/logout/` | GET | User logout |
| `/accounts/profile/` | GET/POST | User profile |

### Task Management Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tasks/` | GET | Task dashboard |
| `/tasks/list/` | GET | Task list |
| `/tasks/create/` | GET/POST | Create task |
| `/tasks/<id>/` | GET | Task detail |
| `/tasks/<id>/edit/` | GET/POST | Edit task |
| `/tasks/<id>/delete/` | POST | Delete task |

### AJAX Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tasks/ajax/update-status/` | POST | Update task status |
| `/tasks/ajax/toggle-importance/` | POST | Toggle task importance |
| `/tasks/ajax/add-comment/` | POST | Add task comment |
| `/tasks/ajax/start-tracking/` | POST | Start time tracking |
| `/tasks/ajax/stop-tracking/` | POST | Stop time tracking |

### Weather Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/weather/` | GET | Weather dashboard |
| `/weather/search/` | GET/POST | Search weather |
| `/weather/city/<id>/` | GET | City weather detail |

### News Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/news/` | GET | News dashboard |
| `/news/search/` | GET/POST | Search news |
| `/news/category/<slug>/` | GET | Category news |

### Blog Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/blog/` | GET | Blog home |
| `/blog/post/<slug>/` | GET | Blog post detail |
| `/blog/create/` | GET/POST | Create blog post |
| `/blog/category/<slug>/` | GET | Category posts |

## Database Schema

### Key Relationships

```sql
-- User to Tasks (One-to-Many)
User ||--o{ Task : creates

-- Task to Category (Many-to-One)
Task }o--|| TaskCategory : belongs_to

-- Task to Priority (Many-to-One)
Task }o--|| TaskPriority : has

-- Task to Comments (One-to-Many)
Task ||--o{ TaskComment : has

-- Task to Time Logs (One-to-Many)
Task ||--o{ TaskTimeLog : tracks

-- User to Weather Preferences (One-to-Many)
User ||--o{ UserWeatherPreference : has

-- User to World Clocks (One-to-Many)
User ||--o{ WorldClock : owns

-- User to Blog Posts (One-to-Many)
User ||--o{ BlogPost : authors

-- Blog Post to Comments (One-to-Many)
BlogPost ||--o{ BlogComment : receives
```

### Indexes

The application includes optimized database indexes for:
- User-based queries (user_id indexes)
- Date-based queries (created_at, due_date indexes)
- Status-based queries (status indexes)
- Search functionality (text indexes)

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific module tests
python manage.py test tests.accounts
python manage.py test tests.tasks

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Structure

- **Unit Tests**: Model and form validation
- **Integration Tests**: View and workflow testing
- **AJAX Tests**: Dynamic functionality testing
- **Performance Tests**: Response time validation

### Test Coverage

Current test coverage includes:
- User authentication: 95%
- Task management: 90%
- Core functionality: 85%
- API endpoints: 80%

## Maintenance

### Regular Tasks

1. **Database Maintenance**
   ```bash
   # Backup database
   pg_dump mansiri_prod > backup_$(date +%Y%m%d).sql
   
   # Optimize database
   python manage.py dbshell
   VACUUM ANALYZE;
   ```

2. **Log Rotation**
   ```bash
   # Configure logrotate
   sudo nano /etc/logrotate.d/mansiri
   ```

3. **Update Dependencies**
   ```bash
   pip list --outdated
   pip install -U package_name
   pip freeze > requirements.txt
   ```

4. **Monitor Performance**
   ```bash
   # Check system resources
   htop
   
   # Check database performance
   python manage.py dbshell
   SELECT * FROM pg_stat_activity;
   ```

### Backup Strategy

1. **Database Backups**
   - Daily automated backups
   - Weekly full backups
   - Monthly archive backups

2. **File Backups**
   - Media files backup
   - Configuration backup
   - Log files archive

3. **Monitoring**
   - Application health checks
   - Database performance monitoring
   - Error rate tracking

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
python manage.py dbshell
```

#### Redis Connection Issues
```bash
# Check Redis status
sudo systemctl status redis-server

# Test Redis connection
redis-cli ping
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check Nginx configuration
sudo nginx -t
sudo systemctl reload nginx
```

#### Celery Tasks Not Running
```bash
# Check Celery worker status
celery -A mansiri inspect active

# Restart Celery workers
sudo systemctl restart celery
```

### Performance Issues

1. **Slow Database Queries**
   - Enable query logging
   - Use Django Debug Toolbar
   - Optimize with select_related() and prefetch_related()

2. **High Memory Usage**
   - Monitor with htop
   - Check for memory leaks
   - Optimize Celery worker configuration

3. **Slow Page Load Times**
   - Enable browser caching
   - Optimize static files
   - Use CDN for static assets

### Error Monitoring

1. **Application Errors**
   - Check Django logs: `/app/logs/django.log`
   - Monitor Sentry dashboard
   - Review error patterns

2. **System Errors**
   - Check system logs: `/var/log/syslog`
   - Monitor disk space: `df -h`
   - Check memory usage: `free -h`

### Support and Documentation

- **Django Documentation**: https://docs.djangoproject.com/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Redis Documentation**: https://redis.io/documentation
- **Celery Documentation**: https://docs.celeryproject.org/

---

**Last Updated**: June 2025
**Version**: 1.0.0
**Maintainer**: MANSIRI Development Team

