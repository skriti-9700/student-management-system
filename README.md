# Student Management System

A web-based Student Management System developed using Python and Flask. This application provides a simple interface to manage student records and their course enrollments.

## Features

- View all registered students.
- Add new student records.
- View individual student details.
- Update student information.
- Enroll students in courses.
- Modify course enrollments.
- Delete student records.
- Prevent duplicate student roll numbers.

## Technologies Used

- **Programming Language:** Python
- **Backend Framework:** Flask
- **Database:** SQLite
- **ORM:** Flask-SQLAlchemy
- **Frontend:** HTML and CSS
- **Templating Engine:** Jinja2

## Project Structure

```text
student-management-system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── create.html
│   ├── details.html
│   ├── update.html
│   └── exists.html
│
└── static/
    └── style.css
```

## Getting Started

Follow these instructions to run the project locally.

### Prerequisites

- Python installed on your system.

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

Replace `YOUR_REPOSITORY_URL` with the URL of this GitHub repository.

### 2. Navigate to the Project Directory

```bash
cd student-management-system
```

### 3. Create a Virtual Environment

```bash
py -m venv venv
```

### 4. Activate the Virtual Environment

On Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
py -m pip install -r requirements.txt
```

### 6. Database Setup

The application uses SQLite with Flask-SQLAlchemy.

The required database tables and course records must be set up before using the application. The SQLite database file is not included in this repository.

### 7. Run the Application

```bash
py app.py
```

Open the following URL in your browser:

http://127.0.0.1:5000

## Learning Outcomes

This project demonstrates practical implementation of:

- Flask web application development.
- Database integration using Flask-SQLAlchemy.
- Create, Read, Update and Delete (CRUD) operations.
- Relational database management.
- Form handling and validation.
- Dynamic HTML rendering using Jinja2.
- Basic frontend development using HTML and CSS.

## Future Improvements

- User authentication and authorization.
- Search and filtering functionality.
- Responsive user interface.
- Pagination for student records.
- Enhanced form validation.

---

**Developed using Python, Flask and SQLite.**