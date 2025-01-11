# AI_Scientia Platform

AI_Scientia is a comprehensive learning platform focused on Artificial Intelligence and Generative AI education. The platform provides structured learning paths, interactive demonstrations, and expert insights into AI technologies.

## Features

- **Learning Center**: Structured tutorials and courses on AI
- **Blog System**: Latest updates and insights about AI
- **Interactive Demos**: Hands-on AI technology demonstrations
- **User Management**: Custom user profiles and authentication
- **Responsive Design**: Mobile-friendly interface

## Technology Stack

- Python 3.12
- Django 5.0.2
- Bootstrap 5
- SQLite (Development) / PostgreSQL (Production)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tc45/ai-scientia.git
   cd ai-scientia
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

ai_scientia/
├── src/
│   ├── ai_scientia/      # Project configuration
│   ├── learning/         # Learning app
│   ├── blog/            # Blog app
│   ├── accounts/        # User management
│   ├── templates/       # Global templates
│   └── static/         # Static files
├── requirements.txt
└── README.md

## License

This project is proprietary and confidential.
