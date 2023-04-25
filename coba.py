from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Set secret key for session
app.secret_key = 'secret_key_for_session'

# Database of doctors
doctors = {
    'doctor1': {'username': 'doctor1', 'password': 'password1', 'name': 'Doctor 1', 'verified': False},
    'doctor2': {'username': 'doctor2', 'password': 'password2', 'name': 'Doctor 2', 'verified': True},
    'doctor3': {'username': 'doctor3', 'password': 'password3', 'name': 'Doctor 3', 'verified': False},
}

@app.route('/')
def index():
    # Check if user is logged in
    if 'username' in session:
        return redirect(url_for('profile'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in doctors and password == doctors[username]['password']:
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    # Check if user is logged in
    if 'username' in session:
        username = session['username']
        doctor = doctors[username]
        return render_template('profile.html', doctor=doctor)
    return redirect(url_for('login'))

@app.route('/verify')
def verify():
    # Check if user is logged in
    if 'username' in session:
        username = session['username']
        doctor = doctors[username]
        if not doctor['verified']:
            doctor['verified'] = True
            return render_template('verify.html', doctor=doctor)
        else:
            return redirect(url_for('profile'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
