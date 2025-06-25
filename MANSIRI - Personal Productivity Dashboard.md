# MANSIRI - Personal Productivity Dashboard

![MANSIRI Logo](static/images/logo.png)

**MANSIRI** is a comprehensive personal productivity dashboard that integrates task management, weather information, world clocks, news aggregation, and personal blogging into a single, elegant web application.

## 🌟 Features

### 🔐 User Authentication
- Secure user registration and login
- Profile management with customizable preferences
- Password reset functionality
- Session management and security

### ✅ Task Management
- Complete task lifecycle management
- Categories, priorities, and tags
- Time tracking and productivity analytics
- Kanban boards and calendar views
- Task comments and collaboration
- Reminder system with notifications

### 🌤️ Weather Integration
- Real-time weather data from OpenWeatherMap
- Multiple location support
- Weather alerts and notifications
- Historical weather data
- Customizable weather preferences

### 🕐 World Clock
- Multiple timezone support
- Customizable clock displays
- Business hours overlap calculator
- Clock alarms and reminders
- Daylight saving time awareness

### 📰 News Aggregator
- Latest news from multiple sources via NewsAPI
- Category-based news filtering
- Saved articles and reading lists
- Custom news feeds
- Search and discovery features

### 📝 Personal Blog
- Full-featured blogging system
- Rich text editor with media support
- Categories, tags, and series organization
- Comment system with moderation
- SEO optimization and social sharing

### 📊 Dashboard
- Unified view of all modules
- Customizable widgets and layout
- Real-time updates and notifications
- Responsive design for all devices
- Dark/light theme support

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/mansiri.git
   cd mansiri
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**
   - Open your browser to `http://localhost:8000`
   - Login with your superuser credentials

### Manual Installation

1. **Prerequisites**
   - Python 3.11+
   - PostgreSQL 15+
   - Redis 7+

2. **Setup**
   ```bash
   git clone https://github.com/your-username/mansiri.git
   cd mansiri
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure database**
   ```bash
   # Create PostgreSQL database
   createdb mansiri_dev
   
   # Run migrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Required API Keys

1. **OpenWeatherMap API**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Get your free API key
   - Add to `.env`: `OPENWEATHER_API_KEY=your_key_here`

2. **NewsAPI**
   - Sign up at [NewsAPI](https://newsapi.org/)
   - Get your free API key
   - Add to `.env`: `NEWS_API_KEY=your_key_here`

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=mansiri_dev
DB_USER=your_db_user
DB_PASSWORD=your_db_password
OPENWEATHER_API_KEY=your_openweather_key
NEWS_API_KEY=your_news_api_key
```

## 📖 Documentation

- **[Technical Documentation](TECHNICAL_DOCUMENTATION.md)** - Detailed technical information
- **[User Guide](USER_GUIDE.md)** - Complete user manual
- **[Quality Assurance](QA_CHECKLIST.md)** - Testing and QA information
- **[API Documentation](docs/api.md)** - API endpoints and usage

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific module tests
python manage.py test tests.accounts
python manage.py test tests.tasks

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🏗️ Architecture

### Technology Stack

- **Backend**: Django 4.2.7, Python 3.11
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Task Queue**: Celery with Redis broker
- **Deployment**: Docker, Docker Compose, Nginx

### Project Structure

```
mansiri/
├── accounts/           # User authentication
├── tasks/             # Task management
├── weather/           # Weather integration
├── worldclock/        # World clock feature
├── news/              # News aggregator
├── blog/              # Personal blog
├── templates/         # HTML templates
├── static/            # Static files
├── tests/             # Test suite
├── docs/              # Documentation
└── requirements.txt   # Dependencies
```

## 🚀 Deployment

### Production Deployment

1. **Configure production settings**
   ```bash
   export DJANGO_SETTINGS_MODULE=mansiri.settings_production
   ```

2. **Deploy with Docker**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

3. **SSL Configuration**
   ```bash
   # Using Let's Encrypt
   sudo certbot --nginx -d yourdomain.com
   ```

### Scaling

- **Horizontal scaling**: Multiple web server instances
- **Database scaling**: Read replicas and connection pooling
- **Cache scaling**: Redis cluster configuration
- **Background tasks**: Multiple Celery workers

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style

- Follow PEP 8 for Python code
- Use Black for code formatting
- Add docstrings for all functions and classes
- Write comprehensive tests

## 📊 Performance

### Benchmarks

- **Page Load Time**: < 2 seconds
- **API Response Time**: < 500ms
- **Database Queries**: Optimized with select_related()
- **Memory Usage**: < 512MB per worker
- **Concurrent Users**: 1000+ supported

### Optimization Features

- Database query optimization
- Redis caching for frequent data
- Static file compression and CDN support
- Lazy loading for images and content
- AJAX for dynamic updates

## 🔒 Security

### Security Features

- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS protection (Django templates)
- Secure password hashing
- Session security
- HTTPS enforcement in production

### Security Best Practices

- Regular security updates
- Input validation and sanitization
- Rate limiting on API endpoints
- Secure headers configuration
- Regular security audits

## 📈 Monitoring

### Application Monitoring

- **Health Checks**: `/health/` endpoint
- **Error Tracking**: Sentry integration
- **Performance Monitoring**: Built-in metrics
- **Log Aggregation**: Structured logging

### Metrics

- User activity and engagement
- Task completion rates
- API usage statistics
- Performance metrics
- Error rates and patterns

## 🆘 Support

### Getting Help

- **Documentation**: Check the docs folder
- **Issues**: [GitHub Issues](https://github.com/your-username/mansiri/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/mansiri/discussions)
- **Email**: support@mansiri.com

### Troubleshooting

Common issues and solutions:

1. **Database connection errors**: Check PostgreSQL service
2. **Redis connection errors**: Verify Redis is running
3. **API key errors**: Ensure API keys are configured
4. **Static files not loading**: Run `collectstatic`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django**: The web framework for perfectionists with deadlines
- **OpenWeatherMap**: Weather data API
- **NewsAPI**: News aggregation service
- **Bootstrap**: Frontend framework
- **Font Awesome**: Icon library
- **Contributors**: All the amazing people who contribute to this project

## 📞 Contact

- **Website**: https://mansiri.com
- **Email**: hello@mansiri.com
- **Twitter**: [@mansiri_app](https://twitter.com/mansiri_app)
- **GitHub**: [github.com/your-username/mansiri](https://github.com/your-username/mansiri)

---

**Made with ❤️ by the MANSIRI Team**

*MANSIRI - Your Personal Productivity Dashboard*

