from flask import Flask, render_template, request, redirect, url_for, flash, g, jsonify
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        db.commit()

# Create schema.sql if it doesn't exist
if not os.path.exists('schema.sql'):
    with open('schema.sql', 'w') as f:
        f.write("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    budget REAL NOT NULL,
    expected_guests INTEGER NOT NULL,
    ticket_price REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT NOT NULL,
    event_id INTEGER,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY (event_id) REFERENCES events (id)
);

CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    service_type TEXT NOT NULL,
    cost REAL NOT NULL,
    event_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES events (id)
);
""")

# Initialize database
init_db()

# Helper functions
def get_event_cost(event_id):
    db = get_db()
    vendor_cost = db.execute('SELECT SUM(cost) FROM vendors WHERE event_id = ?', (event_id,)).fetchone()[0] or 0
    event = db.execute('SELECT budget FROM events WHERE id = ?', (event_id,)).fetchone()
    return event['budget'] + vendor_cost if event else 0

def get_event_revenue(event_id):
    db = get_db()
    event = db.execute('SELECT expected_guests, ticket_price FROM events WHERE id = ?', (event_id,)).fetchone()
    return event['expected_guests'] * event['ticket_price'] if event else 0

def get_event_profit(event_id):
    return get_event_revenue(event_id) - get_event_cost(event_id)

# Routes
@app.route('/')
def dashboard():
    db = get_db()
    
    # Summary cards
    total_events = db.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    total_revenue = sum(get_event_revenue(row['id']) for row in db.execute('SELECT id FROM events').fetchall())
    total_bookings = db.execute('SELECT COUNT(*) FROM customers WHERE status = "Confirmed"').fetchone()[0]
    total_customers = db.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
    
    # Recent events
    recent_events = db.execute('SELECT * FROM events ORDER BY date DESC LIMIT 5').fetchall()
    
    # Chart data: Monthly bookings
    monthly_bookings = db.execute('''
        SELECT strftime('%Y-%m', date) as month, COUNT(*) as count
        FROM customers c JOIN events e ON c.event_id = e.id
        WHERE c.status = 'Confirmed'
        GROUP BY month
        ORDER BY month
    ''').fetchall()
    monthly_labels = [row['month'] for row in monthly_bookings]
    monthly_data = [row['count'] for row in monthly_bookings]
    
    # Revenue trend
    revenue_trend = db.execute('''
        SELECT strftime('%Y-%m', date) as month, SUM(expected_guests * ticket_price) as revenue
        FROM events
        GROUP BY month
        ORDER BY month
    ''').fetchall()
    revenue_labels = [row['month'] for row in revenue_trend]
    revenue_data = [row['revenue'] for row in revenue_trend]
    
    return render_template('dashboard.html', 
                           total_events=total_events, 
                           total_revenue=total_revenue, 
                           total_bookings=total_bookings, 
                           total_customers=total_customers,
                           recent_events=recent_events,
                           monthly_labels=json.dumps(monthly_labels),
                           monthly_data=json.dumps(monthly_data),
                           revenue_labels=json.dumps(revenue_labels),
                           revenue_data=json.dumps(revenue_data))

@app.route('/events')
def events():
    db = get_db()
    events_list = db.execute('SELECT * FROM events').fetchall()
    events_with_calcs = []
    for event in events_list:
        cost = get_event_cost(event['id'])
        revenue = get_event_revenue(event['id'])
        profit = revenue - cost
        events_with_calcs.append({
            'id': event['id'],
            'name': event['name'],
            'type': event['type'],
            'date': event['date'],
            'location': event['location'],
            'budget': event['budget'],
            'expected_guests': event['expected_guests'],
            'ticket_price': event['ticket_price'],
            'total_cost': cost,
            'revenue': revenue,
            'profit': profit
        })
    return render_template('events.html', events=events_with_calcs)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        date = request.form['date']
        location = request.form['location']
        budget = float(request.form['budget'])
        expected_guests = int(request.form['expected_guests'])
        ticket_price = float(request.form.get('ticket_price', 0))
        
        db = get_db()
        db.execute('INSERT INTO events (name, type, date, location, budget, expected_guests, ticket_price) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (name, type_, date, location, budget, expected_guests, ticket_price))
        db.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('events'))
    return render_template('add_event.html')

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    db = get_db()
    event = db.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        date = request.form['date']
        location = request.form['location']
        budget = float(request.form['budget'])
        expected_guests = int(request.form['expected_guests'])
        ticket_price = float(request.form.get('ticket_price', 0))
        
        db.execute('UPDATE events SET name=?, type=?, date=?, location=?, budget=?, expected_guests=?, ticket_price=? WHERE id=?',
                   (name, type_, date, location, budget, expected_guests, ticket_price, event_id))
        db.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events'))
    return render_template('edit_event.html', event=event)

@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    db = get_db()
    db.execute('DELETE FROM events WHERE id = ?', (event_id,))
    db.commit()
    flash('Event deleted successfully!', 'danger')
    return redirect(url_for('events'))

@app.route('/customers')
def customers():
    db = get_db()
    customers = db.execute('SELECT c.*, e.name as event_name FROM customers c LEFT JOIN events e ON c.event_id = e.id').fetchall()
    events = db.execute('SELECT id, name FROM events').fetchall()
    return render_template('customers.html', customers=customers, events=events)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        event_id = request.form.get('event_id')
        status = request.form['status']
        
        db = get_db()
        db.execute('INSERT INTO customers (name, contact, event_id, status) VALUES (?, ?, ?, ?)',
                   (name, contact, event_id, status))
        db.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    db = get_db()
    events = db.execute('SELECT id, name FROM events').fetchall()
    return render_template('add_customer.html', events=events)

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    db = get_db()
    customer = db.execute('SELECT * FROM customers WHERE id = ?', (customer_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        event_id = request.form.get('event_id')
        status = request.form['status']
        
        db.execute('UPDATE customers SET name=?, contact=?, event_id=?, status=? WHERE id=?',
                   (name, contact, event_id, status, customer_id))
        db.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers'))
    events = db.execute('SELECT id, name FROM events').fetchall()
    return render_template('edit_customer.html', customer=customer, events=events)

@app.route('/delete_customer/<int:customer_id>')
def delete_customer(customer_id):
    db = get_db()
    db.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    db.commit()
    flash('Customer deleted successfully!', 'danger')
    return redirect(url_for('customers'))

@app.route('/vendors')
def vendors():
    db = get_db()
    vendors = db.execute('SELECT v.*, e.name as event_name FROM vendors v LEFT JOIN events e ON v.event_id = e.id').fetchall()
    events = db.execute('SELECT id, name FROM events').fetchall()
    return render_template('vendors.html', vendors=vendors, events=events)

@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        name = request.form['name']
        service_type = request.form['service_type']
        cost = float(request.form['cost'])
        event_id = request.form.get('event_id')
        
        db = get_db()
        db.execute('INSERT INTO vendors (name, service_type, cost, event_id) VALUES (?, ?, ?, ?)',
                   (name, service_type, cost, event_id))
        db.commit()
        flash('Vendor added successfully!', 'success')
        return redirect(url_for('vendors'))
    db = get_db()
    events = db.execute('SELECT id, name FROM events').fetchall()
    return render_template('add_vendor.html', events=events)

@app.route('/edit_vendor/<int:vendor_id>', methods=['GET', 'POST'])
def edit_vendor(vendor_id):
    db = get_db()
    vendor = db.execute('SELECT * FROM vendors WHERE id = ?', (vendor_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        service_type = request.form['service_type']
        cost = float(request.form['cost'])
        event_id = request.form.get('event_id')
        
        db.execute('UPDATE vendors SET name=?, service_type=?, cost=?, event_id=? WHERE id=?',
                   (name, service_type, cost, event_id, vendor_id))
        db.commit()
        flash('Vendor updated successfully!', 'success')
        return redirect(url_for('vendors'))
    events = db.execute('SELECT id, name FROM events').fetchall()
    return render_template('edit_vendor.html', vendor=vendor, events=events)

@app.route('/delete_vendor/<int:vendor_id>')
def delete_vendor(vendor_id):
    db = get_db()
    db.execute('DELETE FROM vendors WHERE id = ?', (vendor_id,))
    db.commit()
    flash('Vendor deleted successfully!', 'danger')
    return redirect(url_for('vendors'))

@app.route('/analytics')
def analytics():
    db = get_db()
    
    # Most profitable event
    events = db.execute('SELECT id, name FROM events').fetchall()
    profits = [(e['name'], get_event_profit(e['id'])) for e in events]
    most_profitable = max(profits, key=lambda x: x[1]) if profits else ('None', 0)
    
    # Highest cost event
    costs = [(e['name'], get_event_cost(e['id'])) for e in events]
    highest_cost = max(costs, key=lambda x: x[1]) if costs else ('None', 0)
    
    # Revenue distribution by event type
    revenue_by_type = db.execute('''
        SELECT type, SUM(expected_guests * ticket_price) as revenue
        FROM events
        GROUP BY type
    ''').fetchall()
    type_labels = [row['type'] for row in revenue_by_type]
    type_data = [row['revenue'] for row in revenue_by_type]
    
    # Event type popularity
    popularity = db.execute('SELECT type, COUNT(*) as count FROM events GROUP BY type').fetchall()
    pop_labels = [row['type'] for row in popularity]
    pop_data = [row['count'] for row in popularity]
    
    return render_template('analytics.html', 
                           most_profitable=most_profitable,
                           highest_cost=highest_cost,
                           type_labels=json.dumps(type_labels),
                           type_data=json.dumps(type_data),
                           pop_labels=json.dumps(pop_labels),
                           pop_data=json.dumps(pop_data))

if __name__ == '__main__':
    app.run(debug=True)