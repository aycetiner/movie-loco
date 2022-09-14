from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, URL

class PostForm(FlaskForm):
    """Form for adding/editing posts."""

    title = StringField('Title', validators=[InputRequired()])

    description = StringField('Description', validators=[InputRequired()])

    image_url = StringField('Location Image Link', validators=[InputRequired(),URL(require_tld=True, message=u'Invalid URL.')])

    lat = FloatField('lat', validators=[InputRequired()])

    lng = FloatField('lng', validators=[InputRequired()])
    
    address = StringField('address', validators=[InputRequired()])

    city = StringField('city', validators=[InputRequired()])

    state = StringField('state', validators=[InputRequired()])

    country = StringField('country', validators=[InputRequired()])

    zipcode = IntegerField('zipcode', validators=[InputRequired()])
    
 

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class ProfileEditForm(FlaskForm):
    """Form for editing user profile."""

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired()])
    image_url = StringField('(Optional) Profile Image URL')
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    bio = TextAreaField('Bio')
    password = PasswordField('Password', validators=[Length(min=6)])

class ChangePasswordForm(FlaskForm):
    """Change Password form."""

    password = PasswordField('Current Password', validators=[Length(min=6)])
    new_password = PasswordField('New Password', validators=[Length(min=6)])
    new_password_match = PasswordField('New Password Again', validators=[Length(min=6)])
    
