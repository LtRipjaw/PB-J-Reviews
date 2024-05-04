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
        new_movie = Movies(
            title = request.form.get('title'),
            genre = request.form.get('genre'),
            director = request.form.get('director'),
            franchise = request.form.get('franchise'),
            rating = request.form.get('rating')
        )

        db.session.add(new_movie)
        flash('Succesfully Created!')
        db.session.commit()

        return redirect(url_for('movies'))
    
@app.route('/edit_movie', methods = ['POST'])
def edit_movie():
    if request.method == 'POST':
        movie = Movies.query.get(request.form.get('id'))

        movie.title = request.form.get('title')
        movie.genre = request.form.get('genre')
        movie.director = request.form.get('director')
        movie.franchise = request.form.get('franchise')
        movie.rating = request.form.get('rating')

        db.session.commit()
        flash('Succesfully Updated!')

        return redirect(url_for('movies'))

@app.route('/delete_movie/<id>', methods = ['GET', 'POST'])
def delete_movie(id):
    movie = Movies.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    flash('Deleted Successfully!')
    return redirect(url_for('movies'))
    
@app.route("/games/")
def games():
    games = Games.query.all()
    return render_template('games.html', games=games)

@app.route('/create_game', methods = ['POST'])
def create_game():
    if request.method == 'POST':
        new_game = Games(
            title = request.form.get('title'),
            genre = request.form.get('genre'),
            developer = request.form.get('developer'),
            franchise = request.form.get('franchise'),
            rating = request.form.get('rating')
        )

        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('games'))
    
@app.route('/edit_game', methods = ['POST'])
def edit_game():
    if request.method == 'POST':
        game = Games.query.get(request.form.get('id'))

        game.title = request.form.get('title')
        game.genre = request.form.get('genre')
        game.developer = request.form.get('developer')
        game.franchise = request.form.get('franchise')
        game.rating = request.form.get('rating')

        db.session.commit()
        flash('Succesfully Updated!')

        return redirect(url_for('games'))

@app.route('/delete_game/<id>', methods = ['GET', 'POST'])
def delete_game(id):
    game = Games.query.get(id)
    db.session.delete(game)
    db.session.commit()
    flash('Deleted Successfully!')
    return redirect(url_for('games'))
    
@app.route("/shows/")
def shows():
    shows = Shows.query.all()
    return render_template('shows.html', shows=shows)

@app.route('/create_show/', methods = ['POST'])
def create_show():
    if request.method == 'POST':
        new_show = Shows(
            title = request.form.get('title'),
            genre = request.form.get('genre'),
            director = request.form.get('director'),
            franchise = request.form.get('franchise'),
            rating = request.form.get('rating')
        )

        db.session.add(new_show)
        db.session.commit()

        return redirect(url_for('shows'))
    
@app.route('/edit_show/', methods = ['POST'])
def edit_show():
    if request.method == 'POST':
        show = Shows.query.get(request.form.get('id'))

        show.title = request.form.get('title')
        show.genre = request.form.get('genre')
        show.director = request.form.get('director')
        show.franchise = request.form.get('franchise')
        show.rating = request.form.get('rating')

        db.session.commit()
        flash('Succesfully Updated!')

        return redirect(url_for('shows'))

@app.route('/delete_show/<id>', methods = ['GET', 'POST'])
def delete_show(id):
    show = Shows.query.get(id)
    db.session.delete(show)
    db.session.commit()
    flash('Deleted Successfully!')
    return redirect(url_for('shows'))

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)