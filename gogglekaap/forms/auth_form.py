from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    user_id = StringField('User Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class RegisterForm(LoginForm): #상속
    password = PasswordField(
        'Password',
        validators=[DataRequired(), EqualTo(
            'repassword',
            message='Password not match.'
        )]
    )
    repassword = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
    
    user_name = StringField('User Name', validators=[DataRequired()])