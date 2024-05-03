from flask import Flask, redirect, url_for, render_template, request, session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask.views import View
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db import db, Movies, Shows, Games, users

app = Flask(__name__)
app.secret_key = "Remember, Remember the 5th of November"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pbjreviews.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.route("/")
def home():
    if current_user.is_authenticated:
        name = current_user.name
        return render_template("index.html", name=name)
    else:
        return redirect(url_for('login'))

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/login/", methods=["POST"])
def login_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = users.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('home'))

@app.route("/register/")
def register():
    return render_template('register.html')

@app.route("/register/", methods=['POST'])
def register_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = users.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('register'))
    
    new_user = users(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route("/movies/")
def movies():
    movies = Movies.query.all()
    return render_template('movies.html', movies=movies)

@app.route('/create_movie', methods = ['POST'])
def create_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        director = request.form['director']
        franchise = request.form['franchise']
        rating = request.form['rating']

        new_movie = Movies(title, genre, director, franchise, rating)
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('movies'))
    
@app.route("/games/")
def games():
    games = Games.query.all()
    return render_template('games.html', games=games)

@app.route('/create_game', methods = ['POST'])
def create_game():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        developer = request.form['director']
        franchise = request.form['franchise']
        rating = request.form['rating']

        new_game = Games(title, genre, developer, franchise, rating)
        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('games'))
    
@app.route("/shows/")
def shows():
    shows = Shows.query.all()
    return render_template('shows.html', shows=shows)

@app.route('/create_show', methods = ['POST'])
def create_show():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        director = request.form['director']
        franchise = request.form['franchise']
        rating = request.form['rating']

        new_show = Shows(title, genre, director, franchise, rating)
        db.session.add(new_show)
        db.session.commit()

        return redirect(url_for('shows'))

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)