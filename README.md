# Multilingual FAQ System

A Django-based FAQ system with multilingual support, WYSIWYG editor, and automatic translations.

## Features

- Multilingual FAQ management with support for English, Hindi, and Bengali
- Rich text editor (WYSIWYG) using CKEditor
- Automatic translation using Google Translate API
- Redis-based caching for improved performance
- RESTful API with language selection support
- Comprehensive test coverage
- Docker support for easy deployment

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```
5. Migrate models:
```bash
python manage.py makemigrations faq
# Edit .env with your settings
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```


```bash
#combined commands
# Delete old venv
rm -rf venv

# Create new venv with updated Python
python3.12 -m venv venv

# Activate venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```
## Running with Docker

```bash
docker-compose up --build
```

## API Usage

### List FAQs
```bash
# English (default)
curl http://localhost:8000/api/faqs/

# Hindi
curl http://localhost:8000/api/faqs/?lang=hi

# Bengali
curl http://localhost:8000/api/faqs/?lang=bn
```

### Create FAQ
```bash
curl -X POST http://localhost:8000/api/faqs/ \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Django?","answer":"Django is a web framework."}'
```

## Running Tests

```bash
# Run all tests
pytest
```


## Other Testing Commmands
```bash
# Install requirements (ensure you're in backend directory)
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Run unit tests (from project root)
python manage.py test faq

# Check PEP8 compliance
flake8 backend/

# Start development server
python manage.py runserver

# Test API endpoints (in separate terminal)
curl http://localhost:8000/api/faqs/
curl http://localhost:8000/api/faqs/?lang=hi
curl http://localhost:8000/api/faqs/?lang=bn
```

## Format the code
```bash
# Install formatting tools
pip install black isort

# Format code
black backend/
isort backend/

# Check again
flake8 backend/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

