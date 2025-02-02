@app.route('/post/<int:id>', methods=['GET', 'POST'])
def view_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        comment = Comment(content=request.form['comment'], post_id=id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
    comments = Comment.query.filter_by(post_id=id).all()
    return render_template('post.html', post=post, comments=comments)
