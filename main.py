from flask import Flask, render_template_string, redirect, url_for
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted, logout_user
from database import db_session, init_db
from models import User, Role
import os
 
# Create a flask application
app = Flask(__name__)
app.config['DEBUG'] = True

# Enter a secret key. You can generate a key using secrets.token_urlsafe()
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
# Set SALT value. You can generate a good salt for password hashing using: secrets.SystemRandom().getrandbits(128)
app.config["SECURITY_PASSWORD_SALT"] = os.getenv('SECURITY_PASSWORD_SALT')
# Don't worry if email has findable domain
app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}

# manage sessions per request - make sure connections are closed and returned
app.teardown_appcontext(lambda exc: db_session.close())

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string('Hello {{current_user.email}}!')

@app.route("/user")
@auth_required()
@permissions_accepted("user-read")
def user_home():
    return render_template_string("Hello {{ current_user.email }} you are a user!")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for(""))

# one time setup
with app.app_context():
    init_db()
    # Create a user and role to test with
    security.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )
    db_session.commit()
    if not security.datastore.find_user(email="test@me.com"):
        security.datastore.create_user(email="test@me.com",
        password=hash_password("password"), roles=["user"])
    db_session.commit()

if __name__ == '__main__':
    # run application (can also use flask run)
    app.run()