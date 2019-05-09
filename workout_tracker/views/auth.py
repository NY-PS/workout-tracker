from flask import (
    Blueprint, current_app, flash, redirect, render_template,
    request, url_for
)
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user

from workout_tracker import LOGIN_MANAGER
from workout_tracker.database import Database
from workout_tracker.forms.login import LoginForm
from workout_tracker.forms.register import RegistrationForm
from workout_tracker.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    user = User.get(int(user_id))

    if user is not None:
        return User(user.id, user.user_name, user.pswd, user.user_role)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        pw_hash = Bcrypt(current_app).generate_password_hash(
            form.password.data
        ).decode('utf-8')

        with Database() as conn:
            query = """
            SELECT COUNT(*) user_count
            FROM user_data
            WHERE user_name = :username OR email = :email"""

            user_count = conn.query(query, username=form.username.data,
                                    email=form.email.data).first().user_count

            print(user_count)

            if user_count > 0:
                flash('This username/email is already taken.', 'danger')
            else:
                query = """
                INSERT INTO user_data (user_name, fname, lname, email, pswd,
                                       user_role, city, state) VALUES
                            (:username, :fname, :lname, :email, :pw_hash,
                             :user_role, :city, :state)"""

                conn.query(query, username=form.username.data,
                           fname=form.fname.data, lname=form.lname.data,
                           email=form.email.data,
                           user_role='user',
                           city=form.city.data, state=form.state.data,
                           pw_hash=pw_hash)

                flash(('Your account has been created! Please log in '
                       'with your credentials to continue.'), 'success')
                return redirect(url_for('auth.login'))
    else:
        print(form.errors)

    return render_template('register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        with Database() as conn:
            query = ('SELECT id, user_name, pswd, user_role '
                     'FROM user_data '
                     'WHERE user_name = :username')

            user_record = conn.query(
                query, username=form.username.data
            ).first()

        if user_record:
            user = User(user_id=user_record.id,
                        username=user_record.user_name,
                        pw_hash=user_record.pswd,
                        role=user_record.user_role)

            is_valid_pw = Bcrypt(current_app).check_password_hash(
                user.pw_hash, form.password.data
            )

            if user and is_valid_pw:
                login_user(user, remember=form.remember.data)

                # redirect to next page after login
                next_page = request.args.get('next')
                next_page = next_page if next_page else url_for('index')

                return redirect(next_page)
            else:
                flash('Incorrect username or password.', 'danger')
        else:
            flash('Incorrect username or password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')

    return redirect(url_for('auth.login'))
