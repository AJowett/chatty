from flask import render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import main
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
  return render_template("index.html");

@main.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('user.html', user=user)

@main.route('/chat')
@login_required
def chat():
    return render_template("chat.html")