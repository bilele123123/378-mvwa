from flask import Blueprint, request, render_template_string

bp = Blueprint("reflected_xss", __name__)

@bp.route("/", methods=['GET'])
def xss_demo():
    # Capture user input from the query parameter
    user_input = request.args.get("input", "")
    
    # Render the HTML content
    return render_template_string("""
        <html>
            <body>
                <h1>Reflected XSS Demo</h1>
                <p>Enter a message in the URL query parameter "input" to see it reflected below.</p>
                <p>Example: <code>?input=&lt;script&gt;alert('XSS')&lt;/script&gt;</code></p>
                <h2>User Input:</h2>
                <h1>{{ user_input|safe }}</h1>
            </body>
        </html>
    """, user_input=user_input), 200
