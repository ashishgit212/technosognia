import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# Set your secret key here or load from .env
app.secret_key = os.getenv('SECRET_KEY', '25e3e41d239579f89d46c81918397f7ebdd11e775aa9ccda')

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

# --- AUTHENTICATION ROUTES ---
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Add your registration DB insert logic here
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add your login validation logic here
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# --- PROTECTED ROUTES ---
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    total = len(employees)
    conn.close()
    return render_template('index.html', employees=employees, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        dept = request.form['department']
        email = request.form['email']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        # Ensure your table columns match this query exactly
        cursor.execute("INSERT INTO employees (name, department, email) VALUES (%s, %s, %s)", 
                       (name, dept, email))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/search', methods=['GET', 'POST'])
def search_student():
    if not session.get('logged_in'): return redirect(url_for('login'))
    results = []
    if request.method == 'POST':
        query = request.form['query'].strip()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Use OR to match either the first name part or the last name part
        # This assumes your 'name' column contains both first and last names
        sql = "SELECT * FROM employees WHERE name LIKE %s OR name LIKE %s"
        # Search for names starting with the query (first name) 
        # or containing a space followed by the query (last name)
        params = (f"{query}%", f"% {query}%")
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
    return render_template('search_student.html', results=results)

@app.route('/reports')
def reports():
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT department, COUNT(*) as count FROM employees GROUP BY department")
    report_data = cursor.fetchall()
    conn.close()
    return render_template('reports.html', report_data=report_data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)