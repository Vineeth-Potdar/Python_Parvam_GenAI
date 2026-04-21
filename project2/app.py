from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Database Configuration
DATABASE = 'students.db'

# Initialize Database
def init_db():
    """Initialize the database with tables"""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Students table
        cursor.execute('''
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                course TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

# Database connection helper
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, else to login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup route"""
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([full_name, email, phone, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))
        
        if len(password) < 8 or len(password) > 14:
            flash('Password must be 8-14 characters long.', 'danger')
            return redirect(url_for('signup'))
        
        # Check password requirements
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        if not (has_upper and has_lower and has_digit and has_special):
            flash('Password must contain uppercase, lowercase, digit, and special character.', 'danger')
            return redirect(url_for('signup'))
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            hashed_password = generate_password_hash(password)
            
            cursor.execute('''
                INSERT INTO users (name, email, phone, password)
                VALUES (?, ?, ?, ?)
            ''', (full_name, email, phone, hashed_password))
            
            conn.commit()
            conn.close()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('signup'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('login'))
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            conn.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_email'] = user['email']
                flash(f'Welcome, {user["name"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('login'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout route"""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ==================== DASHBOARD & USER ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page - show all users"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, phone FROM users')
        users = cursor.fetchall()
        conn.close()
        
        user = {
            'name': session.get('user_name'),
            'email': session.get('user_email')
        }
        
        return render_template('dashboard.html', user=user, users=users)
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

# ==================== STUDENT MANAGEMENT ROUTES ====================

@app.route('/students')
@login_required
def students():
    """View all students"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY id DESC')
        students_list = cursor.fetchall()
        conn.close()
        
        return render_template('students.html', students=students_list)
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('students'))

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        course = request.form.get('course')
        phone = request.form.get('phone')
        
        if not all([name, email, course, phone]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('add_student'))
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO students (name, email, course, phone)
                VALUES (?, ?, ?, ?)
            ''', (name, email, course, phone))
            
            conn.commit()
            conn.close()
            
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('add_student'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_student'))
    
    return render_template('add_student.html')

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    """Edit a student"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            course = request.form.get('course')
            phone = request.form.get('phone')
            
            if not all([name, email, course, phone]):
                flash('All fields are required.', 'danger')
                return redirect(url_for('edit_student', student_id=student_id))
            
            cursor.execute('''
                UPDATE students
                SET name = ?, email = ?, course = ?, phone = ?
                WHERE id = ?
            ''', (name, email, course, phone, student_id))
            
            conn.commit()
            conn.close()
            
            flash('Student updated successfully!', 'success')
            return redirect(url_for('students'))
        
        # GET request - show form with current data
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        
        if not student:
            flash('Student not found.', 'danger')
            return redirect(url_for('students'))
        
        return render_template('edit_student.html', student=student)
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('students'))

@app.route('/delete_student/<int:student_id>')
@login_required
def delete_student(student_id):
    """Delete a student"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        
        flash('Student deleted successfully!', 'success')
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('students'))

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# ==================== APPLICATION ENTRY POINT ====================

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
