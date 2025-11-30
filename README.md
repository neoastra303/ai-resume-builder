# AI Resume Builder

A cutting-edge platform for creating professional resumes with AI-powered enhancements.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-blue)

## Features

- **AI-Powered Enhancement**: Smart content suggestions and professional summary generation
- **Professional Templates**: Industry-specific designs for Tech, Executive, Academic, and Designer careers
- **Complete Customization**: Flexible layouts, color schemes, and typography controls
- **Enterprise Security**: Multi-factor authentication, GDPR compliance, and rate limiting
- **Modern UX**: Responsive design with drag-and-drop interface and real-time preview

## Quick Start

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd resume_builder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver --settings=resume_builder.settings.development
```

### Production Deployment

```bash
# Using Docker (recommended for production)
docker-compose up --build -d
```

## Technology Stack

- **Backend**: Django Framework with PostgreSQL
- **Frontend**: Tailwind CSS
- **AI Integration**: OpenAI API
- **Infrastructure**: Docker, Redis caching
- **Security**: OAuth, 2FA, Rate Limiting

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@neoastra303](https://twitter.com/neoastra303) - neozero3303@gmail.com

Project Link: [https://github.com/neoastra303/resume_builder](https://github.com/neoastra303/resume_builder)