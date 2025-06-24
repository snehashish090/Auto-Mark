from flask import *
from flask_session import Session
from functools import wraps
from datetime import timedelta
from hashlib import sha256
from db import DataBase, DIRECTORY
app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"  # Or 'redis', 'memcached', etc.
app.config["SECRET_KEY"] = "supersecret"   # Required for sessions to work securely
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=40)

Session(app)

# Helper function to hash passwords
def hashString(input_string):
    return sha256(input_string.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get("logStatus"):
            session["logStatus"] = False
        if session["logStatus"] == False:
            return redirect('/login')
        return f(*args, **kwargs)

    return wrap

@app.route("/", methods=["GET"])
@login_required
def index():
    db = DataBase()
    sightings = db.get_all_sightings()

    return render_template("index.html", sightings=sightings)

@app.route("/login", methods=["GET", "POST"])
def login_function():

    error_code = 200

    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = hashString(request.form.get("password"))

        db = DataBase()

        if db.verify_admin(user_id, password):

            session['logStatus'] = True
            session['user_id'] = user_id
            session.permanent = True  # trigger expiration logic
            return redirect("/")
        else:
            error_code=403
            return render_template("login.html", error_code=error_code)

    return render_template("login.html", error_code=error_code)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session['logStatus'] = False
    session['user_id'] = None
    session.permanent = True  # trigger expiration logic

    return redirect("/")

@app.route("/add/faces", methods=["GET", "POST"])
@login_required
def add_faces():
    if request.method == "POST":
        uploaded_data = {}

        for key in request.files:
            file = request.files[key]

            name_key = key.replace("file_", "name_")
            name = request.form.get(name_key)

            if file and name:
                # Example: Save file to disk (optional)
                save_path = DIRECTORY+f"/data_set/{name}_{file.filename}"
                file.save(save_path)

                db = DataBase()
                db.add_person(name, save_path)

                return redirect("/")
            else:
                return render_template("add.html", problem=True)

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)