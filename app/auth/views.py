from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db, login_manager
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, \
  ForgotPasswordForm, ResetPasswordForm, ChangeEmailForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if not current_user.is_anonymous:
    return redirect(url_for('main.index'));
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user, form.remember_me.data)
      next = request.args.get('next')
      if next is None or not next.startswith('/'):
        next = url_for('main.index')
      return redirect(next)
    flash('Invalid username or password.')
  return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been logged out.')
  return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(email=form.email.data, username=form.username.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    token = user.generate_confirmation_token()
    send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
    flash('A confirmation email has been sent')
    return redirect(url_for('auth.login'))
  return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
  if current_user.confirmed:
    return redirect(url_for('main.index'))
  if current_user.confirm(token):
    db.session.commit()
    flash('You have confirmed your account. Thanks!')
  else:
    flash('The confirmation link is invalid or has expired')
  return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
  token = current_user.generate_confirmation_token()
  send_email(current_user.email, 'Confirm Your Account',
              'auth/email/confirm', user=current_user, token=token)
  flash('A new confirmation emails has been sent to you')
  return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
  if current_user.is_authenticated:
    if not current_user.confirmed and request.blueprint != 'auth' \
      and request.endpoint != 'static':
      return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
  if current_user.is_anonymous or current_user.confirmed:
    return redirect(url_for('main.index'))
  return render_template('auth/unconfirmed.html')

@auth.route('/change-password', methods=['Get', 'POST'])
@login_required
def change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    if current_user.verify_password(form.old_password.data):
      current_user.password = form.password.data
      db.session.add(current_user)
      db.session.commit()
      flash('Your password has been updated.')
      return redirect(url_for('main.index'))
    else:
      flash('Invalid password.')
  return render_template('auth/change_password.html', form=form)

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
  if not current_user.is_anonymous:
    return redirect(url_for('main.index'))
  form = ForgotPasswordForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      token = user.generate_reset_token()
      send_email(user.email, 'Password Reset', 'auth/email/reset_password', user=user, token=token)
    flash('An email with instructions to reset your password has been sent to you.')
    return redirect(url_for('main.index'))
  return render_template('auth/forgot_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
  if not current_user.is_anonymous:
    return redirect(url_for('main.index'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    if User.reset_password(token, form.password.data):
      db.session.commit()
      flash('Your password has been updated.')
      return redirect(url_for('auth.login'))
    else:
      flash('Password could not be updated.')
      return redirect(url_for('main.index'))
  return render_template('auth/reset_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email():
  form = ChangeEmailForm()
  if form.validate_on_submit():
    token = current_user.generate_email_change_token(form.email.data)
    send_email(current_user.email, 'Confirm New Email', 'auth/email/update_email', user=current_user, token=token)
    flash('A confirmation email has been sent to your new email address.')
    return redirect(url_for('main.index'))
  return render_template('auth/change_email.html', form=form)

@auth.route('/change-email/<token>')
@login_required
def update_email(token):
  if current_user.change_email(token):
    db.session.commit()
    flash('Your email address has been updated.')
  else:
    flash('Invalid request.')
  return redirect(url_for('main.index'))

