from app import app, db

if __name__ == '__main__':
    db.create_all()  # Creates database tables
    app.run(debug=True)