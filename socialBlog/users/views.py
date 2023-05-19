# users/views.py


# register users view
from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_user, current_user, logout_user, login_required

from socialBlog.models import User, BlogPost
from socialBlog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from socialBlog.users.picture_handler import add_profile_pic

from socialBlog import db

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(url_for('core.index'))
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic_file = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
