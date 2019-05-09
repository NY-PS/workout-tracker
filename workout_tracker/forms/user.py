from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import (
    DataRequired, Length, Email
)

from workout_tracker.database import Database


def get_user_roles():
    with Database() as conn:
        query = """
        SELECT row_number() over() row_number,
               e.enumlabel user_role
        FROM pg_type t
          JOIN pg_enum e ON t.oid = e.enumtypid
          JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
        WHERE n.nspname = 'public' AND t.typname = 'role'
        ORDER BY 1"""

        return conn.query(query).all()


class UserForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=3, max=16)]
    )
    fname = StringField('First Name', validators=[])
    lname = StringField('Last Name', validators=[])
    email = StringField('Email Address', validators=[Email()])
    user_role = SelectField(
        'Role', validators=[], choices=get_user_roles(), coerce=int,
        default=next(v[0] for v in get_user_roles() if v[1] == 'user')
    )
    city = StringField('City')
    state = StringField('State')
    submit = SubmitField('Sign Up')
