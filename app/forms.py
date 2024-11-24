from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app import teams
from app import sqlComs
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from app import config

# List of all historical MLB teams

# Generating the choices with an identifier format 'optionX'
team_choices = [(f'option{i+1}', team) for i, team in enumerate(teams.teams)]

class TeamForm(FlaskForm):
    team1 = SelectField('Select Team', choices=[], validators=[DataRequired()])
    team2 = SelectField('Select Team', choices=teams.teams, validators=[DataRequired()])
    submit = SubmitField('Submit',render_kw={'class': 'stylish-button'})


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit', render_kw={'class': 'stylish-button'})


class DisplayForm(FlaskForm):

    rows = ["asdsa"]
    year_dropdown = SelectField('Select Year', choices=[], validators=[DataRequired()])
    team_dropdown = SelectField('Select team', choices=teams.teams, validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'class': 'stylish-button'})

