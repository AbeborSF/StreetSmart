from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post, Comment
from app.email_sms import send_email, send_sms

@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST'):
        author = request.form['author']
        text = request.form['text']
        new_comment = Comment(post_id=post.id, author=author, text=text)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', 'success')
    comments = Comment.query.filter_by(post_id=post.id).all()
    return render_template('post.html', post=post, comments=comments)

@app.route('/crime_insights')
def crime_insights():
    return render_template('crime_insights.html')

@app.route('/posts', methods=['GET'])
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template('posts.html', posts=posts)