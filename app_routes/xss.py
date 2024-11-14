from flask import Blueprint, request, render_template_string

bp = Blueprint("xss", __name__)

# Simulated storage for comments
comments = []

@bp.route("/", methods=["GET", "POST"])
def xss_demo():
    if request.method == "POST":
        comment = request.form.get("comment")
        comments.append(comment)  # Vulnerable to XSS
    return render_template_string("""
        <html>
        <head>
            <title>User Comments</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    padding: 20px;
                    margin: 0;
                }
                .container {
                    width: 100%;
                    max-width: 600px;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                h2 {
                    color: #333;
                    text-align: center;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    margin-bottom: 20px;
                }
                textarea {
                    padding: 10px;
                    font-size: 16px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    resize: vertical;
                    margin-bottom: 15px;
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
                .comments-section {
                    margin-top: 20px;
                }
                .comment {
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-radius: 4px;
                    margin-bottom: 10px;
                }
                .comment p {
                    margin: 0;
                    font-size: 16px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>User Comments</h2>
                <form method="post">
                    <label for="comment">Add your comment:</label>
                    <textarea name="comment" id="comment" rows="4" placeholder="Write your comment here..."></textarea>
                    <input type="submit" value="Submit Comment">
                </form>
                <div class="comments-section">
                    <h3>All Comments:</h3>
                    {% for comment in comments %}
                        <div class="comment">
                            <p>{{ comment | safe }}</p>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </body>
        </html>
    """, comments=comments)
