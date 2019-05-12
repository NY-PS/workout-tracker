from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required
from flask import (
    Blueprint, flash, render_template, request, jsonify, current_app
)

from workout_tracker.database import Database
from workout_tracker.forms.user import UserForm, get_user_roles

bp = Blueprint('admin', __name__, url_prefix='/admin')


def get_users():
    query = """
    SELECT id, user_name, fname, lname, email, user_role, city, state
      FROM user_data"""

    with Database() as conn:
        return conn.query(query).all()


def get_user(user_id):
    query = """
    SELECT user_name, fname, lname, email, user_role, city, state
      FROM user_data
     WHERE id = :user_id"""

    with Database() as conn:
        return conn.query(
            query, user_id=user_id
        ).first()


def create_user(username, fname, lname, email, pw_hash,
                user_role, city, state):
    query = """
    INSERT INTO user_data (user_name, fname, lname, email, pswd,
                           user_role, city, state) VALUES
                (:username, :fname, :lname, :email, :pw_hash,
                 :user_role, :city, :state)"""

    user_role = next(
        i.user_role for i in get_user_roles() if i.row_number == user_role
    )

    with Database() as conn:
        conn.query(
            query, username=username, fname=fname, lname=lname,
            email=email, pw_hash=pw_hash, user_role=user_role,
            city=city, state=state
        )

    return True


def update_user(user_id, username, fname, lname, email, pw_hash,
                user_role, city, state):
    query = """
    UPDATE user_data
       SET user_name = :username, fname = :fname, lname = :lname,
           email = :email, pswd = :pw_hash, user_role = :user_role,
           city = :city, state = :state
     WHERE id = :user_id"""

    with Database() as conn:
        conn.query(
            query, username=username, fname=fname, lname=lname,
            email=email, pw_hash=pw_hash, user_role=user_role,
            city=city, state=state, user_id=user_id
        )

    return True


def delete_user(user_id):
    query = """DELETE FROM user_data WHERE id = :user_id"""

    with Database() as conn:
        conn.query(query, user_id=user_id)

    return True


@bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    form = UserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            pw_hash = Bcrypt(current_app).generate_password_hash(
                form.password.data
            ).decode('utf-8')

            create_user(username=form.username.data,
                        fname=form.fname.data,
                        lname=form.lname.data,
                        email=form.email.data,
                        pw_hash=pw_hash,
                        user_role=form.user_role.data,
                        city=form.city.data,
                        state=form.state.data)
        else:
            flash('\n'.join(form.errors), 'danger')

    return render_template('users.html', title='Manage Users',
                           users=get_users(), form=form)


@bp.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def user_details(user_id):
    if request.method == 'DELETE':
        status = 200 if delete_user(user_id) else 500
        return jsonify({'status': status})
    elif request.method == 'PUT':
        pw_hash = Bcrypt(current_app).generate_password_hash(
            request.form['password']
        ).decode('utf-8')

        status = 200 if update_user(
            user_id, request.form['username'], request.form['fname'],
            request.form['lname'], request.form['email'], pw_hash,
            request.form['user_role'], request.form['city'],
            request.form['state']
        ) else 500

        return jsonify({'status': status})
    else:
        user_record = get_user(user_id)

        if not user_record:
            flash(f'User with id "{user_id}" does not exist.', 'danger')

        return render_template('user-details.html', title='User Details',
                               user=user_record, user_id=user_id)
