from flask import Blueprint, request, redirect, render_template_string
import re

bp = Blueprint("open_redirect", __name__)

# List of allowed base URLs for redirection
ALLOWED_DOMAINS = ["google.com", "www.google.com"]

@bp.route("/", methods=["GET"])
def open_redirect_demo():
    # Get the target URL from the query parameter
    target = request.args.get("target")

    # If no target is provided, show the interactive demo page
    if not target:
        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Open Redirect Demo</title>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                    }
                    .container {
                        max-width: 400px;
                        width: 100%;
                        padding: 20px;
                        background-color: #ffffff;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        border-radius: 8px;
                        text-align: center;
                    }
                    h1 {
                        color: #333333;
                    }
                    p {
                        color: #555555;
                        font-size: 16px;
                    }
                    .btn {
                        display: inline-block;
                        margin: 10px;
                        padding: 10px 20px;
                        font-size: 16px;
                        color: #ffffff;
                        background-color: #007bff;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        text-decoration: none;
                        transition: background-color 0.3s;
                    }
                    .btn:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Open Redirect Demonstration</h1>
                    <p>Click one of the buttons below to test the application’s response to trusted and untrusted redirects.</p>
                    <a href="?target=https://www.google.com" class="btn">Trusted Redirect</a>
                    <a href="?target=http://gogle.com" class="btn">Untrusted Redirect</a>
                    <p>Note: Trusted redirects are allowed, while untrusted redirects are blocked.</p>
                </div>
            </body>
            </html>
        """)

    # Parse the domain from the target URL
    match = re.match(r'^https?://([^/]+)', target)
    if match:
        domain = match.group(1)
        # Check if the domain is in the list of allowed domains
        if domain in ALLOWED_DOMAINS:
            return redirect(target)  # Safe redirect to a trusted domain

    # If the domain is not allowed, show a blocked message
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Redirect Blocked</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                }
                .container {
                    max-width: 400px;
                    width: 100%;
                    padding: 20px;
                    background-color: #ffffff;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                    text-align: center;
                }
                h1 {
                    color: #e74c3c;
                }
                p {
                    color: #555555;
                    font-size: 16px;
                }
                .btn {
                    display: inline-block;
                    margin-top: 15px;
                    padding: 10px 20px;
                    font-size: 16px;
                    color: #ffffff;
                    background-color: #007bff;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                    transition: background-color 0.3s;
                }
                .btn:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Redirect Blocked</h1>
                <p>The target URL <code>{{ target }}</code> is not permitted.</p>
                <p>Only links to trusted sites are allowed for security purposes.</p>
                <a href="/" class="btn">Back to Demo</a>
            </div>
        </body>
        </html>
    """, target=target), 400
