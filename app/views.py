from flask import Flask, render_template, request, redirect, url_for
from .model import bdd
from .model.user import User
from mysql.connector import Error as  mysql_connector_error
from flask_login import LoginManager, login_required, login_user

login_manager = LoginManager()


app = Flask(__name__)

login_manager.init_app(app)
app.template_folder = "./templates"
app.static_folder = "./static"
app.config.from_object("app.config")

@app.route("/")
@login_required
def index():
    return render_template("index.html")


# ========================================= USER ======================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Le form envoyé
        if "username" in request.form and "password" in request.form:
            try :
                user_id = bdd.log_user(request.form["username"], request.form["password"])
            except  mysql_connector_error:
                return "", 525
            if type(user_id) == int:
                user = User(user_id)
                login_user(user)
                return "Ok", 200
            else:
                return "WRONG username/password", 403
    return render_template("login.html")

@app.route("/create_account", methods=["GET","POST"])
def create_account():
    if request.method == "POST":
        if "password" in request.form and "password_confirm" in request.form and "username" in request.form :
            password = request.form["password"]
            password2 = request.form["password_confirm"]
            username = request.form["username"]
            if password == password2 and len(password) > 4 and len(username) >= 4 :
                bdd.create_account(username, password)
                # TODO : vérifier la réponse de la bdd (si l'utilisateur existe déjà...)
    return render_template("create_account.html")
# =======================================================================================

@app.route("/membres")
def membres():
    msg, listeMembre = bdd.get_membresData()
    print(msg)
    return render_template("membres.html",liste=listeMembre)


@login_manager.unauthorized_handler
def unauthorized():
    # redirect user not logged to login page
    return redirect(url_for("login", next=request.endpoint))

@login_manager.user_loader 
def user_loader(user_id):
    return User(user_id)

