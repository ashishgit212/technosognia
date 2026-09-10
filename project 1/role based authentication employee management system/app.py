from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'legal_contract_secure_secret_key'

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='mysql123',
        database='legal_contract_db'
    )

# Helper function to record audit logs anywhere in your app
def log_audit(username, action_type, details):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_logs (username, action_type, details) VALUES (%s, %s, %s)",
            (username, action_type, details)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Audit log error: {e}")

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        log_audit(user['username'], 'LOGIN', f"User {user['username']} logged into the system.")
        return redirect(url_for('dashboard'))
    return "Invalid credentials, <a href='/'>try again</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            conn.commit()
            log_audit(username, 'USER_REGISTERED', f"New user account created for {username} with role {role}")
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            cursor.close()
            conn.close()
            return f"Registration Error: {e} <a href='/register'>Try again</a>"
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        log_audit(session['username'], 'LOGOUT', f"User {session['username']} logged out of the system.")
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if session['role'] == 'admin':
        cursor.execute("SELECT * FROM contracts ORDER BY id DESC")
        contracts = cursor.fetchall()
        
        cursor.execute("SELECT * FROM modification_requests ORDER BY id DESC")
        requests_list = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return render_template('admin_dashboard.html', contracts=contracts, requests_list=requests_list)
    else:
        cursor.execute("SELECT * FROM contracts WHERE created_by = %s ORDER BY id DESC", (session['username'],))
        contracts = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return render_template('user_dashboard.html', contracts=contracts)

@app.route('/create_contract', methods=['GET', 'POST'])
def create_contract():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_by = session['username']
        status = 'APPROVED' if session['role'] == 'admin' else 'PENDING'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contracts (title, content, created_by, status) VALUES (%s, %s, %s, %s)", 
                       (title, content, created_by, status))
        conn.commit()
        log_audit(created_by, 'CONTRACT_CREATED', f"Created contract '{title}' (Status: {status})")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    return render_template('create_contract.html')

@app.route('/review_contract/<int:contract_id>', methods=['GET', 'POST'])
def review_contract(contract_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        action = request.form['action']
        approver_comment = request.form.get('approver_comment')
        rejection_reason = request.form.get('rejection_reason') if action == 'REJECT' else None
        new_status = 'APPROVED' if action == 'APPROVE' else 'REJECTED'
        
        cursor.execute("""
            UPDATE contracts 
            SET status = %s, approver_comment = %s, rejection_reason = %s 
            WHERE id = %s
        """, (new_status, approver_comment, rejection_reason, contract_id))
        conn.commit()
        log_audit(session['username'], 'CONTRACT_REVIEW', f"Contract #{contract_id} review decision: {new_status}")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM contracts WHERE id = %s", (contract_id,))
    contract = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('review_contract.html', contract=contract)

@app.route('/request_modification/<int:contract_id>', methods=['GET', 'POST'])
def request_modification(contract_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contracts WHERE id = %s", (contract_id,))
    contract = cursor.fetchone()
    
    if request.method == 'POST':
        clause_title = request.form.get('clause_title')
        request_type = request.form['request_type']
        original_value = request.form.get('original_value')
        proposed_modification = request.form['proposed_modification']
        reason = request.form['reason']
        requested_by = session['username']
        
        cursor.execute("""
            INSERT INTO modification_requests 
            (contract_id, contract_title, clause_title, request_type, original_value, proposed_modification, reason, requested_by) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (contract_id, contract['title'], clause_title, request_type, original_value, proposed_modification, reason, requested_by))
        conn.commit()
        log_audit(requested_by, 'MODIFICATION_REQUESTED', f"Requested modification for contract #{contract_id} ({contract['title']})")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.close()
    conn.close()
    return render_template('request_modification.html', contract=contract)

@app.route('/approver_dashboard')
def approver_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM modification_requests ORDER BY id DESC")
    requests_list = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('approver_dashboard.html', requests_list=requests_list)

@app.route('/review_modification/<int:req_id>', methods=['GET', 'POST'])
def review_modification_request(req_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        action = request.form['action']
        approver_comment = request.form.get('approver_comment')
        rejection_reason = request.form.get('rejection_reason') if action == 'REJECT' else None
        new_status = 'APPROVED' if action == 'APPROVE' else 'REJECTED'
        
        cursor.execute("""
            UPDATE modification_requests 
            SET status = %s, approver_comment = %s, rejection_reason = %s 
            WHERE id = %s
        """, (new_status, approver_comment, rejection_reason, req_id))
        conn.commit()
        log_audit(session['username'], 'MODIFICATION_REVIEW', f"Modification request #{req_id} review decision: {new_status}")
        cursor.close()
        conn.close()
        return redirect(url_for('approver_dashboard'))
        
    cursor.execute("SELECT * FROM modification_requests WHERE id = %s", (req_id,))
    req = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('review_modification.html', req=req)

@app.route('/audit_log')
def audit_log():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT timestamp, username, action_type, details FROM audit_logs ORDER BY id DESC")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('audit_log.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)