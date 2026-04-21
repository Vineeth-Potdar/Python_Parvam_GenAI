# Student Management System - Flask Web Application

A modern, responsive Flask web application for managing student records with user authentication and a clean Bootstrap 5 interface.

## ✨ Features

- **User Authentication**
  - User registration with password validation
  - Secure login/logout functionality
  - Session management
  
- **Dashboard**
  - Welcome message with user info
  - View all registered users in a table

- **Student Management**
  - Add new students
  - View all students
  - Edit student information
  - Delete students with confirmation dialog
  
- **Modern UI**
  - Bootstrap 5 responsive design
  - Clean, minimal interface
  - Mobile-friendly
  - Card-based layouts
  - Auto-dismissing flash messages

## 📁 Project Structure

```
project2/
├── app.py                      # Main Flask application
├── requirement.txt             # Python dependencies
├── templates/                  # HTML templates
│   ├── base.html              # Base template (navbar, footer, flash messages)
│   ├── login.html             # Login page
│   ├── signup.html            # Registration page
│   ├── dashboard.html         # User dashboard
│   ├── students.html          # Students list
│   ├── add_student.html       # Add new student form
│   └── edit_student.html      # Edit student form
├── static/                     # Static files (CSS, JS)
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── script.js           # Custom JavaScript
└── students.db                # SQLite database (created automatically)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory:**
```bash
cd project2
```

2. **Create a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirement.txt
```

### Running the Application

1. **Start the Flask development server:**
```bash
python app.py
```

2. **Open your browser and navigate to:**
```
http://localhost:5000
```

## 🔐 Default Behavior

- The application redirects to login page if not authenticated
- First-time users can create an account via the signup page
- Passwords are hashed for security
- All student management features require login

## 📝 Password Requirements

- 8–14 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character (!@#$%^&*)

## 💾 Database

- SQLite database (`students.db`) is automatically created on first run
- Two tables: `users` and `students`
- Database stores all user and student information

## 🎨 Customization

### Change Secret Key
Edit `app.py` line 8:
```python
app.secret_key = 'your_secret_key_here_change_in_production'
```

### Change Port
Edit `app.py` line 254:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Modify Database Path
Edit `app.py` line 11:
```python
DATABASE = 'students.db'  # Change database location
```

## 🔗 Application Routes

| Route | Method | Description | Authentication |
|-------|--------|-------------|-----------------|
| `/` | GET | Home (redirects to dashboard or login) | - |
| `/login` | GET, POST | User login | No |
| `/signup` | GET, POST | User registration | No |
| `/logout` | GET | User logout | Yes |
| `/dashboard` | GET | View all users | Yes |
| `/students` | GET | View all students | Yes |
| `/add_student` | GET, POST | Add new student | Yes |
| `/edit_student/<id>` | GET, POST | Edit student info | Yes |
| `/delete_student/<id>` | GET | Delete student | Yes |

## 🛡️ Security Features

- ✅ Password hashing with werkzeug
- ✅ Session-based authentication
- ✅ Email uniqueness validation
- ✅ CSRF protection ready
- ✅ SQL injection prevention
- ✅ Input validation on all forms

## 🎯 File Descriptions

### app.py
- Flask application setup
- Database initialization
- Route definitions
- Authentication logic
- Error handlers

### base.html
- Main template that other pages extend
- Responsive navbar
- Flash message handling
- Footer
- Bootstrap 5 integration

### login.html & signup.html
- Authentication forms
- Form validation
- Links to switch between login/signup

### dashboard.html
- Welcome message
- User list table
- Protected route

### students.html, add_student.html, edit_student.html
- Student management CRUD operations
- Responsive table
- Forms with validation
- Delete confirmation dialog

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Database Issues
Delete `students.db` to reset the database. It will be recreated on next run.

### Missing Templates
Ensure all HTML files are in the `templates/` folder and match the template names in `app.py`.

## 📦 Dependencies

- **Flask** - Web framework
- **Werkzeug** - WSGI utilities and password hashing
- **Jinja2** - Template engine
- **MarkupSafe** - String escaping for templating

## 🌐 Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📄 License

This project is open source and available for educational purposes.

## 💡 Future Enhancements

- [ ] User roles and permissions
- [ ] Email verification for signup
- [ ] Password reset functionality
- [ ] Student grades/marks management
- [ ] Export student data to CSV/PDF
- [ ] Search and filtering
- [ ] Dark mode
- [ ] User profile management

## 📞 Support

For issues or questions, check the Flask documentation at https://flask.palletsprojects.com/

---

**Happy Coding! 🚀**
