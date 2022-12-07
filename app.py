from flask import Flask, render_template, request, redirect, url_for
import data

app = Flask(__name__)

user = ''

outcome = None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    global user 
    user = ''

    global outcome
    outcome = None

    return render_template('login.html')

@app.route('/home', methods = ['POST'])
def home():
    if request.method == 'POST':
        global user 
        user = request.form['member_id']

        return redirect(url_for('main'))

@app.route('/main')
def main():
    global outcome
    
    if outcome is None:
        items = data.pass_recommendation(user)

        print(items)

        outcome = items.to_dict('records')

    return render_template('main.html', user = user, outcome = outcome)

@app.route('/history')
def history():
    result = data.locate_data(user)

    category_count = data.category_count(user)

    if result is not None:
        result1 = result.to_dict('series')
        amount = len(result1['Order Code'])
    else:
        result1 = '-'
        amount = 0

    return render_template('history.html', user = user, result = result1, amount = amount, category_count = category_count)