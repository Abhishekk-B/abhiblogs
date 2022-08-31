from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from website import db
from flask_login import UserMixin
from flask_ckeditor import CKEditorField
from datetime import date
from sqlalchemy.orm import relationship





class LoginForm(FlaskForm):
    email = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    password = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=5, max=100)])
    login = SubmitField(label='Login')

class RegistrationForm(FlaskForm):
    name = StringField(label= 'Enter Your Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    password = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=5, max=100)])
    register = SubmitField(label='Sign UP')

class ContactForm(FlaskForm):
    name = StringField(label= 'Enter Your Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    comment = TextAreaField(label = 'Enter Your Comments', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField(label='Submit')


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = relationship("BlogPost", back_populates = 'author')
    comments =  relationship("Comment", back_populates = 'comment_author')


class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String, unique=True, nullable=False)
    author_name = db.Column(db.String, nullable=False)
    author = relationship("User", back_populates = "posts")
    date = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    comments = relationship("Comment", back_populates = 'parent_post')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_post.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text = db.Column(db.Text, nullable=False)

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()], description='10 January, 2022', default=date.today().strftime("%d %B, %Y"))
    author_name = StringField("Your Name", validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


class Check(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


db.create_all()





