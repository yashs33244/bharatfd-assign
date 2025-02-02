Here’s a well-structured and professional README for your Django-based multilingual FAQ system project:

---

# Multilingual FAQ System

A Django-based FAQ system with multilingual support, WYSIWYG editor, and automatic translations.

## Features

- Multilingual FAQ management supporting **English**, **Hindi**, and **Bengali**.
- Rich text editor (WYSIWYG) integration using **CKEditor** for FAQ answers.
- Automatic translation with **Google Translate API** or **googletrans** for language support.
- Performance optimization with **Redis-based caching**.
- RESTful API with language selection via query parameters (`?lang=hi`, `?lang=bn`, etc.).
- Comprehensive **unit test** coverage using **pytest**.
- Docker support for easy deployment.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Usage](#api-usage)
- [Running with Docker](#running-with-docker)
- [Running Tests](#running-tests)
- [Code Formatting](#format-the-code)
- [Contributing](#contributing)
- [Model Design](#model-design)
- [WYSIWYG Editor Integration](#wysiwyg-editor-integration)
- [API Development](#api-development)
- [Caching Mechanism](#caching-mechanism)
- [Multi-language Translation Support](#multi-language-translation-support)
- [Admin Panel](#admin-panel)
- [Tests & Code Quality](#unit-tests--code-quality)

---

## Installation

Follow these steps to set up the project locally.

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
.\venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your specific settings (e.g., API keys, secret keys)
```

### 5. Migrate models

```bash
python manage.py makemigrations faq
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

---

## Running with Docker

To run the application in a Docker container, use the following commands:

```bash
docker-compose up --build
```

---

## API Usage

### List FAQs

Fetch the FAQs in the default language (English) or other supported languages.

```bash
# English (default)
curl https://bharatfd.yashprojects.online/api/faqs/

# Hindi
curl https://bharatfd.yashprojects.online/api/faqs/?lang=hi

# Bengali
curl https://bharatfd.yashprojects.online/api/faqs/?lang=bn
```

### Create FAQ

Create a new FAQ entry.

```bash
curl -X POST http://localhost:8000/api/faqs/ \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Django?","answer":"Django is a web framework.","language":"en"}'

curl -X POST https://bharatfd.yashprojects.online/api/faqs/ \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Django?","answer":"Django is a web framework.","language":"en"}'
```

### Get FAQ

Fetch a single FAQ entry by ID.

```bash
curl http://localhost:8000/api/faqs/1/
curl https://bharatfd.yashprojects.online/api/faqs/1/
```

### Get All FAQs

Fetch all FAQs.

```bash
curl -X GET https://bharatfd.yashprojects.online/api/faqs/
```

---

## Running Tests

Run the following command to execute all tests in the project:

```bash
pytest
```

### Other Testing Commands

```bash
# Run database migrations
python manage.py migrate

# Run unit tests (from the project root)
python manage.py test faq

# Check PEP8 compliance
flake8 backend/

# Start development server
python manage.py runserver
```

---

## Format the Code

### Install Formatting Tools

```bash
pip install black isort
```

### Format Code

```bash
black backend/
isort backend/
flake8 backend/
```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Model Design

The FAQ model includes the following fields:

- `question`: TextField for the FAQ question.
- `answer`: RichTextField for the formatted FAQ answer using CKEditor.
- `language`: Language code (`en`, `hi`, `bn`).
- `question_hi`, `question_bn`: Translations for different languages.

Model Method:
- A method to retrieve the correct translated FAQ question and answer dynamically based on the requested language.

---

## WYSIWYG Editor Integration

I use **django-ckeditor** for the rich text editor that supports multilingual content. CKEditor is used to format the answer to FAQs, allowing for bold, italic, and other rich text features.

---

## API Development

The RESTful API supports managing FAQs with language selection through the query parameter `?lang=<language-code>`. It ensures multilingual content is returned based on the provided language.

---

## Caching Mechanism

**Redis** is used to cache FAQ data and translations. This ensures fast responses and reduces the number of API calls to the Google Translate API by caching translated text.

---

## Multi-language Translation Support

I use **Google Translate API** (or `googletrans` for free translation) to automate the translation of FAQs during object creation. If a translation is unavailable, it falls back to English.

---

## Admin Panel

The FAQ model is registered in the Django admin panel, where users can manage FAQs in different languages. The user-friendly interface allows admins to create and update FAQs with translations.

---

## Tests & Code Quality

### Unit Tests

Unit tests are written using **pytest** to test model methods and API responses.

### Code Quality

I follow **PEP8** conventions for Python code style and use **flake8** for linting. JavaScript-related tools like **eslint** (for front-end development) are used to ensure proper code quality.

---

## Deployment & Docker Support (Bonus)

A **Dockerfile** and **docker-compose.yml** are provided for containerizing the application. The application can be deployed to **Heroku** or **AWS**.

---
