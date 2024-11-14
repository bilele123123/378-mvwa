from flask import Blueprint, request, render_template_string
import sqlite3

bp = Blueprint("user_enum", __name__)

@bp.route("/", methods=["GET", "POST"])
def user_enum_demo():
    if request.method == "POST":
        username = request.form.get("username")
        
        # Vulnerable to user enumeration
        conn = sqlite3.connect('vulnerable_app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone() is not None
        conn.close()
        
        if user_exists:
            message = "User found. Please enter password."
        else:
            message = "User does not exist."  # Vulnerable to user enumeration
        
        # Render the template with the message
        return render_template_string("""
            <html>
            <head>
                <title>Login Name Search</title>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                    }
                    .search-container {
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
                    input[type="text"] {
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
                    .message {
                        margin-top: 20px;
                        font-size: 14px;
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <div class="search-container">
                    <h2>Login Name Search</h2>
                    <form method="post">
                        <label for="username">Username</label>
                        <input type="text" name="username" id="username" placeholder="Enter username" required>
                        <input type="submit" value="Search">
                    </form>
                    {% if message %}
                        <p class="message">{{ message }}</p>
                    {% endif %}
                </div>
            </body>
            </html>
        """, message=message)
    
    # Initial GET request view
    return render_template_string("""
        <html>
        <head>
            <title>Login Name Search</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                }
                .search-container {
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
                input[type="text"] {
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
            </style>
        </head>
        <body>
            <div class="search-container">
                <h2>Login Name Search</h2>
                <form method="post">
                    <label for="username">Username</label>
                    <input type="text" name="username" id="username" placeholder="Enter username" required>
                    <input type="submit" value="Search">
                </form>
            </div>
        </body>
        </html>
    """)
