from flask import Flask, render_template_string, Blueprint, make_response

bp = Blueprint("csp_bypass", __name__)

@bp.route("/", methods=['GET'])
def csp_bypass_demo():
    # A misconfigured CSP that allows inline scripts, demonstrating a bypass
    response_content = """
    <html>
        <head>
            <title>CSP Bypass Demo</title>
            <meta charset="UTF-8">
            <!-- Intentionally weak CSP allowing 'unsafe-inline' -->
            <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline';">
        </head>
        <body>
            <h1>CSP Bypass Example</h1>
            <p>
                This page has a Content Security Policy (CSP) that allows inline scripts via <code>'unsafe-inline'</code>.
                This setting is risky, as it enables attackers to inject and run scripts directly on the page, potentially bypassing CSP restrictions.
            </p>
            <p>Observe the alert triggered by an inline script below:</p>
            <script>alert('This is a CSP bypass example due to unsafe-inline policy');</script>

            <h2>Why This is Vulnerable</h2>
            <p>
                By allowing <code>'unsafe-inline'</code> in the CSP, we enable any inline script to execute. This could lead to XSS attacks if an attacker manages to inject code here.
            </p>
            <p>
                To avoid this vulnerability, a stricter CSP policy should avoid <code>'unsafe-inline'</code> and rely on nonce-based or hash-based CSPs instead.
            </p>
        </body>
    </html>
    """
    
    response = make_response(render_template_string(response_content))
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline';"
    return response
