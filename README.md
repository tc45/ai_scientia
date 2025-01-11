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
```bash
.
├── README.md
├── requirements.txt
├── src
│   ├── accounts        # Handles all user authentication and management
│   ├── ai_scientia     # Project configuration
│   ├── blog            # Handles all blog posts and comments
│   ├── db.sqlite3      # SQLite database
│   ├── home            # Home page
│   ├── learning        # Learning center
│   ├── manage.py       # Django management script
│   ├── media           # Media files
│   ├── static          # Static files
│   ├── static_root     # Static root
│   └── templates       # Global templates
```

## License

This project is proprietary and confidential.
