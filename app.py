from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from config import SECRET_KEY

from modules import auth, routes, honeypot  # Import blueprints
from modules.database import create_tables  # Initialize database

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")
app.secret_key = SECRET_KEY 

bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(routes.bp)
app.register_blueprint(honeypot.bp)

# Initialize the database
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
