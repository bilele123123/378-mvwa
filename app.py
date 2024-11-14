from flask import Flask, redirect, url_for, render_template
from app_routes import sql_injection, xss, csrf, open_redirect, user_enum, file_upload, weak_session_id, csp_bypass, insecure_captcha, reflected_xss
import sqlite3
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)  # Generate a random secret key each time you run the app

# Configure the upload folder path
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Set upload path to 'uploads' in the current directory

# Initialize the SQLite database
def init_sqlite_db():
    conn = sqlite3.connect('vulnerable_app.db')
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_sqlite_db()

# Register Blueprints for each vulnerability
app.register_blueprint(sql_injection.bp, url_prefix="/sql_injection")
app.register_blueprint(xss.bp, url_prefix="/xss")
app.register_blueprint(csrf.bp, url_prefix="/csrf")
app.register_blueprint(open_redirect.bp, url_prefix="/open_redirect")
app.register_blueprint(user_enum.bp, url_prefix="/user_enum")
app.register_blueprint(file_upload.bp, url_prefix="/file_upload")
app.register_blueprint(weak_session_id.bp, url_prefix="/weak_session_id")
app.register_blueprint(csp_bypass.bp, url_prefix="/csp_bypass")
app.register_blueprint(insecure_captcha.bp, url_prefix="/insecure_captcha")
app.register_blueprint(reflected_xss.bp, url_prefix="/reflected_xss")

# Initialize the file upload folder by calling init_file_upload
file_upload.init_file_upload(app.config['UPLOAD_FOLDER'])

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
