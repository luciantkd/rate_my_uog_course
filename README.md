# Rate My UoG Course

A Django-based platform for students to rate and provide feedback on university courses at the University of Glasgow.

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## About the Project

Rate My UoG Course is a web application designed to help students provide honest feedback on their university courses. This feedback helps both future students and university administrators understand the course quality and areas for improvement.

## Features

- User authentication for students and administrators
- Course rating and feedback submission
- Search and filter functionality for courses
- Google ReCAPTCHA for spam prevention on login and signup
- Admin dashboard for managing feedback

## Technologies Used

- **Backend**: Django (Python)
- **Database**: SQLite (or other databases as configured)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: Google ReCAPTCHA

## Getting Started

To set up this project locally, follow these steps.

### Prerequisites

- Python 3.x
- Django 2.1.5 or later
- Pip (Python package manager)
- Git (for version control)

### Installation

1. **Clone the Repository**
   git clone git@github.com:luciantkd/rate_my_uog_course.git
   cd rate_my_uog_course
   
3. **Create a Virtual Environment**
  python3 -m venv venv
  source venv/bin/activate  # For Windows: venv\Scripts\activate

4. **Install Dependencies**
  pip install -r requirements.txt

5. **Apply Migrations**
  python manage.py migrate

6. **Run the Development Server**
  python manage.py runserver

### The app should now be running at http://127.0.0.1:8000/.

### Usage
Home Page: Explore courses and view ratings.
User Signup/Login: Create an account or log in to rate courses.
Admin Access: Administrators can log in to manage feedback and view course insights.
Contributing
Contributions are welcome! Please follow these steps to contribute:

### Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
Distributed under the MIT License. See LICENSE for more information.

### Contact
Project Maintainer - Lucian Procopciuc
GitHub Repository - Rate My UoG Course


### Additional Tips
1. **Update `requirements.txt`**: Run `pip freeze > requirements.txt` to capture dependencies.
2. **Add Screenshots**: Consider adding screenshots of key pages for better visualization.
3. **Detailed Setup**: Expand the setup steps for clarity if more configurations are needed (e.g., for databases or specific environment settings). 

This `README.md` provides an overview and setup guide, making it easy for others to understand, set up, and contribute to your project.

