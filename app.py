from flask import Flask, render_template, request, redirect, url_for
from db import init_db, get_all_logs, save_log, delete_log

app = Flask(__name__)

init_db

@app.route('/')
def index():
    logs = get_all_logs()
    return render_template('index.html', logs=logs)

@app.route('/add', methods=['POST'])
def add():
    context = request.form.get('context')
    if context:
        save_log(context)
    return redirect(url_for('index'))