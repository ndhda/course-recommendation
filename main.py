from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from topsis import rank_courses

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Load the dataset
df = pd.read_csv('data/coursera_courses.csv')

users = {}  # Simple user storage

@app.route('/')
def home():
    logged_in = 'user' in session
    return render_template('home.html', logged_in=logged_in)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/mcdm-detail')
def mcdm_detail():
    return render_template('mcdm-detail.html')

@app.route('/topsis-detail')
def topsis_detail():
    return render_template('topsis-detail.html')

@app.route('/results', methods=['POST'])
def results():
    if 'user' in session:
        course_difficulty = request.form['course_difficulty']
        course_time = request.form['course_time']
        course_type = request.form['course_type']

        recommendations = rank_courses(df, course_difficulty, course_time, course_type)

        if recommendations.empty:
            flash('No courses found matching your criteria.', 'error')
            return redirect(url_for('no_courses_found'))

        return render_template('results.html', courses=recommendations)
    else:
        flash('Please login or sign up to use this feature.', 'error')
        return redirect(url_for('login'))

@app.route('/no_courses_found')
def no_courses_found():
    return render_template('error.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, please try again.', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists, please choose another one.', 'error')
        else:
            users[username] = password
            session['user'] = username
            flash('Sign up successful!', 'success')
            return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
