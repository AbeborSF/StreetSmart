from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from twilio.rest import Client
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo

app = Flask(_name_)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite DB for simplicity
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Regular')

# Routes and views
@app.route('/')
def home():
    return render_template('index.html')

# User Registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = form.password.data  # Use hashing in a real app
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Account created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

# User Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # Use hashed password comparison
            login_user(user)
            return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Blog Post Management
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if current_user.role != 'Admin' and current_user.role != 'Moderator':
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content, author_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html')

# Commenting System (simplified)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        author = request.form['author']
        text = request.form['text']
        new_comment = Comment(post_id=post.id, author=author, text=text)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', 'success')
    comments = Comment.query.filter_by(post_id=post.id).all()
    return render_template('post.html', post=post, comments=comments)

# Email & SMS Alerts
def send_email(subject, recipient, message):
    msg = Message(subject, recipients=[recipient])
    msg.body = message
    mail.send(msg)

def send_sms(phone_number, message):
    account_sid = 'your_twilio_sid'
    auth_token = 'your_twilio_auth_token'
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_='your_twilio_number', to=phone_number)

# Google Maps Integration (for Crime Insights)
@app.route('/crime_insights')
def crime_insights():
    # This can be expanded with actual crime data and map integration.
    return render_template('crime_insights.html')

# Pagination & Search (for blog posts)
@app.route('/posts', methods=['GET'])
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template('posts.html', posts=posts)

if _name_ == '_main_':
    db.create_all()  # Creates database tables
    app.run(debug=True)