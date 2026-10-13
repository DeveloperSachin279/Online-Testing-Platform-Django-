# TestFlow - Online Testing Platform

TestFlow is a modern Django-based online assessment platform designed for conducting exams, managing subjects and questions, tracking student performance, and generating detailed result reports.

## Features

- Student authentication and profile management
- Browse and attempt available tests
- Exam timer and question flow
- Automatic answer saving during test attempts
- Result calculation with score summary and review
- Admin panel for managing subjects, exams, and questions
- Student attempt tracking and analytics
- Clean, responsive UI with Django templates and custom CSS

## Tech Stack

- Python
- Django
- SQLite
- HTML, CSS, JavaScript

## Project Structure

- `accounts/` - Login, registration, and profile functionality
- `admin_panel/` - Admin dashboard and exam management
- `dashboard/` - Student dashboard and analytics
- `exams/` - Exams, subjects, questions, and attempt logic
- `results/` - Result generation and detailed reports
- `online_testing/` - Django project settings and routes
- `templates/` - Frontend template files
- `static/` - CSS, JS, and assets

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd online_testing
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

Open the app in your browser:

- Student app: http://127.0.0.1:8000
- Admin dashboard: http://127.0.0.1:8000/admin-dashboard/

## Screenshots

This project is designed for a modern assessment workflow with a clean dashboard, exam interface, and results page.

## Future Enhancements

- Role-based permissions
- Email-based password reset
- Question import/export
- PDF report generation
- Better exam security for live environments

## License

This project is for educational and learning purposes.

## Author

Built as a Django training project for online testing and assessment systems.
