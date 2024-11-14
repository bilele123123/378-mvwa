from flask import Blueprint, request, render_template_string

bp = Blueprint("insecure_captcha", __name__)

@bp.route("/", methods=['GET', 'POST'])
def insecure_captcha_demo():
    # Simple CAPTCHA without complexity or rate limiting
    if request.method == 'POST':
        user_input = request.form.get('captcha')
        if user_input == "1234":  # Static CAPTCHA value
            return render_template_string("""
                <html>
                <head>
                    <title>CAPTCHA Verification</title>
                    <style>
                        .message { font-size: 1.2em; color: #28a745; }
                        .container { display: flex; align-items: center; justify-content: center; height: 100vh; }
                        .card { max-width: 400px; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background-color: white; text-align: center; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="card">
                            <p class="message">CAPTCHA passed successfully!</p>
                            <a href="/">Go back</a>
                        </div>
                    </div>
                </body>
                </html>
            """)
        return render_template_string("""
            <html>
            <head>
                <title>CAPTCHA Verification</title>
                <style>
                    .message { font-size: 1.2em; color: #dc3545; }
                    .container { display: flex; align-items: center; justify-content: center; height: 100vh; }
                    .card { max-width: 400px; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background-color: white; text-align: center; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="card">
                        <p class="message">CAPTCHA failed. Please try again.</p>
                        <a href="/">Go back</a>
                    </div>
                </div>
            </body>
            </html>
        """)

    # Initial GET request view
    return render_template_string("""
        <html>
        <head>
            <title>CAPTCHA Verification</title>
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
                .container {
                    width: 100%;
                    max-width: 400px;
                    padding: 20px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                    text-align: center;
                }
                h2 {
                    margin-bottom: 15px;
                    color: #333;
                }
                p {
                    color: #555;
                    font-size: 16px;
                    margin-bottom: 15px;
                }
                img {
                    margin-bottom: 15px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    max-width: 100%; /* Ensures the image fits within the form */
                    height: auto;
                }
                input[type="text"] {
                    padding: 10px;
                    font-size: 16px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    width: calc(100% - 22px); /* Adjust for padding */
                    margin-bottom: 15px;
                }
                button {
                    background-color: #007bff;
                    color: white;
                    font-size: 16px;
                    padding: 10px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                    width: 100%;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>CAPTCHA Verification</h2>
                <p>Please enter the text shown in the image below:</p>
                <img src="https://cdn.textstudio.com/output/sample/normal/7/0/7/3/1234-logo-578-13707.png" alt="CAPTCHA Image">
                <form method="POST">
                    <input type="text" name="captcha" placeholder="Enter CAPTCHA code" required>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
    """)
