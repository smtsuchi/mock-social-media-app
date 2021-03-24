from . import bp as posts
from flask import request, redirect, url_for,jsonify, render_template, flash
from app import db
from flask_login import login_required, current_user
from .forms import PostForm
from app.models import Post, Comment, Post_Comment
from app.auth import token_auth


@posts.route('/all', methods=['GET'])
def showposts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@posts.route('/popular', methods=['GET'])
def showpostsbypopularity():
    posts = Post.query.order_by(Post.upvote_count.desc(), Post.downvote_count, Post.date_created.desc()).all()
    return jsonify([p.to_dict() for p in posts])

@posts.route('/unpopular', methods=['GET'])
def showpostsbyunpopularity():
    posts = Post.query.order_by(Post.downvote_count.desc(), Post.upvote_count, Post.date_created.desc()).all()
    return jsonify([p.to_dict() for p in posts])

@posts.route('/all/<int:id>', methods=['GET'])
def post(id):
    post = Post.query.get_or_404(id)

    comments_by_post = Post_Comment.query.filter_by(post_id=id).all()
    for id in comments_by_post:
        comment_content = Comment.query.filter_by(id=id).all()
    return jsonify([c.to_dict() for c in comment_content])

    return jsonify(post.to_dict())

@posts.route('/comments/<int:post_id>')
def comments(post_id):
    post_comments = Post_Comment.query.filter_by(post_id=post_id).all()
    arr = [c.to_dict()['comment_id'] for c in post_comments]
    comments = Comment.query.all()
    return jsonify([c.to_dict() for c in comments if c.id in arr])

    # for num in arr:
    #     comment_detail = Comment.query.filter(id==num).all()

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

@posts.route('/upvote/<int:post_id>', methods=['GET'])
# @token_auth.login_required
def upvote(post_id):
    # data = request.json
    post = Post.query.get_or_404(post_id)
    post.upvote_count += 1
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()['upvote_count'])

@posts.route('/downvote/<int:post_id>', methods=['GET'])
# @token_auth.login_required
def downvote(post_id):
    # data = request.json
    post = Post.query.get_or_404(post_id)
    post.downvote_count += 1
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()['downvote_count'])

@posts.route('/comment/<int:post_id>', methods=['POST'])
@token_auth.login_required
def comment(post_id):
    data = request.json
    print(data)
    user = token_auth.current_user()
    c = Comment(data['content'], user.id, post_id)
    db.session.add(c)
    db.session.commit()
    p_c = Post_Comment(post_id, c.to_dict()['id'])
    db.session.add(p_c)
    db.session.commit()
    return jsonify(c.to_dict())
