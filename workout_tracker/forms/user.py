class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=3, max=16)]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')]
    )
    fname = StringField('First Name', validators=[])
    lname = StringField('Last Name', validators=[])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    user_role = SelectField(
        'Role', validators=[], choices=get_user_roles(), coerce=int,
        default=next(v[0] for v in get_user_roles() if v[1] == 'user')
    )
    city = StringField('City')
    state = StringField('State')
    submit = SubmitField('Sign Up')
