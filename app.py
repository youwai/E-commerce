from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home', methods = ['POST'])
def home():
    if request.method == 'POST':
        member_id = request.form['member_id']

        return render_template('main.html', member_id = member_id)