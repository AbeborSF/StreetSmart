@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if current_user.role not in ['admin', 'moderator']:
        flash('Permission denied!', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_post = Post(title=request.form['title'], content=request.form['content'], author_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html')

@app.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user.role != 'admin':
        flash('Permission denied!', 'danger')
        return redirect(url_for('index'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('index'))
