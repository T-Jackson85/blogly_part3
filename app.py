"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Users, Post, Tag 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:aniya123///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
db.create_all()

@app.route("/")
def home():
    """Homepage shows list of all users"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return redirect("homepage.html", posts= posts)

@app.route('/users')
def user_list():
    """Shows user info"""

    users= Users.query.order_by(Users.last_name, Users.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():

    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def new_users():

    new_user= Users(
        first_name= request.form['first_name'],
        last_name= request.form['last_name'],
        image_url= request.form['image-url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:users_id>')
def show_user(users_id):

    users = Users.query.get_or_404(users_id)
    return render_template('users/show.html', users=users)

@app.route('/users/<int:users_id>/edit', methods=["POST"])
def users_update(users_id):

    user = Users.query.get_or_404(users_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:users_id>/posts/new')
def new_post_form(users_id):

    users = Users.query.get_or_404(users_id)
    tags = Tag.query.all()
    return render_template('newpost.html', users= users, tags=tags)

@app.route('/users/<int:users_id>/posts/new', methods=['POST'])
def new_post(users_id):

    users = Users.query.get_or_404(users_id)
    tag_id = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_id)).all()


    new_post = Post(title = request.form['content'],users =users, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{users_id}")

@app.route('/posts/<int:posts_id>')
def show_post(posts_id):
    
    post = Post.query.get_or_404(posts_id)
    return render_template('showpost.html', post= post)

@app.route('/posts/<int:posts_id>/edit')
def edit_post(posts_id):

    post = Post.query.get_or_404(posts_id)
    tags = Tag.query.all()
    return render_template('editpost.html', post=post, tags=tags)

@app.route('/posts/<int:posts_id>/edit', methods=['POST'])
def edited_post(posts_id):

    post = Post.query.get_or_404(posts_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_id = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_id)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.users_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(posts_id):

    post = Post.query.get_or_404(posts_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.users_id}")

@app.route("/tags")
def tags_index():

    tags = Tag.query.all()
    return render_template('tagsIndex.html', tags=tags)


@app.route("/tags/new")
def new_tags_form():

    posts = Post.query.all()
    return render_template('newTags.html', posts=posts)

@app.route('/tags/new', methods='POST')
def tags_new():

    post_id = [int(num for num in request.form.getlist("posts"))]
    posts= Post.query.filter(Post.id.in_(post_id)).all()
    new_tag = Tag(name= request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    return render_template('showTags.html', tag = tag)

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('editTags.html', tag=tag, posts=posts)

@app.route('tags/<int:tag_id>/edit', methods=["POST"])
def edit_tags(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_id = [int(num) for num in request.form.getlist('posts')]
    tag.post = Post.query.filter(Post.id.in_(post_id)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tags(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


if __name__== "__main__":
     app.run(debug=True)
