from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, widgets
from wtforms.validators import InputRequired, Length, URL, Optional

# class PostForm(FlaskForm):
#     """Form for adding/editing posts."""

#     title = StringField('Title', validators=[InputRequired()])

#     description = StringField('Description', validators=[InputRequired()])

#     image_url = StringField('Location Image Link', validators=[InputRequired(),URL(require_tld=True, message=u'Invalid URL.')])

#     lat = FloatField('lat', validators=[InputRequired()])

#     lng = FloatField('lng', validators=[InputRequired()])
    
#     address = StringField('address', validators=[InputRequired()])

#     city = StringField('city', validators=[InputRequired()])

#     state = StringField('state', validators=[InputRequired()])

#     country = StringField('country', validators=[InputRequired()])

#     zipcode = IntegerField('zipcode', validators=[InputRequired()])
    
class PostForm(FlaskForm):
    """Form for adding/editing posts."""

    title = StringField('Title', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    image_url = StringField('Location Image Link', validators=[InputRequired(),URL(require_tld=True, message=u'Invalid URL.')])
    lat = FloatField('Latitute',widget=widgets.HiddenInput(), validators=[InputRequired()])
    lng = FloatField('Longtitude',widget=widgets.HiddenInput(), validators=[InputRequired()])
    address = StringField('Address',widget=widgets.HiddenInput(), validators=[InputRequired()])
    city = StringField('City',widget=widgets.HiddenInput(), validators=[Length(max=200)])
    state = StringField('State',widget=widgets.HiddenInput(), validators=[Length(min=0, max=50)])
    country = StringField('Country',widget=widgets.HiddenInput(), validators=[Length(min=0, max=50)])
    zipcode = IntegerField('Zipcode',widget=widgets.HiddenInput(), validators=[Optional(strip_whitespace=True)])

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
    bio = TextAreaField('Bio')
    password = PasswordField('Password', validators=[Length(min=6)])

class ChangePasswordForm(FlaskForm):
    """Change Password form."""

    password = PasswordField('Current Password', validators=[Length(min=6)])
    new_password = PasswordField('New Password', validators=[Length(min=6)])
    new_password_match = PasswordField('New Password Again', validators=[Length(min=6)])
    
