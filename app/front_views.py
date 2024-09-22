from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Escrow  # Ensure Escrow model is imported

front_bp = Blueprint('front', __name__)


@front_bp.route('/')
def index():
    return redirect(url_for('front.home'))


@front_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("用户已经登录，重定向到首页")
        return redirect(url_for('front.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('用户名或密码不正确')
            return redirect(url_for('front.login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('front.home'))

    return render_template('front/login.html', form=form)


@front_bp.route('/home')
@login_required
def home():
    escrows = Escrow.query.all()
    return render_template('front/home.html', escrows=escrows)


@front_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录。')
        return redirect(url_for('front.login'))
    return render_template('front/register.html', form=form)


@front_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('front.login'))