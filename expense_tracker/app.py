from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')

@app.route('/')
@app.route('/dashboard')
def dashboard():
    category_filter = request.args.get('category', '')
    conn = get_db()
    if category_filter:
        expenses = conn.execute('SELECT * FROM expenses WHERE category = ? ORDER BY date DESC', (category_filter,)).fetchall()
    else:
        expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    total = conn.execute('SELECT SUM(amount) as total FROM expenses').fetchone()['total'] or 0
    categories = conn.execute('SELECT DISTINCT category FROM expenses').fetchall()
    return render_template('dashboard.html', expenses=expenses, total=total, categories=[c['category'] for c in categories], selected_category=category_filter)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        conn = get_db()
        conn.execute('INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)', (title, amount, category, date))
        conn.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = get_db()
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        conn.execute('UPDATE expenses SET title = ?, amount = ?, category = ?, date = ? WHERE id = ?', (title, amount, category, date, id))
        conn.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    expense = conn.execute('SELECT * FROM expenses WHERE id = ?', (id,)).fetchone()
    return render_template('edit_expense.html', expense=expense)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    conn = get_db()
    conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)