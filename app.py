from flask import Flask, redirect, url_for, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask.views import View
import db

app = Flask(__name__)
app.secret_key = "Remember, Remember the 5th of November"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pbjreviews.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.users.query.get(int(user_id))

class ListView(View):
    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        items = self.model.query.all()
        return render_template(self.template, items=items)
    
app.add_url_rule(
    "/movies/",
    view_func=ListView.as_view("movie_list", db.movies, "movies.html"),
)

app.add_url_rule(
    "/games/",
    view_func=ListView.as_view("game_list", db.games, "games.html"),
)

app.add_url_rule(
    "/shows/",
    view_func=ListView.as_view("show_list", db.shows, "shows.html"),
)

app.add_url_rule(
    "/directors/",
    view_func=ListView.as_view("director_list", db.directors, "directors.html"),
)

app.add_url_rule(
    "/developers/",
    view_func=ListView.as_view("developer_list", db.developers, "developers.html"),
)

app.add_url_rule(
    "/franchises/",
    view_func=ListView.as_view("franchise_list", db.franchises, "franchises.html"),
)

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

    user = db.users.query.filter_by(email=email).first()

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

    user = db.users.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('register'))
    
    new_user = db.users(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)