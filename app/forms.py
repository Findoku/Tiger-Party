from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app import teams
from app import sqlComs
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

# List of all historical MLB teams

# Generating the choices with an identifier format 'optionX'
team_choices = [(f'option{i+1}', team) for i, team in enumerate(teams.teams)]

class TeamForm(FlaskForm):
    username = SelectField('Username', choices=team_choices)


submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    submit = SubmitField('Submit', render_kw={'class': 'stylish-button'})


class DisplayForm(FlaskForm):
    password = StringField('Year', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    rows = ["asdsa"]
    year_dropdown = SelectField('Select Year', choices=[], validators=[DataRequired()])
    team_dropdown = SelectField('Select team', choices=teams.teams, validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'class': 'stylish-button'})


