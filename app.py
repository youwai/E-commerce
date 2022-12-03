from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

user = ''

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    user = ''
    return render_template('login.html')

@app.route('/home', methods = ['POST'])
def home():
    if request.method == 'POST':
        global user 
        user = request.form['member_id']

        return redirect(url_for('main'))

@app.route('/main')
def main():
    return render_template('main.html', user = user)

@app.route('/history')
def history():
    return render_template('history.html', user = user)