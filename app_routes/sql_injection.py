from flask import Blueprint, request, render_template_string, session
import sqlite3
import time
from datetime import datetime
import random

bp = Blueprint("sql_injection", __name__)
bp.secret_key = "supersecretkey"  # Secret key for session management

# Login attempt limit and lockout duration (in seconds)
MAX_ATTEMPTS = 3
LOCKOUT_DURATION = 120  # 2 minutes

@bp.route("/", methods=["GET", "POST"])
def sql_injection_demo():
    # Initialize session variables if they don't exist
    if "login_attempts" not in session:
        session["login_attempts"] = 0
    if "lockout_time" not in session:
        session["lockout_time"] = 0

    # Check if user is in the lockout period
    if session["login_attempts"] >= MAX_ATTEMPTS:
        remaining_lockout = session["lockout_time"] - time.time()
        if remaining_lockout > 0:
            # User is locked out
            return render_template_string("""
                <html>
                <body>
                    <h2>Login</h2>
                    <p class="error-message">Too many failed attempts. Please try again in {{ remaining_lockout|round }} seconds.</p>
                </body>
                </html>
            """, remaining_lockout=remaining_lockout)

        # Reset lockout once the duration has passed
        session["login_attempts"] = 0
        session["lockout_time"] = 0

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Vulnerable query
        conn = sqlite3.connect('vulnerable_app.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)

        results = cursor.fetchall()
        conn.close()

        if results:
            # Successful login
            session["login_attempts"] = 0  # Reset attempts on successful login

            # Generate login success details
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_number = random.randint(100000, 999999)

            return render_template_string("""
                <html>
                <body>
                    <h2>Login Successful</h2>
                    <p>Welcome, {{ username }}!</p>
                    <p>Current Date and Time: {{ current_datetime }}</p>
                    <p>Your Session Number: {{ session_number }}</p>
                    <p>You now have access to this web app!</p>
                </body>
                </html>
            """, username=username, current_datetime=current_datetime, session_number=session_number)
        else:
            # Increment failed attempts
            session["login_attempts"] += 1

            # Check if the lockout threshold is reached
            if session["login_attempts"] >= MAX_ATTEMPTS:
                session["lockout_time"] = time.time() + LOCKOUT_DURATION
                remaining_lockout = LOCKOUT_DURATION
                return render_template_string("""
                    <html>
                    <body>
                        <h2>Login</h2>
                        <p class="error-message">Too many failed attempts. Please try again in {{ remaining_lockout }} seconds.</p>
                    </body>
                    </html>
                """, remaining_lockout=remaining_lockout)

            # Show error message for invalid login attempt
            error_message = "Invalid credentials! Try again!"
            return render_template_string("""
                <html>
                <body>
                    <div class="login-container">
                        <h2>Login</h2>
                        <form method="post">
                            <label for="username">Username</label>
                            <input type="text" name="username" id="username" required>
                            <label for="password">Password</label>
                            <input type="password" name="password" id="password" required>
                            <input type="submit" value="Login">
                        </form>
                        <p class="error-message">{{ error_message }}</p>
                    </div>
                </body>
                </html>
            """, error_message=error_message)

    # Render login form if the request method is GET
    return render_template_string("""
        <html>
        <head>
            <title>Login</title>
            <style>
                /* Centered and clean layout */
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                }
                .login-container {
                    width: 100%;
                    max-width: 400px;
                    padding: 20px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                    text-align: center;
                }
                h2 {
                    margin-bottom: 20px;
                    color: #333;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }
                label {
                    text-align: left;
                    color: #555;
                    font-size: 14px;
                }
                input[type="text"], input[type="password"] {
                    padding: 10px;
                    font-size: 16px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                input[type="submit"] {
                    background-color: #007bff;
                    color: white;
                    font-size: 16px;
                    padding: 10px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                .error-message {
                    color: red;
                    font-size: 14px;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h2>Login</h2>
                <form method="post">
                    <label for="username">Username</label>
                    <input type="text" name="username" id="username" required>
                    <label for="password">Password</label>
                    <input type="password" name="password" id="password" required>
                    <input type="submit" value="Login">
                </form>
            </div>
        </body>
        </html>
    """)
