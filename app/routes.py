from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.models import User


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('המשתמש כבר קיים')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('ההרשמה הצליחה! התחבר/י כעת')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))

        flash('שם משתמש או סיסמה שגויים')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/lists')
@login_required
def lists():
    return render_template('lists.html')


@app.route('/add-list', methods=['GET', 'POST'])
@login_required
def add_list():
    if request.method == 'POST':
        # כאן תוסיף לוגיקה לשמירת הרשימה בבסיס הנתונים
        flash('הרשימה נוספה בהצלחה!')
        return redirect(url_for('lists'))
    return render_template('add_list.html')


@app.route('/recommendations')
@login_required
def recommendations():
    return render_template('recommendations.html')
