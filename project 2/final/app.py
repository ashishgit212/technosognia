from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
from datetime import datetime, date
import re

app = Flask(__name__)
app.secret_key = 'a9f39fcdd7a87b8c750f94b6d329d66dae3a4d3ce5f484750f99f5f8e3187dea'

# ============== DATABASE CONNECTION ==============
def get_db_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='mysql123',  # 💡 Change to your actual MySQL root password if needed
            database='corp_vault_db'
        )
    except Exception as e:
        print(f"❌ Storage Core Error: {e}")
        raise e

# ============== HELPER FUNCTIONS ==============
def calculate_tenure_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# ============== ROUTES ==============
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/employee_login')
def employee_login():
    return render_template('emlogin.html')

@app.route('/admin_login')
def admin_login():
    return render_template('adlogin.html')

@app.route('/hr_login')
def hr_login():
    return render_template('hrlogin.html')

# ============== REGISTER API ==============
@app.route('/register_employee', methods=['POST'])
def register_employee():
    try:
        full_name = request.form['name']
        mobile_num = request.form['mobile']
        email_addr = request.form['email']
        uname = request.form['username']
        passphrase = request.form['password']
        
        # Validation
        if not re.match(r'^[0-9]{10}$', mobile_num):
            return jsonify({'success': False, 'message': 'Mobile contact must be 10 digits'})
        
        if not re.match(r'^[a-z]+$', uname):
            return jsonify({'success': False, 'message': 'Username must be lowercase letters only'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check duplicate identity
        cursor.execute("SELECT * FROM personnel WHERE username = %s OR email = %s", (uname, email_addr))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Username or Email identity already provisioned'})
        
        # Insert essential credentials in plaintext
        cursor.execute("""INSERT INTO personnel 
                         (full_name, mobile_number, email, username, password, role) 
                         VALUES (%s, %s, %s, %s, %s, %s)""",
                       (full_name, mobile_num, email_addr, uname, passphrase, 'employee'))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Provisioning successful! Access terminal to login.'})
    except Exception as e:
        print(f"❌ Provisioning Error: {e}")
        return jsonify({'success': False, 'message': str(e)})

# ============== LOGIN API ==============
@app.route('/login_employee', methods=['POST'])
def login_employee():
    try:
        uname = request.form['username']
        passphrase = request.form['password']
        user_role = request.form.get('role', 'employee')
        
        print(f"🔍 Access attempt: username={uname}, clearance={user_role}")
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check against plaintext password
        cursor.execute("SELECT * FROM personnel WHERE username = %s AND password = %s AND role = %s", 
                      (uname, passphrase, user_role))
        personnel_rec = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if personnel_rec:
            print(f"✅ Clearance granted: {personnel_rec['full_name']} ({personnel_rec['role']})")
            session['personnel_id'] = personnel_rec['id']
            session['personnel_name'] = personnel_rec['full_name']
            session['personnel_role'] = personnel_rec['role']
            
            if user_role == 'admin':
                return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
            elif user_role == 'hr':
                return jsonify({'success': True, 'redirect': url_for('hr_dashboard')})
            else:
                return jsonify({'success': True, 'redirect': url_for('employee_dashboard')})
        else:
            print(f"❌ Clearance denied: Invalid credentials for {uname}")
            return jsonify({'success': False, 'message': 'Invalid clearance credentials'})
    except Exception as e:
        print(f"❌ Authentication Error: {e}")
        return jsonify({'success': False, 'message': str(e)})

# ============== DASHBOARDS ==============
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'personnel_id' not in session or session.get('personnel_role') != 'admin':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, full_name AS name, mobile_number AS mobile, email, username, role 
        FROM personnel WHERE role != 'admin' ORDER BY id DESC
    """)
    personnel_list = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('addashboard.html', employees=personnel_list)

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'personnel_id' not in session or session.get('personnel_role') != 'employee':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, full_name AS name, mobile_number AS mobile, email, username, role 
        FROM personnel WHERE id = %s
    """, (session['personnel_id'],))
    personnel_rec = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('emdashboard.html', employee=personnel_rec)

@app.route('/hr_dashboard')
def hr_dashboard():
    if 'personnel_id' not in session or session.get('personnel_role') != 'hr':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, full_name AS name, mobile_number AS mobile, email, username, role 
        FROM personnel WHERE role = 'employee' ORDER BY id DESC
    """)
    personnel_list = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('hrdashboard.html', employees=personnel_list)

# ============== OPERATIONS ==============
@app.route('/add_employee', methods=['POST'])
def add_employee():
    if 'personnel_id' not in session or session.get('personnel_role') not in ['admin', 'hr']:
        return jsonify({'success': False, 'message': 'Unauthorized node action'})
    
    try:
        full_name = request.form['name']
        mobile_num = request.form['mobile']
        email_addr = request.form['email']
        uname = request.form['username']
        passphrase = request.form['password']
        user_role = request.form.get('role', 'employee')
        
        if not re.match(r'^[0-9]{10}$', mobile_num):
            return jsonify({'success': False, 'message': 'Mobile contact must be 10 digits'})
        
        if not re.match(r'^[a-z]+$', uname):
            return jsonify({'success': False, 'message': 'Username must be lowercase letters only'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM personnel WHERE username = %s OR email = %s", (uname, email_addr))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Username or Email identity already exists'})
        
        cursor.execute("""INSERT INTO personnel 
                         (full_name, mobile_number, email, username, password, role) 
                         VALUES (%s, %s, %s, %s, %s, %s)""",
                       (full_name, mobile_num, email_addr, uname, passphrase, user_role))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Personnel profile deployed successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_employee/<int:record_id>', methods=['POST'])
def delete_employee(record_id):
    if 'personnel_id' not in session or session.get('personnel_role') not in ['admin', 'hr']:
        return jsonify({'success': False, 'message': 'Unauthorized node action'})
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personnel WHERE id = %s AND role != 'admin'", (record_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Personnel profile terminated successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ============== MAIN ==============
if __name__ == '__main__':
    print("=" * 50)
    print("⚡ NEXUS WORKFORCE OPERATIONS HUB")
    print("=" * 50)
    print("📍 Gateway: http://localhost:5000")
    print("🔑 Admin Clearance: director / masterkey")
    print("🔑 HR Clearance: supervisor / keypass")
    print("🔑 Personnel Access: (provisioned credentials)")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
