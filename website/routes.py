from website import app
from flask import render_template, url_for, flash, request, redirect
from website.models import BlogPost, ContactForm, LoginForm, RegistrationForm, User, CreatePostForm, CommentForm, Comment, Check
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import  login_user, logout_user, current_user, login_required
from flask_gravatar import Gravatar
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)






@app. route('/')
def home():
    all_post = BlogPost.query.all()

    return render_template('home.html', user = current_user, posts = all_post)

@app. route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        all_post = BlogPost.query.limit(3).all()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Login Successfully", category='success')
                return render_template('home.html', user = current_user, posts = all_post)
            else:
                flash("Incorrect password", category='error')
        else:
            flash('Email ID does not exists, Please register yourself.', category='error')
    return render_template('login.html', form = form, user = current_user)

@app. route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data,method='pbkdf2:sha256', salt_length=8)
        user = User.query.filter_by(email = email).first()
        all_post = BlogPost.query.limit(3).all()
        if user:
            flash("Email ID already exists, please login.", category='error')
        else:
            new_user = User(username = name, email = email, password = password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registered successfully", category='success')
            login_user(new_user, remember=True)
            return render_template('home.html', user = current_user, posts = all_post)
    return render_template('register.html', form = form, user = current_user)

@app. route('/contact', methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        comment = form.comment.data
        flash('Thanks for contact! We will reach out to you shortly.', category='success')
    return render_template('contact.html', form = form, user = current_user)

@app. route('/post', methods=["GET", "POST"])
def post():
    all_post = BlogPost.query.all()
    return render_template('post.html', posts = all_post, user = current_user)

@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        author_name = form.author_name.data
        date = form.date.data
        body = form.body.data
        if len(title)==0:
            flash('The title of the blank cannot be blank.', category='error')
        elif len(author_name) == 0:
            flash('The author name cannot be blank.', category='error')
        elif len(body) <50:
            flash('The blog should have more than 50 word.', category='error')
        else:
            new_blog = BlogPost(author=current_user, author_name = author_name, title = title, date = date, body = body)
            db.session.add(new_blog)
            db.session.commit()
            flash("Your blog is posted, Thanks for writing the blog." , category='success')
            return redirect('/post')
        return render_template("new_post.html", form=form, user = current_user)
    return render_template("new_post.html", form=form, user = current_user)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to register for comment.")
            return redirect(url_for("login"))
        new_comment = Comment(text=form.comment_text.data,comment_author=current_user,parent_post=requested_post)
        db.session.add(new_comment)
        db.session.commit()
        return render_template("post_read.html", post=requested_post, user = current_user, form = form)

    return render_template("post_read.html", post=requested_post, user = current_user, form = form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')





