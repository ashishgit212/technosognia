# app.py
import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'a9f39fcdd7a87b8c750f94b6d329d66dae3a4d3ce5f484750f99f5f8e3187dea')

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'employee_db'),
        cursorclass=pymysql.cursors.DictCursor
    )

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in first.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'Admin':
            flash('Access denied. Administrator rights required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE email = %s", (email,))
            user = cursor.fetchone()
        connection.close()
        
        if user and user['password'] == password:
            session['user'] = user['name']
            session['role'] = user.get('role', 'Employee')
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        department = request.form.get('department')
        email = request.form.get('email')
        password = request.form.get('password')
        status = request.form.get('status', 'Active')
        role = request.form.get('role', 'Employee')
        
        if role == 'Admin':
                    admin_secret = request.form.get('admin_secret')
                    if admin_secret != 'a9f39fcdd7a87b8c750f94b6d329d66dae3a4d3ce5f484750f99f5f8e3187dea':
                        flash('Invalid Admin Secret Key!', 'danger')
                        return redirect(url_for('register'))

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('Email already registered. Please login.', 'warning')
                connection.close()
                return redirect(url_for('login'))
                
            sql = "INSERT INTO employees (name, department, email, password, status, role) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, department, email, password, status, role))
            connection.commit()
        connection.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    search = request.args.get('search', '')
    status = request.args.get('status', 'All')
    sort = request.args.get('sort', 'name')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        query_base = "FROM employees WHERE 1=1"
        params = []
        
        if search:
            query_base += " AND (name LIKE %s OR department LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])
            
        if status != 'All':
            query_base += " AND status = %s"
            params.append(status)
            
        cursor.execute(f"SELECT COUNT(*) AS total {query_base}", tuple(params))
        total_employees = cursor.fetchone()['total']
        
        sort_column = "created_at" if sort == "created_at" else "name"
        
        fetch_query = f"SELECT * {query_base} ORDER BY {sort_column} ASC LIMIT %s OFFSET %s"
        cursor.execute(fetch_query, tuple(params) + (per_page, offset))
        employees = cursor.fetchall()
        
    connection.close()
    
    total_pages = (total_employees + per_page - 1) // per_page
    
    return render_template('index.html', 
                           employees=employees, 
                           page=page, 
                           total_pages=total_pages,
                           search=search,
                           status=status,
                           sort=sort)

@app.route('/reports')
@login_required
def reports():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total_employees FROM employees")
        emp_count = cursor.fetchone()['total_employees']
        
        cursor.execute("SELECT COUNT(*) AS active_employees FROM employees WHERE status = 'Active'")
        active_count = cursor.fetchone()['active_employees']
    connection.close()
    
    report_data = {
        "active_employees": active_count,
        "inactive_employees": emp_count - active_count
    }
    return render_template('reports.html', report_data=report_data)

@app.route('/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        department = request.form.get('department')
        email = request.form.get('email')
        password = request.form.get('password', '123456')
        status = request.form.get('status')
        role = request.form.get('role', 'Employee')
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO employees (name, department, email, password, status, role) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, department, email, password, status, role))
            connection.commit()
        connection.close()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('add_employee.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        if request.method == 'POST':
            name = request.form.get('name')
            department = request.form.get('department')
            email = request.form.get('email')
            status = request.form.get('status')
            role = request.form.get('role')
            
            sql = "UPDATE employees SET name=%s, department=%s, email=%s, status=%s, role=%s WHERE id=%s"
            cursor.execute(sql, (name, department, email, status, role, id))
            connection.commit()
            connection.close()
            flash('Employee updated successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
        employee = cursor.fetchone()
    connection.close()
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
        connection.commit()
    connection.close()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)