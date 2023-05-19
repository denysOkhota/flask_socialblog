# blog_posts/views.py
"""Blog Posts views"""

from flask import render_template, request, redirect, url_for, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required

from socialBlog.blog_posts.forms import BlogPostForm
from socialBlog.models import User, BlogPost
from socialBlog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from socialBlog import db

blog_posts = Blueprint('blog_posts', __name__)


# create blog post
@blog_posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data, body=form.content.data, user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


@blog_posts.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = BlogPostForm()
    post = BlogPost.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.content.data
        db.session.commit()
        return redirect(url_for('blog_posts.update_post', post_id=post.id))
    form.title.data = post.title
    form.content.data = post.body
    return render_template('update_post.html', form=form)


@blog_posts.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('core.index'))


@blog_posts.route('/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', post=post)
