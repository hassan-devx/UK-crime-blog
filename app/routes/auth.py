from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app.models import User
from app import db

from app.forms import RegisterForm
from app.forms import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("That username is already taken. Please choose another.")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. You can now log in.")
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.username}!")  # ✅ Now inside request context
            return redirect(url_for('home.dashboard'))

        flash("Invalid credentials. Please try again.")

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


