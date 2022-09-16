from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from wb.users.forms import RegistrationForm, LoginForm
from wb.models import Post, User
from wb import database, bcrypt
from flask_login import login_user, current_user, logout_user, login_required




users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberme.data)
            next_page = request.args.get('next')
            try:
                next_page = next_page[1:]
                next_page = f"main.{next_page}"
            except TypeError:
                pass
            flash(f'Logged in as {user.username}', category='success')
            return redirect(url_for(next_page)) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Log in unsuccessful', category='danger')

    return render_template('login.html', form=form)

#
# @users.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username = form.username.data, email = form.email.data, password = hashed_password)
#         database.session.add(user)
#         database.session.commit()
#         flash(f'Account created for {form.username.data}, enjoy the scrumptious account', category='success')
#         return redirect(url_for('users.login'))
#     return render_template('signup.html', form=form)


@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash(f'Logged out', category='success')
    return redirect(url_for('main.home'))

