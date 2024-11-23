from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app import teams
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

# List of all historical MLB teams

# Generating the choices with an identifier format 'optionX'
team_choices = [(f'option{i+1}', team) for i, team in enumerate(teams.teams)]

class TeamForm(FlaskForm):
    username = SelectField('Username', choices=team_choices)
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):

    password = StringField('Year', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')