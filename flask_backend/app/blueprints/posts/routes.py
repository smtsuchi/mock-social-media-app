from . import bp as posts
from flask import request, redirect, url_for,jsonify, render_template, flash
from app import db
from flask_login import login_required, current_user
from .forms import PostForm
from app.models import Post
from app.auth import token_auth


@posts.route('/all', methods=['GET'])
def showposts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@posts.route('/all/<int:id>', methods=['GET'])
def post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())

@posts.route('/create', methods=['POST'])
@token_auth.login_required
def create():
    data = request.json
    user = token_auth.current_user()
    p = Post(data['title'], data['image'], data['content'], user.id)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict())



## Fix he two under here
@posts.route('/myposts/update/<int:post_id>', methods =['GET','POST'])
# @login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    update_form = PostForm()
    if post.author.id != current_user.id:
        flash("You cannot update another user's post", "danger")
        return redirect(url_for('myPosts'))
    if request.method == "POST" and update_form.validate():
        post_title = update_form.title.data
        post_content = update_form.content.data

        post.title = post_title
        post.content = post_content

        db.session.commit()
        flash("Your post has been updated.", "info")
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('post_update.html', form = update_form, post=post)

@posts.route('/myposts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        flash("You cannot update another user's post", "danger")
        return redirect(url_for('myPosts'))
    db.session.delete(post)
    db.session.commit()
    flash("This entry has been deleted", 'info')
    return redirect(url_for('hello_world'))