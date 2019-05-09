from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired, Length, EqualTo, ValidationError, Email
)

from workout_tracker.database import Database


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=3, max=16)]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')]
    )
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        with Database() as conn:
            query = ('SELECT user_name '
                     'FROM user_data '
                     'WHERE user_name = :username')
            user = conn.query(query, username=username.data).first()

        if user is not None:
            raise ValidationError('Oops! Someone already has that username.')
