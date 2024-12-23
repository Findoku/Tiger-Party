from flask import Flask
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


app = Flask(__name__)

app.config.from_object(Config)

from app import routes